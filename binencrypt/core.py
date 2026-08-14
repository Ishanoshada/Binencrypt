#!/usr/bin/env python3
"""
binencrypt.core - Recursive Python code encryption with marshal optimisation, watermarking, and visible watermarks.
Version: 2.7.6
"""

import os
import sys
import re
import random
import hashlib
import base64
import zlib
import gzip
import marshal
import binascii
import argparse
import functools
import subprocess
import secrets
import time
from typing import Optional, List, Dict, Any

__version__ = "2.7.4"
__author__ = "K.A. ISHAN OSHADA"


class CryptoVault:
    """Single layer of encryption operations."""

    _OPERATIONS = [
        'b16encode', 'b32encode', 'b64encode', 'a85encode',
        'hexlify', 'b2a_base64', 'b2a_hex',
        'gzip_compress', 'zlib_compress', 'marshal_dumps'
    ]

    _REVERSE_OPERATIONS = {
        'b16encode': 'b16decode',
        'b32encode': 'b32decode',
        'b64encode': 'b64decode',
        'a85encode': 'a85decode',
        'hexlify': 'unhexlify',
        'b2a_base64': 'a2b_base64',
        'b2a_hex': 'a2b_hex',
        'gzip_compress': 'gzip_decompress',
        'zlib_compress': 'zlib_decompress',
        'marshal_dumps': 'marshal_loads'
    }

    def __init__(self, key: str, min_ops: int = 3, max_ops: int = 5, seed_suffix: str = ""):
        self.key = key
        self.min_ops = min_ops
        self.max_ops = max_ops
        random.seed(key + '::sequence' + seed_suffix)
        num_ops = random.randint(min_ops, max_ops)
        self._sequence = [random.choice(self._OPERATIONS) for _ in range(num_ops)]

    def _apply_operation(self, data: bytes, op: str, direction: str = 'forward') -> bytes:
        if direction == 'forward':
            if op == 'b16encode':
                return base64.b16encode(data)
            elif op == 'b32encode':
                return base64.b32encode(data)
            elif op == 'b64encode':
                return base64.b64encode(data)
            elif op == 'a85encode':
                return base64.a85encode(data)
            elif op == 'hexlify':
                return binascii.hexlify(data)
            elif op == 'b2a_base64':
                return binascii.b2a_base64(data).rstrip(b'\n')
            elif op == 'b2a_hex':
                return binascii.b2a_hex(data)
            elif op == 'gzip_compress':
                return gzip.compress(data)
            elif op == 'zlib_compress':
                return zlib.compress(data)
            elif op == 'marshal_dumps':
                return marshal.dumps(data)
        else:
            if op == 'b16decode':
                return base64.b16decode(data, casefold=True)
            elif op == 'b32decode':
                return base64.b32decode(data)
            elif op == 'b64decode':
                return base64.b64decode(data)
            elif op == 'a85decode':
                return base64.a85decode(data)
            elif op == 'unhexlify':
                return binascii.unhexlify(data)
            elif op == 'a2b_base64':
                return binascii.a2b_base64(data)
            elif op == 'a2b_hex':
                return binascii.a2b_hex(data)
            elif op == 'gzip_decompress':
                return gzip.decompress(data)
            elif op == 'zlib_decompress':
                return zlib.decompress(data)
            elif op == 'marshal_loads':
                return marshal.loads(data)
        return data

    def encrypt(self, plaintext: bytes) -> bytes:
        data = plaintext
        for op in self._sequence:
            data = self._apply_operation(data, op, 'forward')
        return data

    def get_reverse_ops(self) -> List[str]:
        return [self._REVERSE_OPERATIONS[op] for op in reversed(self._sequence)]


class RecursiveVault:
    """Recursive encryption with marshal optimisation and watermarking."""

    HEADER = '# ENCRYPTED_VIA_BINENCRYPT\n'

    def __init__(
        self,
        master_key: str,
        depth: int,
        min_ops_per_layer: int = 3,
        max_ops_per_layer: int = 5,
        use_marshal: bool = True,
        watermark: Optional[str] = None
    ):
        self.master_key = master_key
        self.depth = depth
        self.min_ops = min_ops_per_layer
        self.max_ops = max_ops_per_layer
        self.use_marshal = use_marshal
        self.watermark = watermark

    def _build_layer_vault(self, layer_index: int) -> CryptoVault:
        return CryptoVault(
            key=self.master_key,
            min_ops=self.min_ops,
            max_ops=self.max_ops,
            seed_suffix=f"::layer{layer_index}"
        )

    def _make_self_decrypting_script(
        self,
        encrypted_data: bytes,
        reverse_ops: List[str],
        compact: bool = True,
        is_innermost: bool = False
    ) -> str:
        """
        Generate a script that decrypts `encrypted_data` and executes the result.
        If `use_marshal` is True, the decrypted result is a marshal‑serialised code object.
        """
        encrypted_repr = repr(encrypted_data)

        if compact:
            # Build the nested decryption pipeline
            expr = encrypted_repr
            for op in reverse_ops:
                if op == 'b16decode':
                    expr = f'base64.b16decode({expr}, casefold=True)'
                elif op == 'b32decode':
                    expr = f'base64.b32decode({expr})'
                elif op == 'b64decode':
                    expr = f'base64.b64decode({expr})'
                elif op == 'a85decode':
                    expr = f'base64.a85decode({expr})'
                elif op == 'unhexlify':
                    expr = f'binascii.unhexlify({expr})'
                elif op == 'a2b_base64':
                    expr = f'binascii.a2b_base64({expr})'
                elif op == 'a2b_hex':
                    expr = f'binascii.a2b_hex({expr})'
                elif op == 'gzip_decompress':
                    expr = f'gzip.decompress({expr})'
                elif op == 'zlib_decompress':
                    expr = f'zlib.decompress({expr})'
                elif op == 'marshal_loads':
                    expr = f'marshal.loads({expr})'

            if self.use_marshal:
                script = f'import base64,binascii,zlib,gzip,marshal;exec(marshal.loads({expr}))'
            else:
                script = f'import base64,binascii,zlib,gzip,marshal;exec(compile({expr}.decode(),"<encrypted>","exec"))'

            return script
        else:
            # Readable version (multi‑line)
            lines = [
                self.HEADER,
                '# Generated by binencrypt (recursive mode)',
                '',
                'import base64, binascii, zlib, gzip, marshal',
                '',
                'def _decrypt_and_run():',
                f'    encrypted = {encrypted_repr}',
                '    data = encrypted'
            ]
            for i, op in enumerate(reverse_ops, 1):
                if op == 'b16decode':
                    lines.append(f'    data = base64.b16decode(data, casefold=True)  # Layer {i}')
                elif op == 'b32decode':
                    lines.append(f'    data = base64.b32decode(data)  # Layer {i}')
                elif op == 'b64decode':
                    lines.append(f'    data = base64.b64decode(data)  # Layer {i}')
                elif op == 'a85decode':
                    lines.append(f'    data = base64.a85decode(data)  # Layer {i}')
                elif op == 'unhexlify':
                    lines.append(f'    data = binascii.unhexlify(data)  # Layer {i}')
                elif op == 'a2b_base64':
                    lines.append(f'    data = binascii.a2b_base64(data)  # Layer {i}')
                elif op == 'a2b_hex':
                    lines.append(f'    data = binascii.a2b_hex(data)  # Layer {i}')
                elif op == 'gzip_decompress':
                    lines.append(f'    data = gzip.decompress(data)  # Layer {i}')
                elif op == 'zlib_decompress':
                    lines.append(f'    data = zlib.decompress(data)  # Layer {i}')
                elif op == 'marshal_loads':
                    lines.append(f'    data = marshal.loads(data)  # Layer {i}')

            if self.use_marshal:
                lines.append('    exec(marshal.loads(data))')
            else:
                lines.append('    code = data.decode("utf-8")')
                lines.append('    exec(compile(code, "<encrypted>", "exec"))')

            lines.append('')
            lines.append('if __name__ == "__main__":')
            lines.append('    _decrypt_and_run()')
            return '\n'.join(lines)

    def generate_recursive_script(self, plaintext: str, compact: bool = True) -> str:
        # Inject watermark inside the payload (if provided)
        if self.watermark:
            safe_wm = self.watermark.replace("'", "\\'")
            watermark_code = f"# WATERMARK: {self.watermark}\n__watermark__ = '{safe_wm}'\n"
            plaintext = watermark_code + plaintext

        # Start with the innermost payload
        if self.use_marshal:
            code_obj = compile(plaintext, '<encrypted>', 'exec')
            current_payload = marshal.dumps(code_obj)
        else:
            current_payload = plaintext.encode('utf-8')

        current_script = None
        print(f"Encrypting {self.depth} layers...")
        for layer_idx in range(self.depth, 0, -1):
            print(f"  Layer {layer_idx}/{self.depth}...", end='', flush=True)
            start = time.time()
            vault = self._build_layer_vault(layer_idx)
            encrypted = vault.encrypt(current_payload)
            reverse_ops = vault.get_reverse_ops()
            current_script = self._make_self_decrypting_script(
                encrypted, reverse_ops, compact=compact
            )
            current_payload = current_script.encode('utf-8')
            elapsed = time.time() - start
            print(f" done ({len(current_script):,} bytes, {elapsed:.2f}s)")

        return current_script


def encrypt_python_file(
    input_file: str,
    output_file: Optional[str] = None,
    depth: int = 1,
    key: Optional[str] = None,
    min_ops: int = 3,
    max_ops: int = 5,
    compile_pyc: bool = False,
    compact: bool = True,
    use_marshal: bool = True,
    watermark: Optional[str] = None,
    visible_watermark: Optional[str] = None
) -> None:
    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()

    if output_file is None:
        output_file = input_file.replace('.py', '.encrypted.py')
        if output_file == input_file:
            output_file = f"{input_file}.encrypted.py"

    if depth < 1:
        raise ValueError("Depth must be at least 1")

    master_key = key or secrets.token_hex(32)

    # Use watermark as internal watermark if visible_watermark is not given, else both.
    internal_wm = watermark or visible_watermark

    vault = RecursiveVault(master_key, depth, min_ops, max_ops, use_marshal, internal_wm)
    final_script = vault.generate_recursive_script(source, compact=compact)

    # Prepend visible watermark comment if provided
    if visible_watermark:
        final_script = f"# VISIBLE WATERMARK: {visible_watermark}\n" + final_script

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_script + '\n')

    if compile_pyc:
        subprocess.run(
            [sys.executable, '-m', 'py_compile', output_file],
            check=True,
            capture_output=True
        )
        print(f"✓ Compiled to: {output_file}c")

    print(f"✓ Encrypted: {input_file} -> {output_file}")
    print(f"  Depth: {depth} layers")
    print(f"  Key: {master_key[:16]}...")
    print(f"  Operations per layer: {min_ops}–{max_ops}")
    print(f"  Mode: {'marshal' if use_marshal else 'source'}")
    if internal_wm:
        print(f"  Internal watermark: '{internal_wm}'")
    if visible_watermark:
        print(f"  Visible watermark: '{visible_watermark}'")


def decrypt_python_file(
    input_file: str,
    key: str,
    output_file: Optional[str] = None
) -> str:
    raise NotImplementedError(
        "Decryption of recursive compact mode is not implemented. "
        "Please use --readable when encrypting if you need to decrypt later, "
        "or use the original source code."
    )


def execute_cli() -> None:
    parser = argparse.ArgumentParser(
        prog='binencrypt',
        description='binencrypt - Recursive Python Code Encryption v2.7.4',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encrypt with a visible watermark (comment at top of output file)
  binencrypt -i script.py -o encrypted.py --depth 10 --visible "MyCompany 2024"

  # Also embed an internal watermark (inside the encrypted payload)
  binencrypt -i script.py -o encrypted.py --depth 10 --watermark "Build: 42" --visible "MyCompany 2024"

  # Use a shorter alias for visible watermark
  binencrypt -i script.py -o encrypted.py --depth 10 --vwm "v1.0"

  # Fast mode with visible watermark
  binencrypt -i script.py -o encrypted.py --depth 10 --fast --vwm "internal-use"
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input Python file')
    parser.add_argument('-o', '--output', default=None, help='Output file')
    parser.add_argument('--depth', type=int, default=1, help='Number of recursive layers')
    parser.add_argument('--key', default=None, help='Master encryption key')
    parser.add_argument('--min-ops', type=int, default=3, help='Min operations per layer')
    parser.add_argument('--max-ops', type=int, default=5, help='Max operations per layer')
    parser.add_argument('--fast', action='store_true', help='Fast mode (min-ops=2, max-ops=4)')
    parser.add_argument('--compile', action='store_true', help='Compile to .pyc')
    parser.add_argument('--readable', action='store_true', help='Generate readable output')
    parser.add_argument('--marshal', action='store_true', dest='use_marshal', help='Use marshal mode (default)')
    parser.add_argument('--no-marshal', action='store_false', dest='use_marshal', help='Disable marshal mode')
    parser.add_argument('--func', action='store_true', help='Alias for --marshal')
    parser.add_argument('--watermark', '--wm', dest='watermark', help='Embed a watermark inside the encrypted payload')
    parser.add_argument('--visible', '--vwm', dest='visible_watermark', help='Add a visible comment watermark at the top of the output file')
    parser.add_argument('--decrypt', action='store_true', help='Decrypt mode (not yet implemented)')

    args = parser.parse_args()

    if args.decrypt:
        print("Decryption is not yet implemented for the recursive compact mode.")
        print("Please use the original source code or encrypt with --readable for future decryption.")
        sys.exit(1)

    # Determine marshal mode
    use_marshal = True
    if hasattr(args, 'use_marshal') and args.use_marshal is not None:
        use_marshal = args.use_marshal
    if args.func:
        use_marshal = True

    if args.fast:
        min_ops, max_ops = 2, 4
    else:
        min_ops, max_ops = args.min_ops, args.max_ops

    encrypt_python_file(
        input_file=args.input,
        output_file=args.output,
        depth=args.depth,
        key=args.key,
        min_ops=min_ops,
        max_ops=max_ops,
        compile_pyc=args.compile,
        compact=not args.readable,
        use_marshal=use_marshal,
        watermark=args.watermark,
        visible_watermark=args.visible_watermark
    )


if __name__ == "__main__":
    execute_cli()
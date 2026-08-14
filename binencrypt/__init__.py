"""
binencrypt - Recursive Python Code Encryption Tool
Version: 2.7.6
"""

from .core import (
    CryptoVault,
    RecursiveVault,
    encrypt_python_file,
    decrypt_python_file,
    execute_cli,
    __version__,
    __author__
)

# Compatibility aliases (legacy classes removed; keep only the new ones)
main = execute_cli

__all__ = [
    'CryptoVault',
    'RecursiveVault',
    'encrypt_python_file',
    'decrypt_python_file',
    'execute_cli',
    'main',
    '__version__',
    '__author__'
]
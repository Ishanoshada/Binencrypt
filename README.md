
# 🔐 binencrypt

**Recursive Python Code Encryption & Obfuscation**  
*Version 2.7.2*

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`binencrypt` is a powerful tool that applies **multiple recursive encryption layers** to your Python source code. Each layer wraps the previous one with a unique sequence of encoding, compression, and serialization operations. The final output is a self‑executing Python script that unwraps all layers at runtime and runs your original code.

Designed for **code obfuscation** and **intellectual property protection** – not for cryptographic security. Use it to make reverse‑engineering harder, not impossible.

---

## ✨ Features

- **🔁 Recursive Layering** – Each layer encrypts the entire output of the previous layer (depth up to 10+).
- **🧩 Dynamic Operations** – Each layer picks a random sequence of 5–15 operations (e.g., base64, gzip, marshal, hex, etc.) based on a master key.
- **⚡ Marshal Optimisation** – Compiles your source to bytecode and serialises it with `marshal`, reducing final script size by 30‑50%.
- **📦 Compact Output** – Generates a single‑line Python script (or a readable multi‑line version) that is easy to distribute.
- **🎯 Deterministic** – Same key + depth yields the same encrypted output (useful for reproducible builds).
- **📁 File Support** – Encrypt any Python file; output is a standalone script.
- **⚙️ Customisable** – Control depth, operations per layer, and use of marshal.

---

## 📦 Installation

```bash
# Install from PyPI (soon)
pip install binencrypt

# Or install directly from source
git clone https://github.com/ishanoshada/binencrypt.git
cd binencrypt
pip install -e .
```

---

## 🚀 Quick Start

Encrypt a Python file with **10 recursive layers**:

```bash
binencrypt -i my_script.py -o encrypted.py --depth 10
```

Run the encrypted script:

```bash
python encrypted.py
```

The output will execute the original `my_script.py` code after decrypting all 10 layers.

---

## 🛠 Command Line Options

| Argument | Description |
|----------|-------------|
| `-i, --input` | Input Python file (required) |
| `-o, --output` | Output file path (auto‑generated if not given) |
| `--depth` | Number of recursive encryption layers (default: 1) |
| `--key` | Master encryption key (auto‑generated if omitted) |
| `--min-ops` | Minimum operations per layer (default: 3) |
| `--max-ops` | Maximum operations per layer (default: 5) |
| `--fast` | Fast mode: `min-ops=2, max-ops=4` |
| `--marshal` | Use marshal mode (compiles source to bytecode) – **default** |
| `--no-marshal` | Disable marshal mode (encrypts source as text) |
| `--func` | Alias for `--marshal` |
| `--readable` | Generate multi‑line readable output (not compact) |
| `--compile` | Compile the output to `.pyc` (using `py_compile`) |
| `--decrypt` | (Not yet fully implemented) |

---

## 📝 Examples

### Basic encryption with default settings (3‑5 ops per layer, marshal on)

```bash
binencrypt -i app.py -o app.enc.py --depth 8
```

### Use a specific key

```bash
binencrypt -i app.py -o app.enc.py --depth 10 --key "my-super-secret-2024"
```

### Faster encryption (fewer operations per layer)

```bash
binencrypt -i app.py -o app.enc.py --depth 10 --fast
```

### Generate human‑readable (non‑compact) output

```bash
binencrypt -i app.py -o app.enc.py --depth 5 --readable
```

### Disable marshal mode (larger output, but easier to inspect)

```bash
binencrypt -i app.py -o app.enc.py --depth 5 --no-marshal
```

---

## 📊 Performance & File Size

| Depth | Mode | Size (approx) | Time (approx) |
|-------|------|---------------|---------------|
| 5     | marshal | 300 KB | 0.5 s |
| 5     | source  | 500 KB | 0.7 s |
| 10    | marshal | 1.8 MB | 1.5 s |
| 10    | source  | 4.5 MB | 4.0 s |
| 15    | marshal | 6 MB   | 6 s   |

*Measured on a small 100‑line script. Actual results vary with code size and system.*

---

## ⚠️ Security Disclaimer

**binencrypt is an obfuscation tool, not a cryptographic security solution.**  

- The encryption is **reversible** – anyone with the key and knowledge of the algorithm can recover the source.
- It is designed to **hinder casual reverse‑engineering**, not to protect against determined attackers.
- Do **not** use it to store passwords, API keys, or other sensitive data.
- For real security, use established libraries like `cryptography` or `Fernet`.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**K.A. Ishan Oshada**  
[GitHub](https://github.com/ishanoshada) · [Email](mailto:ic31908@gmail.com)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📚 More Information

- **How it works**: Each layer uses a deterministic random sequence of operations derived from the master key and layer index. The innermost layer is either the original source code (or compiled bytecode). The outer layers encrypt that payload, producing a nested structure that unwraps at runtime.
- **Why use marshal?** `marshal.dumps()` of a compiled code object is significantly smaller than the source code string, and it avoids the `compile()` overhead at runtime, making decryption faster.

---

Happy encrypting! 🚀

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# Read README.md if it exists
readme_path = os.path.join(here, "README.md")
if os.path.exists(readme_path):
    with codecs.open(readme_path, encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "BINENCRYPT - Professional Python Code Encryption Tool"

VERSION = "2.7.2"
DESCRIPTION = 'Professional Python code encryption with multi-layer deep vault methodology'

setup(
    name="binencrypt",
    version=VERSION,
    author="K.A. ISHAN OSHADA",
    author_email="ic31908@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'binencrypt=binencrypt:execute_cli',  # Updated to use execute_cli
        ],
    },
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Obfuscation",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=[
        'binencrypt', 'cryptography', 'encryption', 'decryption',
        'python-obfuscation', 'code-encryption', 'security-tool',
        'deep-vault', 'multi-layer-encryption', 'code-protection'
    ],
    project_urls={
        'Source': 'https://github.com/yourusername/binencrypt',
        'Bug Reports': 'https://github.com/yourusername/binencrypt/issues',
        'Documentation': 'https://github.com/yourusername/binencrypt/wiki',
    },
)
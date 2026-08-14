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
    long_description = "Recursive Python code encryption tool with multi-layer obfuscation."

VERSION = "2.7.6"
DESCRIPTION = "Recursive Python code encryption with marshal optimisation and watermarking."

setup(
    name="binencrypt",
    version=VERSION,
    author="K.A. ISHAN OSHADA",
    author_email="ic31908@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'binencrypt=binencrypt:execute_cli',
        ],
    },
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
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
        'binencrypt', 'encryption', 'obfuscation', 'code-protection',
        'python-obfuscator', 'security-tools', 'marshal',
        'recursive-encryption', 'watermarking', 'cli-tool'
    ],
    project_urls={
        'Source': 'https://github.com/ishanoshada/binencrypt',
        'Bug Reports': 'https://github.com/ishanoshada/binencrypt/issues',
        'Documentation': 'https://github.com/ishanoshada/binencrypt#readme',
    },
)
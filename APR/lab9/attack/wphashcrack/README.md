# WordPress Hash Cracker

A multithreaded WordPress password hash cracker for `$wp$2y$` format hashes.

## Description

WordPress uses a three-step password hashing process:
1. HMAC-SHA384 with 'wp-sha384' key for domain separation
2. Base64 encoding of the HMAC output
3. bcrypt on the base64-encoded result

This tool cracks these hashes using wordlist-based brute force attacks with optional multiprocessing support.

## Requirements

- Python 3.6+
- bcrypt
- tqdm

## Installation

```bash
pip install bcrypt tqdm
```

## Usage

Basic usage:
```bash
./wphashcrack.py -H '$wp$2y$10$...' -w wordlist.txt
```

With multiple workers:
```bash
./wphashcrack.py -H '$wp$2y$10$...' -w rockyou.txt -t 4
```

Use all CPU cores:
```bash
./wphashcrack.py -H '$wp$2y$10$...' -w rockyou.txt -t 0
```

### Options

- `-H, --hash`: WordPress hash to crack (required)
- `-w, --wordlist`: Path to password wordlist file (required)
- `-v, --verbose`: Verbose output
- `-t, --workers`: Number of parallel workers (default: 1, use 0 for CPU count)

## Legal Notice

This tool is intended for:
- Authorized security testing and penetration testing
- CTF competitions
- Educational purposes
- Password recovery with proper authorization

Unauthorized access to computer systems is illegal. Only use this tool on systems you own or have explicit permission to test.

## Disclaimer

This project was vibe coded with claude sonnet 4.5.

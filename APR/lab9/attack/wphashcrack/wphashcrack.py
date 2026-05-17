#!/usr/bin/env python3
"""
WordPress Password Hash Cracker
Cracks WordPress hashes in the format: $wp$2y$...
These are HMAC-SHA384 + base64 pre-hashed bcrypt hashes.
"""

import bcrypt
import hashlib
import hmac
import base64
import argparse
import sys
import multiprocessing
from typing import Optional, Tuple
from tqdm import tqdm


def hash_password_wordpress(password: str) -> bytes:
    """
    Hash a password using HMAC-SHA384 and base64 encoding (WordPress pre-hash step).

    WordPress uses HMAC-SHA384 with 'wp-sha384' as the key for domain separation,
    then base64 encodes the result before passing to bcrypt.

    Args:
        password: The plaintext password to hash

    Returns:
        The base64-encoded HMAC-SHA384 hash as bytes
    """
    # HMAC-SHA384 with 'wp-sha384' key for domain separation
    hmac_hash = hmac.new(
        b'wp-sha384',
        password.strip().encode('utf-8'),
        hashlib.sha384
    ).digest()

    # Base64 encode the HMAC output
    return base64.b64encode(hmac_hash)


def check_password_worker(args: Tuple[str, str]) -> Optional[str]:
    """
    Worker function for multiprocessing. Checks a single password against a hash.

    Args:
        args: Tuple of (password, wp_hash)

    Returns:
        The password if it matches, None otherwise
    """
    password, wp_hash = args
    if verify_wordpress_hash(password, wp_hash):
        return password
    return None


def verify_wordpress_hash(password: str, wp_hash: str) -> bool:
    """
    Verify a password against a WordPress hash.

    WordPress uses a three-step process:
    1. HMAC-SHA384 hash the password with 'wp-sha384' key
    2. Base64 encode the HMAC output
    3. Use bcrypt on the base64-encoded result

    Args:
        password: The plaintext password to test
        wp_hash: The WordPress hash in format $wp$2y$...

    Returns:
        True if the password matches, False otherwise
    """
    # WordPress hash format: $wp$2y$rounds$salt+hash
    # We need to extract the bcrypt portion (everything after $wp)
    if not wp_hash.startswith('$wp$'):
        raise ValueError("Invalid WordPress hash format. Must start with $wp$")

    # Extract the bcrypt hash (remove the $wp prefix, keep the $ before 2y)
    bcrypt_hash = wp_hash[3:]  # Remove '$wp' but keep the leading $

    # Hash the password with SHA-384 first
    prehashed = hash_password_wordpress(password)

    # Then verify against the bcrypt hash
    try:
        return bcrypt.checkpw(prehashed, bcrypt_hash.encode('utf-8'))
    except Exception as e:
        print(f"Error verifying hash: {e}", file=sys.stderr)
        return False


def crack_hash(wp_hash: str, wordlist_path: str, verbose: bool = False, workers: int = 1) -> Optional[str]:
    """
    Attempt to crack a WordPress hash using a wordlist.

    Args:
        wp_hash: The WordPress hash to crack
        wordlist_path: Path to the wordlist file
        verbose: Print progress information
        workers: Number of parallel workers to use

    Returns:
        The cracked password if found, None otherwise
    """
    try:
        # Count total lines for progress bar
        print("[*] Counting wordlist entries...", file=sys.stderr)
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)

        print(f"[*] Found {total_lines:,} passwords in wordlist\n", file=sys.stderr)

        # Single-threaded mode
        if workers == 1:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                pbar = tqdm(f, total=total_lines, unit='try',
                           desc='Cracking',
                           bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

                for line in pbar:
                    password = line.rstrip('\n\r')

                    if verify_wordpress_hash(password, wp_hash):
                        pbar.close()
                        return password

            return None

        # Multi-threaded mode
        print(f"[*] Using {workers} parallel workers\n", file=sys.stderr)

        # Read all passwords into memory
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.rstrip('\n\r') for line in f]

        # Create tasks (password, hash) tuples
        tasks = [(pwd, wp_hash) for pwd in passwords]

        # Process with parallel workers using Pool.imap_unordered for real-time progress
        found_password = None
        with multiprocessing.Pool(processes=workers) as pool:
            # Progress bar
            pbar = tqdm(total=total_lines, unit='try',
                       desc='Cracking',
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

            # Process results as they complete
            try:
                for result in pool.imap_unordered(check_password_worker, tasks, chunksize=1):
                    pbar.update(1)
                    if result:
                        found_password = result
                        pbar.close()
                        pool.terminate()  # Stop all workers immediately
                        break
            finally:
                pbar.close()
                pool.close()
                pool.join()

        return found_password

    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading wordlist: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='WordPress Password Hash Cracker - Cracks $wp$2y$ hashes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -H '$wp$2y$10$7vt1aeAJ8tWXxrM2hXXw6.5LSKc.QwZ6eL2VhTbE8o2DfLS/PKoYS' -w wordlist.txt
  %(prog)s -H '$wp$2y$10$...' -w rockyou.txt -v
  %(prog)s -H '$wp$2y$10$...' -w rockyou.txt -t 4    # Use 4 parallel workers
  %(prog)s -H '$wp$2y$10$...' -w rockyou.txt -t 0    # Use all CPU cores
        '''
    )

    parser.add_argument('-H', '--hash', required=True,
                        help='WordPress hash to crack (format: $wp$2y$...)')
    parser.add_argument('-w', '--wordlist', required=True,
                        help='Path to password wordlist file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output (show progress)')
    parser.add_argument('-t', '--workers', type=int, default=1,
                        help='Number of parallel workers (default: 1, use 0 for CPU count)')

    args = parser.parse_args()

    # Validate hash format
    if not args.hash.startswith('$wp$'):
        print("Error: Hash must start with $wp$", file=sys.stderr)
        sys.exit(1)

    # Handle workers parameter
    workers = args.workers
    if workers == 0:
        workers = multiprocessing.cpu_count()
    elif workers < 0:
        print("Error: Number of workers must be >= 0", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Starting WordPress hash cracker")
    print(f"[*] Target hash: {args.hash}")
    print(f"[*] Wordlist: {args.wordlist}")
    if workers > 1:
        print(f"[*] Workers: {workers}")
    print(f"[*] Beginning brute-force attack...\n")

    result = crack_hash(args.hash, args.wordlist, args.verbose, workers)

    if result:
        print(f"\n[+] SUCCESS! Password found: {result}")
        return 0
    else:
        print(f"\n[-] Password not found in wordlist")
        return 1


if __name__ == '__main__':
    sys.exit(main())

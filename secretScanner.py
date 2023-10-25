import argparse
import math
import os
import re
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO)

keyword_patterns = [r'\bAPI_KEY\b', r'\bSECRET\b', r'\bPASSWORD\b', r'\bTOKEN\b']

def calculate_entropy(s):
    """
    Calculate the entropy of a string
    :param s: string
    :return: entropy
    """
    if not s:
        return 0
    length = len(s)
    prob = [freq / length for _, freq in Counter(s).items()]
    entropy = -sum(p * math.log2(p) for p in prob)
    return entropy

def scan_directory(directory, keyword_search=True, entropy_search=True, threshold=4.4, min_length=8, max_length=40):
    """
    Scan a directory for potential secrets based on entropy and keyword matching.
    :param directory: The directory to scan.
    :param keyword_search: Enable keyword-based secret search.
    :param entropy_search: Enable entropy-based secret search.
    :param threshold: Entropy threshold for considering a string as a potential secret.
    :param min_length: Minimum length of a word to consider for entropy calculation.
    :param max_length: Maximum length of a word to consider for entropy calculation.
    :return: A list of results.
    """
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', errors='replace') as f:
                    for line_num, line in enumerate(f, 1):
                        # Keyword search
                        if keyword_search:
                            for pattern in keyword_patterns:
                                if re.search(pattern, line, re.IGNORECASE):
                                    result = {
                                        'type': 'Keyword',
                                        'file': filepath,
                                        'line_number': line_num,
                                        'content': line.strip()
                                    }
                                    results.append(result)
                                    logging.info(f"[Keyword][{filepath}:{line_num}] Suspect: {line.strip()}")
                                    break  # If a keyword is found, move to the next line

                        # Entropy search
                        if entropy_search:
                            for word in line.split():
                                if min_length <= len(word) <= max_length and calculate_entropy(word) > threshold:
                                    result = {
                                        'type': 'Entropy',
                                        'file': filepath,
                                        'line_number': line_num,
                                        'content': word
                                    }
                                    results.append(result)
                                    logging.info(f"[Entropy][{filepath}:{line_num}] Suspect: {word}")

            except Exception as e:
                logging.error(f"Error reading file {filepath}. Reason: {e}")

    return results

if __name__ == "__main__":
    """
    Usage: python app.py <directory> [options]
    """
    parser = argparse.ArgumentParser(description="Scan a directory for potential secrets based on entropy and keyword matching.")

    parser.add_argument("directory", type=str, help="The directory to scan.")
    parser.add_argument("--disable-keyword-search", action="store_true", help="Disable keyword-based secret search.")
    parser.add_argument("--disable-entropy-search", action="store_true", help="Disable entropy-based secret search.")
    parser.add_argument("--threshold", type=float, default=4.5, help="Entropy threshold for considering a string as a potential secret.")
    parser.add_argument("--min_length", type=int, default=8, help="Minimum length of a word to consider for entropy calculation.")
    parser.add_argument("--max_length", type=int, default=128, help="Maximum length of a word to consider for entropy calculation.")
    
    args = parser.parse_args()
    scan_directory(args.directory, not args.disable_keyword_search, not args.disable_entropy_search, args.threshold, args.min_length, args.max_length)

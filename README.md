# Secret-Scanner

`Secret-Scanner` is a script designed to identify potential hard-coded secrets such as passwords or API keys within a specified directory. Utilizing keyword matching and entropy analysis, it seeks to flag strings that may represent sensitive data.

## Table of Contents
1. [Features](#features)
2. [Usage](#usage)
3. [Optional Arguments](#optional-arguments)
4. [Output](#output)

## Features

The core functionality of `Secret-Scanner` revolves around the following features:

- **Keyword Matching**: Spotting common keywords associated with sensitive data, e.g., "PASSWORD", "API_KEY", "SECRET", and "TOKEN".

- **Entropy Analysis**: Employing string entropy analysis to identify potential secrets, as high entropy often indicates encrypted or randomized data.

- **Configurable Parameters**: Providing the ability to specify the scanning directory, toggle keyword or entropy scanning on or off, and adjust parameters like entropy threshold and word length for analysis.

- **Logging**: Logging suspected secrets along with their file paths and line numbers for further review, as well as logging file reading errors.

## Usage

1. Clone or download the script.
2. Open a terminal and navigate to the script's directory.
3. Run the command:
   ```bash
   python3 secretScanner.py <directory_to_scan> [optional_arguments]
   ```
   Replace `<directory_to_scan>` with the directory path.

### Optional Arguments

- `--disable-keyword-search`: Disables keyword-based search.
- `--disable-entropy-search`: Disables entropy-based search.
- `--threshold`: Sets the entropy threshold (default 4.5).
- `--min_length`: Sets the minimum word length for entropy calculation (default 8).
- `--max_length`: Sets the maximum word length for entropy calculation (default 128).

Example:
```bash
python3 secretScanner.py /path/to/directory --disable-keyword-search --threshold 5.0
```

## Output

The script outputs the suspected secrets to the console (or a log file) in the following format:
```plaintext
[Keyword][file_path:line_number] Suspect: suspected_secret
[Entropy][file_path:line_number] Suspect: suspected_secret
```

# BibTeX to Mbox Converter

A command-line utility to convert a BibTeX (`.bib`) file into an `mbox` email archive. Each BibTeX entry becomes an email message, making your reference library searchable and readable in any standard email client.

[![PyPI version](https://badge.fury.io/py/bibtex-to-mbox.svg)](https://badge.fury.io/py/bibtex-to-mbox) <!-- You can add this badge after publishing -->

## Features

- **Author as Sender**: The `author` field becomes the email's "From" address.
- **Title as Subject**: The `title` field becomes the email's "Subject".
- **Abstract as Body**: The `abstract` field becomes the main body of the email.
- **Link Extraction**: Automatically appends `url` and `doi` links to the end of the email body.
- **LaTeX to Text**: Converts common LaTeX commands (e.g., `{\'e}`, `\textit{...}`, `{...}`) into clean, readable plain text.
- **Progress Bar**: Shows a progress bar via `tqdm` when processing large files.

## Installation

You can install the tool directly from PyPI using pip:

```bash
pip install bibtex-to-mbox
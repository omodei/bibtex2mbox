# BibTeX to Mbox Converter

A command-line utility to convert a BibTeX (`.bib`) file into an `mbox` email archive. Each BibTeX entry becomes an email message, making your reference library searchable and readable in any standard email client.

[![PyPI version](https://badge.fury.io/py/bibtex2mbox.svg)](https://badge.fury.io/py/bibtex2mbox) <!-- You can add this badge after publishing -->

## Features

- **Author as Sender**: The `author` field becomes the email's "From" address.
- **Title as Subject**: The `title` field becomes the email's "Subject".
- **Abstract as Body**: The `abstract` field becomes the main body of the email.
- **Link Extraction**: Automatically appends `url` and `doi` links to the end of the email body.
- **LaTeX to Text**: Converts common LaTeX commands (e.g., `{\'e}`, `\textit{...}`, `{...}`) into clean, readable plain text.
- **Progress Bar**: Shows a progress bar via `tqdm` when processing large files.

## Installation

You can install the tool directly from PyPI using pip:

```bash pip install bibtex2mbox```

## Usage

The script is a command-line tool. You must provide the path to your input BibTeX file and the desired path for the output mbox file.
You can download a specific BibTeX file from the ADS site, selecting "BibTeX-ABS" as download option.

### Command-Line Syntax

```bash 
bibtex2mbox [INPUT_BIB_FILE] [OUTPUT_MBOX_FILE]
```

### Example

You can use any BibTeX file, as long as it is in the correct format. For example you can download one from the [ADS library](https://ui.adsabs.harvard.edu). **Make sure you also export the abstract by selecting BibTeX ABS format from the menu**. Unfortunately ADS allows only 500 entries at the time, so you will have to download large libraries with multiple downloads. The good news is that *bibtex2mbox* will add them (if you keep the same mbox output), resulting in one big mbox.

Let's say you have a file named my_library.bib in your current directory. To convert it into an archive named my_archive.mbox, you would run:

```bash
bibtex2mbox my_library.bib my_archive.mbox
```
You will see the following output as the tool processes your file:

```txt
Found 150 entries in 'my_library.bib'. Starting conversion...
Converting entries: 100%|██████████| 150/150 [00:00<00:00, 850.12entry/s]

Successfully converted 150 entries into 'my_archive.mbox'.
```
The file my_archive.mbox will be created in your current directory.

## Importing the Mbox File into Email Clients

Here are instructions for common clients.

### Mozilla Thunderbird (Recommended)

1.  **Install Add-on**: In Thunderbird, go to `Tools > Add-ons and Themes`, search for and install `ImportExportTools NG`, then restart.
2.  **Import**: Right-click on **Local Folders**, navigate to `ImportExportTools NG > Import mbox file`, choose "Import directly one or more mbox files", and select your `.mbox` file.

### Apple Mail

1.  **Open Import Wizard**: Go to `File > Import Mailboxes...`.
2.  **Select Format**: Choose **"Files in mbox format"** and click "Continue".
3.  **Choose File**: Navigate to and select your `.mbox` file. It will appear in a new "Import" folder under "On My Mac".

### Microsoft Outlook & Webmail (Gmail)

These clients do not directly support mbox imports. The recommended method is to use Thunderbird as an intermediary:

1.  Import the mbox into Thunderbird's "Local Folders".
2.  Set up your Outlook/Gmail account in Thunderbird via IMAP.
3.  Drag and drop the messages from the local mbox folder to a folder in your Outlook/Gmail account. Thunderbird will upload them.

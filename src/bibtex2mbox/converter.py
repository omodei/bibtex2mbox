#!/usr/bin/env python

import bibtexparser
import mailbox
from email.message import EmailMessage
from email.utils import formatdate, formataddr
import uuid
from tqdm import tqdm
from pylatexenc.latex2text import LatexNodes2Text
import datetime
import time

def get_publication_date_timestamp(entry):
    """
    Tries to parse year, month, and day from a BibTeX entry.
    Returns a Unix timestamp for the email header.
    Falls back to the current time if parsing fails or data is missing.
    """
    # BibTeX months can be numbers or 3-letter abbreviations.
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4, # etc for full names
    }

    try:
        # Year is required. If not present or not a number, fallback.
        year_str = entry.get('year')
        if not year_str or not year_str.isdigit():
            return time.time()  # Fallback to now
        year = int(year_str)

        # Month is optional. Default to January (1).
        month_str = entry.get('month', '1').lower()
        if month_str.isdigit():
            month = int(month_str)
        else:
            # Look up the month name; default to 1 if not found.
            month = month_map.get(month_str, 1)

        # Day is optional. Default to the 1st of the month.
        day = int(entry.get('day', '1'))
        
        # Create a datetime object. This will raise ValueError for invalid dates
        # (e.g., Feb 30), which is caught by the except block.
        dt = datetime.datetime(year, month, day, 12, 0, 0) # Use noon to avoid timezone issues
        
        return dt.timestamp()

    except (ValueError, TypeError):
        # If any conversion fails (e.g., year="forthcoming"), use current time.
        return time.time()


def create_mbox_from_bibtex(bibtex_path, mbox_path):
    """
    Parses a BibTeX file, converts LaTeX to plain text, and creates an mbox file,
    displaying a progress bar during the process.
    """
    latex_converter = LatexNodes2Text()

    def latex_to_text(latex_string):
        if not latex_string: return ""
        try:
            plain_text = latex_converter.latex_to_text(latex_string)
            return " ".join(plain_text.split())
        except Exception:
            # In case of pylatexenc error, return original string (minus braces)
            return latex_string.replace("{", "").replace("}", "")

    try:
        with open(bibtex_path, 'r', encoding='utf-8') as bibfile:
            bib_database = bibtexparser.load(bibfile)
    except FileNotFoundError:
        print(f"Error: The file '{bibtex_path}' was not found.")
        return

    mbox_archive = mailbox.mbox(mbox_path)
    mbox_archive.lock()
    print(f"Found {len(bib_database.entries)} entries in '{bibtex_path}'. Starting conversion...")
    
    try:
        for entry in tqdm(bib_database.entries, desc="Converting entries", unit="entry"):
            sender_name = latex_to_text(entry.get('author', 'Unknown Author'))
            subject = latex_to_text(entry.get('title', 'No Title'))
            body = latex_to_text(entry.get('abstract', 'No abstract available.'))
            
            links = []
            if 'url' in entry: links.append(f"URL: {entry['url']}")
            if 'doi' in entry: links.append(f"DOI: https://doi.org/{entry['doi']}")
            if links: body += "\n\n---\n" + "\n".join(links)
            
            # --- THIS IS THE MODIFIED SECTION ---
            # 1. Get the publication date timestamp from our new function
            publication_timestamp = get_publication_date_timestamp(entry)

            # 2. Create the message
            msg = EmailMessage()
            msg['From'] = formataddr((sender_name, 'authors@bibtex.local'))
            msg['Subject'] = subject
            msg['To'] = 'bibtex-archive@local.host'
            
            # 3. Use the publication timestamp to format the Date header
            msg['Date'] = formatdate(publication_timestamp)
            
            msg['Message-ID'] = f"<{uuid.uuid4()}@bibtex-parser.local>"
            msg.set_content(body)
            # --- END OF MODIFICATION ---

            mbox_archive.add(msg)
    finally:
        mbox_archive.flush()
        mbox_archive.unlock()
        mbox_archive.close()
    print(f"\nSuccessfully converted {len(bib_database.entries)} entries into '{mbox_path}'.")
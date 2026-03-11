import argparse
from .converter import create_mbox_from_bibtex

def main():
    parser = argparse.ArgumentParser(
        description="Convert a BibTeX file (with LaTeX commands) into an mbox mail archive.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "bibtex_file",
        help="Path to the input BibTeX (.bib) file."
    )
    parser.add_argument(
        "mbox_file",
        help="Path for the output mbox (.mbox) file."
    )
    
    args = parser.parse_args()
    
    create_mbox_from_bibtex(args.bibtex_file, args.mbox_file)

if __name__ == "__main__":
    main()
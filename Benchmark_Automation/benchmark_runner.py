"""
Benchmark Runner - Milestone 4
Automatic Pilot Runner
"""



import logging
import time
from datetime import datetime
from pathlib import Path

from config import (
    INPUT_FOLDER,
    SUPPORTED_EXTENSIONS,
    LOG_FILE,
    WAIT_BETWEEN_EMAILS
)

from email_sender import send_invoice


# -------------------------------------------------
# Configure Logger
# -------------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -------------------------------------------------
# Discover PDF Files
# -------------------------------------------------

def discover_pdfs():
    """
    Return all PDF files sorted alphabetically.
    """

    files = []

    for file in Path(INPUT_FOLDER).iterdir():

        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ):
            files.append(file)

    return sorted(files)


# -------------------------------------------------
# Run Benchmark
# -------------------------------------------------

def run_benchmark(pdf_list):

    total = len(pdf_list)

    logger.info("=" * 60)
    logger.info("Invoice Benchmark Started")
    logger.info("=" * 60)
    logger.info(f"Start Time : {datetime.now()}")
    logger.info(f"Input Folder : {INPUT_FOLDER}")
    logger.info(f"Total PDFs : {total}")
    logger.info("=" * 60)

    print()

    for index, pdf in enumerate(pdf_list, start=1):

        print("=" * 60)
        print(f"[{index}/{total}] Processing : {pdf.name}")
        print("=" * 60)

        success = send_invoice(pdf)

        if success:

            logger.info(f"SUCCESS | {pdf.name}")

            print("✅ Email sent successfully.")

        else:

            logger.error(f"FAILED | {pdf.name}")

            print("❌ Email sending failed.")

        if index != total:

            print(f"\nWaiting {WAIT_BETWEEN_EMAILS} seconds...\n")

            time.sleep(WAIT_BETWEEN_EMAILS)

    logger.info("=" * 60)
    logger.info("Benchmark Completed")
    logger.info("=" * 60)

    print("\n🎉 Benchmark Completed Successfully.")


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():

    pdfs = discover_pdfs()

    print("=" * 60)
    print(" AI Invoice Benchmark Runner ")
    print("=" * 60)

    print(f"\nFound {len(pdfs)} PDF files.\n")

    for i, pdf in enumerate(pdfs, start=1):

        print(f"{i:03d}. {pdf.name}")

    print()

    answer = input("Start benchmark? (y/n): ").strip().lower()

    if answer != "y":

        print("\nBenchmark cancelled.")

        return

    run_benchmark(pdfs)


if __name__ == "__main__":
    main()
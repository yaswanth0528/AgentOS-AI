
from pathlib import Path
from typing import Any

from pypdf import PdfReader


def pdf_reader_tool(
    file_path: str,
    max_pages: int = 20
) -> dict[str, Any]:
    """
    Extract text from a PDF file.
    """

    if not file_path or not file_path.strip():
        raise ValueError("PDF file path cannot be empty.")

    if not 1 <= max_pages <= 100:
        raise ValueError("max_pages must be between 1 and 100.")

    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise ValueError("The supplied path must point to a PDF file.")

    if path.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("PDF file size cannot exceed 20 MB.")

    try:
        reader = PdfReader(str(path))

        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")

        total_pages = len(reader.pages)
        pages_to_read = min(total_pages, max_pages)

        extracted_pages = []

        for page_number in range(pages_to_read):
            page_text = reader.pages[page_number].extract_text() or ""

            extracted_pages.append({
                "page": page_number + 1,
                "text": page_text
            })

        full_text = "\n".join(
            page["text"] for page in extracted_pages
        )

        return {
            "status": "success",
            "file_name": path.name,
            "total_pages": total_pages,
            "pages_read": pages_to_read,
            "text": full_text,
            "pages": extracted_pages
        }

    except Exception as error:
        if isinstance(error, ValueError):
            raise

        raise RuntimeError(
            f"Failed to read PDF: {error}"
        ) from error

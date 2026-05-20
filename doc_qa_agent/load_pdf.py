import base64
import os


def load_pdf(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")

    with open(path, "rb") as f:
        raw = f.read()

    size_kb = len(raw) / 1024
    # PDFs average ~50KB per page — rough estimate only
    page_estimate = max(1, round(len(raw) / 51_200))

    print(f"  Loaded: {os.path.basename(path)}")
    print(f"  Size:   {size_kb:.1f} KB")
    print(f"  Pages:  ~{page_estimate} (estimated)")

    return base64.b64encode(raw).decode("utf-8")

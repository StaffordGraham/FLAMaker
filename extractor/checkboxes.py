from pypdf import PdfReader

def extract_form_fields(path: str) -> dict:
    reader = PdfReader(path)
    fields = reader.get_fields()
    return fields or {}

# Placeholder for scanned checkbox detection
def detect_checkboxes(path: str) -> dict:
    # For now, just return empty info
    return {}

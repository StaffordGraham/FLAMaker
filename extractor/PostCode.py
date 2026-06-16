import re
from pdf2image import convert_from_path
import pytesseract



def extract_respondent_address_block(clean_text: str) -> str:
    """
    Extracts the block from 'Respondent’s details' up to 'Postcode' + postcode line + FL401.
    """
    start = clean_text.find("Respondent’s details")
    if start == -1:
        return ""

    # from start to FL401
    end = clean_text.find("FL401", start)
    if end == -1:
        return ""

    return clean_text[start:end + len("FL401")]


def remove_fl401(block: str) -> str:
    """
    Removes any form of 'FL401' from the block.
    """
    return block.replace("FL401", "").strip()

def get_last_line(block: str) -> str:
    """
    Returns the last non-empty line from the block.
    """
    lines = [line.strip() for line in block.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return ""
    return lines[-1]

def remove_spaces_from_postcode(line: str) -> str:
    """
    Removes all spaces from the postcode line.
    """
    return "".join(ch for ch in line if ch != " ")

def insert_space_in_postcode(compact: str) -> str:
    """
    Inserts a space between the 3rd and 4th character.
    Assumes length >= 4.
    """
    if len(compact) < 4:
        return compact
    return compact[:3] + " " + compact[3:]



def get_respondent_postcode_from_clean_text (clean_text: str) -> str:
    block = extract_respondent_address_block(clean_text)
    block_no_fl401 = remove_fl401(block)
    last_line = get_last_line(block_no_fl401)
    compact = remove_spaces_from_postcode(last_line)
    postcode = insert_space_in_postcode(compact)
    return postcode
if __name__ == "__main__":
    pdf_path = r"C:\Users\sgcam\Projects\FL401_Extractor\FL401_Ellen_Champion_Flat.pdf"

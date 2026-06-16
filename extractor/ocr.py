from pdf2image import convert_from_path
import fitz
import pytesseract
import numpy as np
import cv2
import pyperclip
import re
from PIL import Image
import io
from extractor.PostCode import get_respondent_postcode_from_clean_text


def ocr_file_to_text(pdf_path: str) -> str:
    """
    Takes a PDF file path, performs OCR, returns raw_text.
    Does nothing else.
    """
    pages = convert_from_path(pdf_path)
    texts = []
    for page in pages:
        text = pytesseract.image_to_string(page)
        texts.append(text)
    return "\n".join(texts)



def clean_ocr_text(raw_text: str) -> str:
    """
    Takes raw OCR text and returns cleaned text.
    Keep this as simple or as rich as you like.
    """
    text = raw_text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def extract_respondent_block(path) -> str:
    """
    Extracts the full 'Respondent’s details' block from the OCR text.
    Returns the block as a string, or "" if not found.
    """
    raw_text = extract_text_ocr(path)

    # 2. Clean text
    cleaned = clean_text_ocr(raw_text)
    text = clean_text_ocr_fl401(cleaned)

    pattern = (
        r"Respondent’s details\s*"      # start marker
        r"(.*?)"                        # everything in between
        r"FL401"                        # end marker
    )

    m = re.search(pattern, text, flags=re.DOTALL)
    if not m:
        return ""

    return m.group(0)  # or m.group(1) if you want to exclude the headings
    


def extract_postcode_from_respondent_block(ocr_text: str) -> str:
    # -------------------------
    # STEP 1 — Extract block
    # -------------------------
    step1_block = extract_respondent_block(ocr_text)

    # -------------------------
    # STEP 2 — Remove FL401
    # -------------------------
    step2_cleaned = re.sub(r"F\s*L\s*4\s*0\s*1", "", step1_block, flags=re.IGNORECASE).strip()

    # -------------------------
    # STEP 3 — Capture last non-empty line
    # -------------------------
    lines = [line.strip() for line in step2_cleaned.splitlines()]
    lines = [line for line in lines if line]  # remove empty lines
    if not lines:
        return ""
    step3_last_line = lines[-1]

    # -------------------------
    # STEP 4 — Normalise postcode
    # -------------------------
    cleaned = "".join(ch for ch in step3_last_line if ch.isalnum()).upper()
    if len(cleaned) < 5:
        return ""
    step4_postcode = cleaned[:-3] + " " + cleaned[-3:]

    return step4_postcode


# Helper from earlier
def extract_respondent_block(text: str) -> str:
    pattern = (
        r"Respondent’s details\s*"
        r"(.*?)"
        r"FL401"
    )
    m = re.search(pattern, text, flags=re.DOTALL)
    if not m:
        return ""
    return m.group(0)


def convert_pdf_to_images_pymupdf(path):
    doc = fitz.open(path)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = pix.tobytes("png")
        images.append(img)

    return images


def clean_text_ocr(text: str) -> str:
    """
    Aggressive cleaning for OCR‑extracted FL401 text.
    Removes noise, fixes spacing, strips artefacts.
    """

    # 1. Remove common OCR garbage characters
    text = re.sub(r"[|~•■□▪◦●◆◇▶◀■□✓✔✗✘]", " ", text)

    # 2. Remove long sequences of punctuation or symbols
    text = re.sub(r"[-_=]{3,}", " ", text)

    # 3. Remove page numbers like "Page 1 of 12"
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", " ", text, flags=re.IGNORECASE)

    # 4. Remove standalone page numbers
    text = re.sub(r"^\s*\d+\s*$", " ", text, flags=re.MULTILINE)

    # 5. Fix broken line endings (join lines that shouldn't be separate)
    text = re.sub(r"\n(?=[a-z])", " ", text)  # lowercase continuation
    text = re.sub(r"\n(?=[A-Z][a-z])", " ", text)  # normal sentence continuation

    # 6. Remove double newlines
    text = re.sub(r"\n{2,}", "\n", text)

    # 7. Collapse multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # 8. Strip leading/trailing whitespace
    text = text.strip()

    return text

def clean_text_ocr_fl401(text: str) -> str:
    """
    Light FL401 cleaning — keeps ALL content.
    Only normalises spacing and prepares for field extraction.
    """
    import re

    # Remove obvious OCR garbage
    text = re.sub(r"[|~•■□▪◦●◆◇▶◀✓✔✗✘]", " ", text)

    # Remove long punctuation lines
    text = re.sub(r"[-_=]{3,}", " ", text)

    # Fix broken lines
    text = re.sub(r"\n(?=[a-z])", " ", text)
    text = re.sub(r"\n(?=[A-Z][a-z])", " ", text)

    # Collapse whitespace
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)

    return text.strip()



def extract_text_ocr(path):
    images = convert_pdf_to_images_pymupdf(path)
    text = ""

    for img_bytes in images:
        img = Image.open(io.BytesIO(img_bytes))
        
        text += pytesseract.image_to_string(img) + "\n"

    return text

import re

def extract_applicant_name(text: str):
    """
    Extracts applicant first name, last name, and any alias.
    """
    # First + Last name
    name_pattern = (
        r"Your full name\s+"
        r"First name\(s\)\s+([A-Za-z ]+)\s+"
        r"Last name\s+([A-Za-z ]+)"
    )
    m = re.search(name_pattern, text)
    
    first_name = m.group(1).strip() if m else None
    last_name = m.group(2).strip() if m else None

    # Alias / previous names
    alias_pattern = r"Any other names you have been known by\s+([A-Za-z ]+)"
    alias_match = re.search(alias_pattern, text)
    alias = alias_match.group(1).strip() if alias_match else None

    return {
        "first_name": first_name,
        "last_name": last_name,
        "alias": alias
    }
    
def extract_applicant_address(text:str):
    return {}


def extract_respondent_address(text: str):
    """
    Extracts respondent address block.
    """
    pattern = (
        r"Their full current address\s+"
        r"Building and street\s+(.+?)\s+"
        r"Second line of address\s+(.+?)\s+"
        r"Town or city\s+(.+?)\s+"
        r"County \(optional\)\s+(.+?)\s+"
        r"Postcode\s+(.+?)\s"
    )

    m = re.search(pattern, text, flags=re.DOTALL)
    if not m:
        return None

    # Extract raw postcode exactly as OCR produced it
    postcode_raw = m.group(5).strip()

    # Repair broken OCR postcode (Option A)
    postcode = repair_local_postcode(postcode_raw)

    return {
        "line1": m.group(1).strip(),
        "line2": m.group(2).strip(),
        "town": m.group(3).strip(),
        "county": m.group(4).strip(),
        "postcode": postcode
    }
import re

def extract_respondent_name(text: str):
    """
    Extracts respondent first and last name.
    """
    pattern = (
        r"Their name\s+"
        r"First name\(s\)\s+([A-Za-z ]+)\s+"
        r"Last name\s+([A-Za-z ]+)"
    )
    m = re.search(pattern, text)
    if not m:
        return None

    return {
        "first_name": m.group(1).strip(),
        "last_name": m.group(2).strip()
    }

def extract_respondent_address(text: str):
    """
    Extracts respondent address block.
    """
    
   
    
    
    pattern = (
        r"Their full current address\s+"
        r"Building and street\s+(.+?)\s+"
        r"Second line of address\s+(.+?)\s+"
        r"Town or city\s+(.+?)\s+"
        r"County \(optional\)\s+(.+?)\s+"
        r"Postcode\s+([A-Z0-9 \n]+?)\s+FL401"
        )

    m = re.search(pattern, text, flags=re.DOTALL)
    if not m:
        return {}
    p_code=get_respondent_postcode_from_clean_text(text)
    return {
        "line1": m.group(1).strip(),
        "line2": m.group(2).strip(),
        "town": m.group(3).strip(),
        "county": m.group(4).strip(),
        "postcode":p_code,

    }


    
    



def extract_respondent_details(text: str):
    return {
        "name": extract_respondent_name(text),
        "address": extract_respondent_address(text)
    }


def extract_children(text: str):
    """
    Extracts children from OCR text where the children table is flattened into columns.
    Always returns a list.
    """

    children = []

    # Pattern for a row in the children table:
    # <name> <dob> <applicant_rel> <parental_resp_flag> <respondent_rel>
    pattern = (
        r"([A-Za-z][A-Za-z \-']+?)\s+"                # child's name
        r"([0-9]{2}/[0-9]{2}/[0-9]{4})\s+"            # date of birth
        r"([A-Za-z]+)\s+"                             # applicant relationship
        r"([A-Za-z]+)\s+"                             # parental responsibility flag (Yes/No/es)
        r"([A-Za-z]+)"                                # respondent relationship
    )

    matches = re.findall(pattern, text, flags=re.DOTALL)

    for name, dob, rel_app, pr_flag, rel_resp in matches:
        children.append({
            "name": name.strip(),
            "dob": dob.strip(),
            "applicant_relationship": rel_app.strip(),
            "respondent_relationship": rel_resp.strip(),
            "both_have_parental_responsibility": pr_flag.lower().startswith("y")
        })

    return children
def extract_orders_requested(text: str):
    """
    Detects whether the applicant is seeking:
    - non-molestation order
    - occupation order
    - both
    Returns a dict with booleans.
    """

    # Normalise text for easier matching
    t = text.lower()

    # Detect non-molestation order
    nm_patterns = [
        r"non[- ]molestation order",
        r"nonmolestation order",
        r"non molestation order"
    ]
    wants_nm = any(re.search(p, t) for p in nm_patterns)

    # Detect occupation order
    occ_patterns = [
        r"occupation order",
        r"occupation\s+order"
    ]
    wants_occ = any(re.search(p, t) for p in occ_patterns)

    return {
        "non_molestation_order": wants_nm,
        "occupation_order": wants_occ,
        "both": wants_nm and wants_occ
    }
    

def extract_specific_orders(text: str):
    """
    Extracts all specific orders requested in Sections 6 and 7.
    Returns a dict with lists of selected prohibitions and occupation measures.
    """

    t = text.lower()

    # --- Non-molestation prohibitions ---
    nm_options = {
        "violence_to_applicant": r"being violent towards me",
        "threats_to_applicant": r"threatening me",
        "harassment_to_applicant": r"harassing or intimidating me",
        "publishing_about_applicant": r"posting or publishing about me",
        "contacting_applicant": r"contacting me directly",
        "damage_possessions": r"causing damage to my possessions",
        "damage_home": r"causing damage to my home",
        "entering_home": r"coming into my home",
        "near_home": r"coming near my home",
        "near_work": r"coming near my place of work",

        "violence_to_children": r"being violent towards my children",
        "harassment_to_children": r"harassing or intimidating my children",
        "publishing_about_children": r"posting or publishing anything about my children",
        "contacting_children": r"contacting my children directly",
        "near_school": r"going to or near my children’s school",
    }

    nm_selected = [
        key for key, pattern in nm_options.items()
        if re.search(pattern, t)
    ]

    # --- Occupation order measures ---
    occ_options = {
        "stay_in_home": r"stay in my home",
        "return_to_home": r"return to my home",
        "exclude_respondent": r"don’t want the respondent to be able to enter my home",
        "keep_respondent_away_area": r"keep the respondent away from the area surrounding my home",
        "limit_respondent_areas": r"limit where in the home the respondent can go",
        "repairs_contribution": r"contribute to repairs or maintenance",
        "rent_mortgage_contribution": r"contribute to the rent or mortgage",
        "use_of_furniture": r"use of the furniture or other household contents",
    }

    occ_selected = [
        key for key, pattern in occ_options.items()
        if re.search(pattern, t)
    ]

    return {
        "non_molestation_specific_orders": nm_selected,
        "occupation_specific_orders": occ_selected
        
    }


def extract_without_notice_reasons(text: str):
    """
    Extracts reasons (a, b, c) for a without-notice application.
    Returns a list of reason codes, e.g. ["a", "c"].
    """

    t = text.lower()
    reasons = []

    # Reason (a)
    if "risk of significant harm" in t:
        reasons.append("a")

    # Reason (b)
    if "deterred or prevented from pursuing" in t:
        reasons.append("b")

    # Reason (c)
    if "deliberately evading service" in t or "seriously prejudice" in t:
        reasons.append("c")

    return reasons

def extract_without_notice_flag(text: str):
    """
    Extracts whether the applicant is applying without notice.
    Returns True, False, or None if unclear.
    """
    block = r"apply for the order without giving notice.*?(Yes|No)"
    m = re.search(block, text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    return True if m.group(1).lower() == "yes" else False
import re

def extract_without_notice_explanation(text: str):
    """
    Extracts the applicant's explanation for why a without-notice order is needed.
    Returns a string or None.
    """

    pattern = (
        r"Why do you think.*?may happen\?\s*"   # The question heading
        r"(.+?)"                                # Capture explanation
        r"\s*As far as you know"                # Stop at next question
    )

    m = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return None

    explanation = m.group(1).strip()

    # Normalise whitespace
    explanation = re.sub(r"\s+", " ", explanation)

    return explanation if explanation else None



def extract_without_notice_details(text: str):
    return {
        "without_notice": extract_without_notice_flag(text),
        "reasons": extract_without_notice_reasons(text),
        "explanation": extract_without_notice_explanation(text)
    }
    
import re

def extract_relationship_category(text: str):
    """
    Extracts the relationship category from Section 4.1.
    Returns a string such as 'married', 'former_cohabitees', etc.
    """

    t = text.lower()

    categories = {
        "married": r"married or in a civil partnership",
        "formerly_married": r"formerly married or in a civil partnership",
        "engaged": r"engaged or proposed civil partnership",
        "formerly_engaged": r"formerly engaged or proposed civil partnership",
        "cohabitees": r"live together as a couple",
        "former_cohabitees": r"formerly lived together as a couple",
        "partners_not_living_together": r"boyfriend, girlfriend or partner who does not live with me",
        "former_partners_not_living_together": r"former boyfriend, girlfriend or partner who did not live with me",
        "other": r"none of the above"
    }

    for key, pattern in categories.items():
        if re.search(pattern, t):
            return key

    return None
def extract_other_relationship(text: str):
    """
    Extracts relationship type from Section 4.4 if 4.1 = 'other'.
    Returns e.g. 'father', 'sister', etc.
    """

    pattern = r"respondent’s relationship to you.*?(father|mother|son|daughter|brother|sister|grandfather|grandmother|uncle|aunt|nephew|niece|cousin)"
    m = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    return m.group(1).lower() if m else None

def extract_relationship_details(text: str):
    category = extract_relationship_category(text)

    return {
        "relationship_category": category,
    }
    
import re

def repair_local_postcode(raw_block: str):
    """
    Repairs a UK postcode using ONLY the text inside the same address block.
    Never guesses missing characters.
    Never mixes applicant/respondent postcodes.
    Returns:
      - full postcode (e.g. 'BN68 JF') if valid
      - outward code only (e.g. 'BN68') if valid
      - '' if nothing valid can be recovered
    """

    if not raw_block:
        return ""

    # Extract all postcode-like fragments from THIS block only
    fragments = re.findall(r"[A-Z]{1,2}\s*\d[A-Z0-9]?\s*\d[A-Z]{2}|[A-Z]{1,2}\s*\d[A-Z0-9]?", raw_block, flags=re.IGNORECASE)

    if not fragments:
        return ""

    # Clean and normalise each fragment
    cleaned = [f.replace(" ", "").upper() for f in fragments]

    # 1. Look for a full postcode (e.g. BN68JF)
    for pc in cleaned:
        if re.match(r"^[A-Z]{1,2}[0-9][0-9A-Z]?[0-9][A-Z]{2}$", pc):
            return pc[:-3] + " " + pc[-3:]   # insert space before inward code

    # 2. Look for a valid outward code (e.g. BN6, BN68, BN1A)
    for pc in cleaned:
        if re.match(r"^[A-Z]{1,2}[0-9][0-9A-Z]?$", pc):
            return pc

    # 3. Nothing valid
    return ""


def extract_fl401_cat_b(text: str) -> dict:

    # 1. Extract applicant fields
    applicant_name = extract_applicant_name(text)
    applicant_address = extract_applicant_address(text)

    # 2. Extract respondent fields
    respondent_name = extract_respondent_name(text)
    respondent_address = extract_respondent_address(text)

    # 3. Children
    children = extract_children(text)

    # 4. Orders
    orders = extract_orders_requested(text)
    specific_orders = extract_specific_orders(text)

    # 5. Without notice
    wn_flag = extract_without_notice_flag(text)
    wn_reasons = extract_without_notice_reasons(text)
    wn_expl = extract_without_notice_explanation(text)

    # 6. Relationship
    relationship = extract_relationship_details(text)

    # 7. Build Cat B structure (Option A: nested address)
    cat_b = {
        "applicant": {
            **applicant_name,
            "address": applicant_address,     # nested
            "dob": {},                        # placeholder
            "share_contact_details_no": "/No, complete C8"
        },

        "respondent": {
            **respondent_name,
            "address": respondent_address,    # nested
        },

        "children": children,

        "orders_requested": orders,
        "specific_orders": specific_orders,

        "without_notice": {
            "without_notice": wn_flag,
            "without_notice_reasons": wn_reasons,
            "without_notice_explanation": wn_expl
        },

        "relationship": relationship,

        "case": {
            "court_name": None,
            "case_number": None
        }
    }

    return cat_b

def extract_by_ocr(pdf_path):
    raw_text=ocr_file_to_text(pdf_path)
    clean_text=clean_text_ocr(raw_text)
    cat_b=extract_fl401_cat_b(clean_text)
    return cat_b
    

    
if __name__ == "__main__":
    pdf_path = r"C:\Users\sgcam\Projects\FL401_Extractor\FL401_Ellen_Champion_Flat.pdf"
    raw_text=ocr_file_to_text(pdf_path)
    clean_text=clean_text_ocr(raw_text)
    cat_b=extract_fl401_cat_b(clean_text)
    p_code=get_respondent_postcode_from_clean_text(clean_text)
    print("cat-b done")
    pyperclip.copy(cat_b)
    

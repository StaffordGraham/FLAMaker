from ocr import extract_text_ocr
from extractor.checkboxes import extract_form_fields, detect_checkboxes
from pypdf import PdfReader


import re
import os
import json
print("Working directory:", os.getcwd())

FIELD_MAP = {

    # ---------------------------------------------------------
    # APPLICANT DETAILS (Section 2)
    # ---------------------------------------------------------

    # Applicant name
    "2.1 First name(s)": "applicant.first_name",
    "2.1 Last name": "applicant.last_name",
    "2.2 Any other names you have been known by": "applicant.other_names",

    # Applicant DOB
    "2.3 Your date of birth - DD": "applicant.dob.day",
    "2.3 Your date of birth - MM": "applicant.dob.month",
    "2.3 Your date of birth - YYYY": "applicant.dob.year",

    # Applicant address
    "2.5 Your full current address: building and street": "applicant.address.line1",
    "2.5 Your full current address: second line of address": "applicant.address.line2",
    "2.5 Your full current address: town or city": "applicant.address.town",
    "2.5 Your full current address: county (optional)": "applicant.address.county",
    "2.5 Your full current address: postcode": "applicant.address.postcode",

    # Applicant contact
    "2.6 Your phone number": "applicant.phone",
    "2.7 Your email address": "applicant.email",
    "2.9 Contact instructions, including safe call times": "applicant.safe_contact_instructions",

    # Contact details shareable?
    "2.4 Can your contact details be shared with the respondent? Yes": "applicant.share_contact_details_yes",
    "2.4 Can your contact details be shared with the respondent? No": "applicant.share_contact_details_no",

    # ---------------------------------------------------------
    # RESPONDENT DETAILS (Section 3)
    # ---------------------------------------------------------

    "3.1 First name(s)": "respondent.first_name",
    "3.1 Last name": "respondent.last_name",
    "3.2 Any other names the respondent has been known by": "respondent.other_names",

    # Respondent DOB
    "3.3 The respondent's date of birth - DD": "respondent.dob.day",
    "3.3 The respondent's date of birth - MM": "respondent.dob.month",
    "3.3 The respondent's date of birth - YYYY": "respondent.dob.year",

    # Respondent address
    "3.5 Respondent's full current address: Building and street": "respondent.address.line1",
    "3.5 Respondent's full current address: Second line of address": "respondent.address.line2",
    "3.5 Respondent's full current address: Town or city": "respondent.address.town",
    "3.5 Respondent's full current address: County": "respondent.address.county",
    "3.5 Respondent's full current address: postcode": "respondent.address.postcode",

    # Respondent contact
    "3.6 The respondent's phone number (if you know it)": "respondent.phone",
    "3.7 The respondent's email address (if you know it)": "respondent.email",

    # Lives together?
    "3.4 Does the respondent live with you? Yes": "respondent.lives_with_applicant_yes",
    "3.4 Does the respondent live with you? No": "respondent.lives_with_applicant_no",

    # ---------------------------------------------------------
    # RELATIONSHIP DETAILS (Section 4)
    # ---------------------------------------------------------

    "4.1 Married or in a civil partnership": "relationship.married",
    "4.1 Formerly married or in a civil partnership": "relationship.formerly_married",
    "4.1 Engaged or proposed civil partnership": "relationship.engaged",
    "4.1 Formerly engaged or proposed civil partnership": "relationship.formerly_engaged",
    "4.1 Live together as a couple": "relationship.live_together",
    "4.1 Formerly lived together as a couple": "relationship.formerly_lived_together",
    "4.1 Boyfriend, girlfriend or partner who does not live with me": "relationship.partner_not_living_together",
    "4.1 Former boyfriend, girlfriend or partner who does not live with me": "relationship.former_partner_not_living_together",
    "4.1 None of the above. Go to question 4.4": "relationship.none_of_the_above",

    # Relationship start/end
    "4.2 When did your relationship start and when did it end? Start - DD": "relationship.start.day",
    "4.2 When did your relationship start and when did it end? Start - MM": "relationship.start.month",
    "4.2 When did your relationship start and when did it end? Start - YYYY": "relationship.start.year",
    "4.2 When did your relationship start and when did it end? End - DD": "relationship.end.day",
    "4.2 When did your relationship start and when did it end? End - MM": "relationship.end.month",
    "4.2 When did your relationship start and when did it end? End - YYYY": "relationship.end.year",

    # Wedding date
    "4.3 If you are or were previously married or in a civil partnership with the respondent, what date was your wedding or civil ceremony? DD": "relationship.wedding.day",
    "4.3 If you are or were previously married or in a civil partnership with the respondent, what date was your wedding or civil ceremony? MM": "relationship.wedding.month",
    "4.3 If you are or were previously married or in a civil partnership with the respondent, what date was your wedding or civil ceremony? YYYY": "relationship.wedding.year",

    # ---------------------------------------------------------
    # CHILDREN (Section 5)
    # ---------------------------------------------------------

    # Child 1
    "5.2 Child's full name 1": "children[0].name",
    "5.2 Child's date of birth 1": "children[0].dob",
    "5.2 Your relationship to the child 1": "children[0].relationship_to_applicant",
    "Respondent’s relationship to the child 1": "children[0].relationship_to_respondent",

    # Child 2
    "5.2 Child's full name 2": "children[1].name",
    "5.2 Child's date of birth 2": "children[1].dob",
    "5.2 Your relationship to the child 2": "children[1].relationship_to_applicant",
    "Respondent’s relationship to the child 2": "children[1].relationship_to_respondent",

    # Child 3
    "5.2 Child's full name 3": "children[2].name",
    "5.2 Child's date of birth 3": "children[2].dob",
    "5.2 Your relationship to the child 3": "children[2].relationship_to_applicant",
    "Respondent’s relationship to the child 3": "children[2].relationship_to_respondent",

    # Child 4
    "5.2 Child's full name 4": "children[3].name",
    "5.2 Child's date of birth 4": "children[3].dob",
    "5.2 Your relationship to the child 4": "children[3].relationship_to_applicant",
    "Respondent’s relationship to the child 4": "children[3].relationship_to_respondent",

    # ---------------------------------------------------------
    # WITHOUT NOTICE (Section 1)
    # ---------------------------------------------------------

    "Do you want to apply for the order without giving notice to the respondent? Yes": "without_notice.apply_yes",
    "Do you want to apply for the order without giving notice to the respondent? No": "without_notice.apply_no",

    "Why do you want to apply without giving notice to the respondent? a)": "without_notice.reason_a",
    "Why do you want to apply without giving notice to the respondent? b)": "without_notice.reason_b",
    "Why do you want to apply without giving notice to the respondent? c)": "without_notice.reason_c",

    "Why do you think one or more of the reasons you have chosen for question 1.3 may happen?":
        "without_notice.explanation",

    # ---------------------------------------------------------
    # BAIL CONDITIONS (Section 1.5–1.6)
    # ---------------------------------------------------------

    "As far as you know, are there any bail conditions stopping the respondent from contacting or coming near you? Yes":
        "bail.conditions_yes",
    "As far as you know, are there any bail conditions stopping the respondent from contacting or coming near you? No":
        "bail.conditions_no",

    "When do the bail conditions end? DD": "bail.end.day",
    "When do the bail conditions end? MM": "bail.end.month",
    "When do the bail conditions end? YYYY": "bail.end.year",

    # ---------------------------------------------------------
    # NON-MOLESTATION ORDER (Section 6)
    # ---------------------------------------------------------

    "6.1 Are you applying for a non-molestation order? Yes": "nonmol.apply_yes",
    "6.1 Are you applying for a non-molestation order? No": "nonmol.apply_no",

    # Behaviours
    "6.2 What do you want to stop the respondent from doing? Being violent towards me or threatening me":
        "nonmol.behaviour.violent",
    "6.2 What do you want to stop the respondent from doing? Harassing or intimidating me":
        "nonmol.behaviour.harassing",
    "6.2 What do you want to stop the respondent from doing? Posting or publishing about me either in print or digitally":
        "nonmol.behaviour.publishing",
    "6.2 What do you want to stop the respondent from doing? Contacting me directly":
        "nonmol.behaviour.contacting",
    "6.2 What do you want to stop the respondent from doing? Causing damage to my possessions":
        "nonmol.behaviour.damage_possessions",
    "6.2 What do you want to stop the respondent from doing? Causing damage to my home":
        "nonmol.behaviour.damage_home",
    "6.2 What do you want to stop the respondent from doing? Coming into my home":
        "nonmol.behaviour.enter_home",
    "6.2 What do you want to stop the respondent from doing? Coming near my home":
        "nonmol.behaviour.near_home",
    "6.2 What do you want to stop the respondent from doing? Coming near my place of work":
        "nonmol.behaviour.near_work",

    # Children behaviours
    "6.3 What do you want to stop the respondent from doing to your child or children (if applicable)? Being violent towards my children or threatening my children":
        "nonmol.children.violent",
    "6.3 What do you want to stop the respondent from doing to your child or children (if applicable)? Harassing or intimidating my children":
        "nonmol.children.harassing",
    "6.3 What do you want to stop the respondent from doing to your child or children (if applicable)? Posting or publishing anything about my children in print, or digitally":
        "nonmol.children.publishing",
    "6.3 What do you want to stop the respondent from doing to your child or children (if applicable)? Contacting my children directly without my consent":
        "nonmol.children.contacting",

    # Additional behaviour
    "6.4 Is there anything else you want the respondent to stop doing that is not mentioned in question 6.1 or 6.2?":
        "nonmol.additional",

}

def set_nested(obj, path, value):
    parts = path.replace("]", "").split(".")
    current = obj

    for i, part in enumerate(parts):
        if "[" in part:
            name, index = part.split("[")
            index = int(index)

            if name not in current:
                current[name] = []

            while len(current[name]) <= index:
                current[name].append({})

            current = current[name][index]

        else:
            if i == len(parts) - 1:
                current[part] = value
            else:
                current = current.setdefault(part, {})


def build_case_json(fields):
    result = {}

    for pdf_name, data in fields.items():
        value = data.get("/V", "")

        # Skip empty values
        if value in ("", None, "/Off"):
            continue

        # Only map fields we recognise
        if pdf_name in FIELD_MAP:
            json_path = FIELD_MAP[pdf_name]
            set_nested(result, json_path, value)

    return result

def extract_form_fields(path):
    reader = PdfReader(path)
    fields = reader.get_fields()
    return fields

def normalise_category_a_output(raw):
    """
    Converts the existing Category A extractor output into the unified FL401 format.
    """

    # --- Without notice ---
    wn_apply = raw["without_notice"].get("apply_yes") == "/Yes"
    wn_reasons = []
    if raw["without_notice"].get("reason_a") == "/a)":
        wn_reasons.append("a")
    if raw["without_notice"].get("reason_b") == "/b)":
        wn_reasons.append("b")
    if raw["without_notice"].get("reason_c") == "/c)":
        wn_reasons.append("c")

    wn_expl = raw["without_notice"].get("explanation", "")

    # --- Orders requested ---
    nm = raw.get("nonmol", {}).get("apply_yes") == "/Yes"
    occ = raw.get("occupation", {}).get("apply_yes") == "/Yes"

    # --- Relationship ---
    rel = raw["relationship"]
    if rel.get("married") == "/Yes":
        relationship_category = "married"
    elif rel.get("none_of_the_above"):
        relationship_category = "other"
    else:
        relationship_category = "unknown"

    # --- Children ---
    children = []
    for c in raw["children"]:
        children.append({
            "name": c["name"].strip(),
            "dob": c["dob"],
            "applicant_relationship": c["relationship_to_applicant"],
            "respondent_relationship": c["relationship_to_respondent"]
        })

    # --- Unified output ---
    return {
        "applicant": raw["applicant"],
        "respondent": raw["respondent"],
        "children": children,
        "orders_requested": {
            "non_molestation": nm,
            "occupation": occ
        },
        "without_notice": {
            "without_notice": wn_apply,
            "without_notice_reasons": wn_reasons,
            "without_notice_explanation": wn_expl
        },
        "relationship": {
            "relationship_category": relationship_category,
            "relationship_start": rel.get("start"),
            "relationship_end": rel.get("end"),
            "marriage_date": rel.get("wedding"),
            "other_relationship": None
        },
        "case": {
            "court_name": None,
            "case_number": None
        }
    }
def extract_from_fl401_by_field(pdf_path):
    fields=extract_form_fields(pdf_path)
    if fields==None:
        return None
    case_json=build_case_json(fields)
    return case_json
    
    

def normalise_fl401_to_casedetails(data, case_details):
    """
    Maps the FL401 extractor output into the CaseDetails object.
    """

    # --- Orders requested ---
    case_details.molestation_order = data["orders_requested"]["non_molestation"]
    case_details.occupation_order = data["orders_requested"]["occupation"]

    # --- Notice / Without Notice ---
    wn = data["without_notice"]["without_notice"]
    case_details.notice = "Without Notice" if wn else "On Notice"

    # Reasons (string summary)
    reasons = data["without_notice"]["without_notice_reasons"]
    case_details.reasons = ", ".join(reasons) if reasons else ""

    # Explanation
    expl = data["without_notice"]["without_notice_explanation"]
    if expl:
        case_details.reasons += f" — {expl}"

    # --- Applicant ---
    app = data["applicant"]
    case_details.applicant.first_name = app["first_name"]
    case_details.applicant.last_name = app["last_name"]
    case_details.applicant.dob = app["dob"]
    case_details.applicant.address = app.get("address", "")

    # --- Respondent ---
    resp = data["respondent"]
    case_details.respondent.first_name = resp["first_name"]
    case_details.respondent.last_name = resp["last_name"]
    case_details.respondent.dob = resp["dob"]
    case_details.respondent.address = resp.get("address", "")

    # --- Children ---
    case_details.children = []
    for child in data["children"]:
        c = child(
            name=child["name"],
            dob=child["dob"],
            relationship_to_applicant=child["applicant_relationship"],
            relationship_to_respondent=child["respondent_relationship"]
        )
        case_details.children.append(c)

    # --- Relationship ---
    rel = data["relationship"]["relationship_category"]
    case_details.relationship = rel

    # --- Case details (if present) ---
    case_details.case_number = data["case"].get("case_number", "")
    case_details.court_name = data["case"].get("court_name", "")
    






# if __name__ == "__main__":
#     pdf_path = r"C:\Users\sgcam\Projects\FL401_Extractor\FL401_Ellen_Champion.pdf"
#     fields=extract_form_fields(pdf_path)
#     case_json=build_case_json(fields)
    
#     print ('lovely white and clean')
#     case_details=normalise_category_a_output(case_json)
#     print ('m oddley normal')
#     pyperclip.copy(case_json)


    
    

    
    
    
    


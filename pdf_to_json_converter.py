<<<<<<< HEAD
import os
import json
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re

# Path to the folder containing PDF templates
PDF_TEMPLATES_FOLDER = r"C:\\Users\\aasav\\Downloads\\voice2text templates"
# Path to save generated JSON templates
JSON_TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), "json_templates")
os.makedirs(JSON_TEMPLATES_FOLDER, exist_ok=True)

def extract_text_from_image(image):
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image, lang='hin')  # Hindi language
    return text

def extract_blocks_from_text(text):
    """
    Extract blocks based on section headings or block titles.
    This is a simple heuristic that splits text by headings.
    Adjust regex as per your PDF structure.
    """
    blocks = []
    # Example regex to find headings (assuming headings are in all caps or numbered)
    headings = re.findall(r'(^[A-Z\s]+$|^\d+\.\s.*$)', text, re.MULTILINE)
    if not headings:
        # If no headings found, treat whole text as one block
        blocks.append({"id": "block1", "name": "Content", "text": text.strip()})
        return blocks

    # Split text by headings
    parts = re.split(r'(^[A-Z\s]+$|^\d+\.\s.*$)', text, flags=re.MULTILINE)
    # parts will have empty strings and headings alternately
    current_block = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if re.match(r'^[A-Z\s]+$|^\d+\.\s.*$', part):
            # This is a heading
            if current_block:
                blocks.append(current_block)
            current_block = {"id": re.sub(r'\W+', '_', part.lower()), "name": part, "text": ""}
        else:
            if current_block:
                current_block["text"] += part + "\n"
            else:
                current_block = {"id": "block1", "name": "Content", "text": part}
    if current_block:
        blocks.append(current_block)
    return blocks

def convert_pdf_to_json(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = extract_text_from_image(img)
        full_text += text + "\n"

    blocks = extract_blocks_from_text(full_text)
    template_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Prepare JSON structure
    json_template = {
        "template_name": template_name,
        "blocks": [{"id": b["id"], "name": b["name"]} for b in blocks]
    }

    # Save JSON file
    json_filename = template_name + ".json"
    json_filepath = os.path.join(JSON_TEMPLATES_FOLDER, json_filename)
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(json_template, f, ensure_ascii=False, indent=2)

    print(f"Converted {pdf_path} to {json_filepath}")

def main():
    for filename in os.listdir(PDF_TEMPLATES_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_TEMPLATES_FOLDER, filename)
            convert_pdf_to_json(pdf_path)

if __name__ == "__main__":
    main()
=======
import os
import json
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re

# Path to the folder containing PDF templates
PDF_TEMPLATES_FOLDER = r"C:\\Users\\aasav\\Downloads\\voice2text templates"
# Path to save generated JSON templates
JSON_TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), "json_templates")
os.makedirs(JSON_TEMPLATES_FOLDER, exist_ok=True)

def extract_text_from_image(image):
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image, lang='hin')  # Hindi language
    return text

def extract_blocks_from_text(text):
    """
    Extract blocks based on section headings or block titles.
    This is a simple heuristic that splits text by headings.
    Adjust regex as per your PDF structure.
    """
    blocks = []
    # Example regex to find headings (assuming headings are in all caps or numbered)
    headings = re.findall(r'(^[A-Z\s]+$|^\d+\.\s.*$)', text, re.MULTILINE)
    if not headings:
        # If no headings found, treat whole text as one block
        blocks.append({"id": "block1", "name": "Content", "text": text.strip()})
        return blocks

    # Split text by headings
    parts = re.split(r'(^[A-Z\s]+$|^\d+\.\s.*$)', text, flags=re.MULTILINE)
    # parts will have empty strings and headings alternately
    current_block = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if re.match(r'^[A-Z\s]+$|^\d+\.\s.*$', part):
            # This is a heading
            if current_block:
                blocks.append(current_block)
            current_block = {"id": re.sub(r'\W+', '_', part.lower()), "name": part, "text": ""}
        else:
            if current_block:
                current_block["text"] += part + "\n"
            else:
                current_block = {"id": "block1", "name": "Content", "text": part}
    if current_block:
        blocks.append(current_block)
    return blocks

def convert_pdf_to_json(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = extract_text_from_image(img)
        full_text += text + "\n"

    blocks = extract_blocks_from_text(full_text)
    template_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Prepare JSON structure
    json_template = {
        "template_name": template_name,
        "blocks": [{"id": b["id"], "name": b["name"]} for b in blocks]
    }

    # Save JSON file
    json_filename = template_name + ".json"
    json_filepath = os.path.join(JSON_TEMPLATES_FOLDER, json_filename)
    with open(json_filepath, "w", encoding="utf-8") as f:
        json.dump(json_template, f, ensure_ascii=False, indent=2)

    print(f"Converted {pdf_path} to {json_filepath}")

def main():
    for filename in os.listdir(PDF_TEMPLATES_FOLDER):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_TEMPLATES_FOLDER, filename)
            convert_pdf_to_json(pdf_path)

if __name__ == "__main__":
    main()
>>>>>>> 2df0a5b16486251fb482ea449e7da0de45eb7fba

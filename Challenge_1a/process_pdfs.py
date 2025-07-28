import fitz  # PyMuPDF
import json
import re
import numpy as np
from pathlib import Path

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^[^\w]+|[^\w]+$', '', text)
    text = re.sub(r'[\x00-\x1F]', '', text)
    return text.strip()

def detect_title(page, global_median, global_std):
    title_candidates = []

    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
    for block in blocks:
        if block["bbox"][1] >= page.rect.height * 0.25:
            continue

        block_text = ""
        font_sizes = []
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                if text:
                    block_text += text + " "
                    font_sizes.append(span["size"])

        if block_text and font_sizes:
            avg_size = np.mean(font_sizes)
            if avg_size > global_median + global_std:
                clean_block = clean_text(block_text)
                if clean_block and len(clean_block) > 5:
                    title_candidates.append((clean_block, avg_size))

    return max(title_candidates, key=lambda x: x[1])[0] if title_candidates else ""

def detect_headings(doc, title, global_median, global_std, page_dimensions):
    headings = []

    for page_num, page in enumerate(doc):
        page_width, page_height = page_dimensions[page_num]
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        for block in blocks:
            if block["bbox"][1] < page_height * 0.1 or block["bbox"][3] > page_height * 0.9:
                continue

            block_text = ""
            font_sizes = []
            is_bold = False
            is_centered = False
            line_count = 0

            for line in block.get("lines", []):
                line_count += 1
                line_text = ""
                line_font_sizes = []

                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text:
                        line_text += text + " "
                        line_font_sizes.append(span["size"])
                        if "bold" in span["font"].lower() or span["flags"] & 2**4:
                            is_bold = True

                if line_text:
                    x0 = min(span["bbox"][0] for span in line["spans"])
                    x1 = max(span["bbox"][2] for span in line["spans"])
                    line_center = (x0 + x1) / 2
                    is_centered = abs(line_center - page_width/2) < (page_width * 0.2)

                    block_text += line_text
                    font_sizes.extend(line_font_sizes)

            clean_block = clean_text(block_text)
            if not clean_block or clean_block == title:
                continue

            if (
                len(clean_block) < 3 or
                len(clean_block.split()) > 15 or
                re.match(r'^\d{1,2}[-–/]\d{1,2}[-–/]\d{2,4}$', clean_block) or
                re.match(r'^\d+$', clean_block) or
                clean_block.lower() in ["confidential", "draft", "internal use"] or
                (not is_bold and not is_centered) or
                line_count > 3
            ):
                continue

            if not font_sizes:
                continue

            avg_size = np.mean(font_sizes)
            size_diff = avg_size - global_median

            level = None
            if size_diff > 3 * global_std:
                level = "H1"
            elif size_diff > 2 * global_std:
                level = "H2"
            elif size_diff > global_std:
                level = "H3"
            elif size_diff > 0.5 * global_std:
                level = "H4"

            if level:
                headings.append({
                    "level": level,
                    "text": clean_block,
                    "page": page_num + 1
                })

    return headings

def process_pdf(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    font_sizes = []
    page_dimensions = []

    for page in doc:
        page_dimensions.append((page.rect.width, page.rect.height))
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if span["text"].strip():
                        font_sizes.append(span["size"])

    if not font_sizes:
        doc.close()
        return {"title": "Untitled", "outline": []}

    global_median = np.median(font_sizes)
    global_std = np.std(font_sizes) if len(font_sizes) > 1 else 2.0

    title = detect_title(doc[0], global_median, global_std)
    headings = detect_headings(doc, title, global_median, global_std, page_dimensions)
    doc.close()

    return {
        "title": title or "Untitled",
        "outline": headings
    }

def process_directory(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for pdf_file in input_dir.glob("*.pdf"):
        try:
            output = process_pdf(pdf_file)
            output_path = output_dir / f"{pdf_file.stem}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)
            print(f"✅ Processed {pdf_file.name}")
        except Exception as e:
            print(f"❌ Failed to process {pdf_file.name}: {e}")

if __name__ == "__main__":
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    process_directory(input_dir, output_dir)

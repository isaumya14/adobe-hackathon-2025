# import os
# import json
# import fitz  # PyMuPDF
# from pathlib import Path
# from datetime import datetime

# def load_input_json(input_file: Path):
#     with input_file.open("r") as f:
#         return json.load(f)

# def extract_keywords(text: str):
#     text = text.lower().replace(",", "").replace(".", "")
#     return [word for word in text.split() if len(word) > 3]

# def extract_relevant_text(pdf_path: Path, keywords: list):
#     doc = fitz.open(pdf_path)
#     relevant_sections = []

#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         blocks = page.get_text("blocks")

#         for block in blocks:
#             text = block[4].strip()
#             if not text:
#                 continue
#             score = sum(kw in text.lower() for kw in keywords)
#             if score > 0:
#                 relevant_sections.append({
#                     "document": pdf_path.name,
#                     "page": page_num + 1,
#                     "section_title": text.split("\n")[0][:80],
#                     "refined_text": text,
#                     "importance_score": score
#                 })

#     return relevant_sections

# def rank_and_format(sections: list):
#     sections.sort(key=lambda x: -x["importance_score"])
#     top_sections = sections[:5]

#     extracted_sections = []
#     analysis_sections = []

#     for rank, section in enumerate(top_sections, 1):
#         extracted_sections.append({
#             "document": section["document"],
#             "section_title": section["section_title"],
#             "importance_rank": rank,
#             "page_number": section["page"]
#         })

#         analysis_sections.append({
#             "document": section["document"],
#             "refined_text": section["refined_text"],
#             "page_number": section["page"]
#         })

#     return extracted_sections, analysis_sections

# def process_collection(input_dir: Path, output_dir: Path):
#     input_file = input_dir / "challenge1b_input.json"
#     if not input_file.exists():
#         print(f"❌ Input file not found: {input_file}")
#         return

#     data = load_input_json(input_file)
#     keywords = extract_keywords(data["job_to_be_done"]["task"])
#     all_sections = []

#     for doc in data["documents"]:
#         pdf_path = input_dir / "PDFs" / doc["filename"]
#         if not pdf_path.exists():
#             print(f"❗ Skipping missing file: {pdf_path.name}")
#             continue
#         all_sections.extend(extract_relevant_text(pdf_path, keywords))

#     extracted_sections, analysis = rank_and_format(all_sections)

#     result = {
#         "metadata": {
#             "input_documents": [d["filename"] for d in data["documents"]],
#             "persona": data["persona"]["role"],
#             "job_to_be_done": data["job_to_be_done"]["task"],
#             "timestamp": datetime.now().isoformat()
#         },
#         "extracted_sections": extracted_sections,
#         "subsection_analysis": analysis
#     }

#     output_path = output_dir / "challenge1b_output.json"
#     with output_path.open("w") as f:
#         json.dump(result, f, indent=2)

#     print(f"✅ Output generated: {output_path}")

# def main():
#     base_input_dir = Path("/app/input")
#     base_output_dir = Path("/app/output")

#     # Scan for all collection directories
#     for collection in sorted(base_input_dir.iterdir()):
#         if not collection.is_dir():
#             continue
#         print(f"\n📂 Processing {collection.name} ...")

#         input_subdir = collection
#         output_subdir = base_output_dir / collection.name
#         output_subdir.mkdir(parents=True, exist_ok=True)

#         process_collection(input_subdir, output_subdir)

# if __name__ == "__main__":
#     main()

import os
import json
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime

def load_input_json(input_file: Path):
    with input_file.open("r") as f:
        return json.load(f)

def extract_keywords(text: str):
    text = text.lower().replace(",", "").replace(".", "")
    return [word for word in text.split() if len(word) > 3]

def extract_relevant_text(pdf_path: Path, keywords: list):
    doc = fitz.open(pdf_path)
    relevant_sections = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4].strip()
            if not text:
                continue
            score = sum(kw in text.lower() for kw in keywords)
            if score > 0:
                relevant_sections.append({
                    "document": pdf_path.name,
                    "page": page_num + 1,
                    "section_title": text.split("\n")[0][:80],
                    "refined_text": text,
                    "importance_score": score
                })

    return relevant_sections

def rank_and_format(sections: list):
    sections.sort(key=lambda x: -x["importance_score"])
    top_sections = sections[:5]

    extracted_sections = []
    analysis_sections = []

    for rank, section in enumerate(top_sections, 1):
        extracted_sections.append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": rank,
            "page_number": section["page"]
        })

        analysis_sections.append({
            "document": section["document"],
            "refined_text": section["refined_text"],
            "page_number": section["page"]
        })

    return extracted_sections, analysis_sections

def process_collection(input_dir: Path, output_dir: Path):
    input_file = input_dir / "challenge1b_input.json"
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return

    data = load_input_json(input_file)
    keywords = extract_keywords(data["job_to_be_done"]["task"])
    all_sections = []

    for doc in data["documents"]:
        pdf_path = input_dir / "PDFs" / doc["filename"]
        if not pdf_path.exists():
            print(f"❗ Skipping missing file: {pdf_path.name}")
            continue
        all_sections.extend(extract_relevant_text(pdf_path, keywords))

    extracted_sections, analysis = rank_and_format(all_sections)

    result = {
        "metadata": {
            "input_documents": [d["filename"] for d in data["documents"]],
            "persona": data["persona"]["role"],
            "job_to_be_done": data["job_to_be_done"]["task"],
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": analysis
    }

    output_path = output_dir / "challenge1b_output.json"
    with output_path.open("w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Output generated: {output_path}")

def main():
    base_input_dir = Path("/app/input")
    base_output_dir = Path("/app/output")

    # Scan for all collection directories, skip hidden ones like .git
    for collection in sorted(base_input_dir.iterdir()):
        if not collection.is_dir() or collection.name.startswith("."):
            continue  # Skip non-directories and hidden folders
        print(f"\n📂 Processing {collection.name} ...")

        input_subdir = collection
        output_subdir = base_output_dir / collection.name
        output_subdir.mkdir(parents=True, exist_ok=True)

        process_collection(input_subdir, output_subdir)

if __name__ == "__main__":
    main()


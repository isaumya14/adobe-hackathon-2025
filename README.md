# Adobe India Hackathon 2025

## 🚀 Connecting the Dots Challenge

> Rethink Reading. Rediscover Knowledge.

In a world flooded with documents, what wins is not more content — it's context. This challenge reimagines the humble PDF as an intelligent, interactive experience. We transform static PDFs into structured, searchable, and persona-aware content for enhanced user experience.

---

## 🧩 Challenge Overview

This repository includes solutions to both subproblems of Round 1:

* **Challenge 1A**: Structured PDF outline extraction
* **Challenge 1B**: Multi-document, persona-driven content extraction

All solutions are:

* Fully containerized using **Docker**
* Designed for **offline**, **CPU-only** environments
* Deterministic and schema-compliant

---

## 📘 Challenge 1A – Structured PDF Processing

### 🧠 Approach

* Extract the **title** from the first page using font-size and page region heuristics.
* Detect **section headings** using boldness, centering, and font-size deviation.
* Classify heading levels (H1–H4) based on statistical analysis of font sizes.
* Output a clean JSON structure with document title and hierarchical outline.

### 🧰 Libraries Used

* `PyMuPDF (fitz)` – for PDF parsing
* `NumPy` – for font size analytics

### 🐳 How to Build & Run (Docker)

Navigate to Challenge\_1a:

```bash
cd Challenge_1a
```

Build the image:

```bash
docker build --platform linux/amd64 -t challenge1a .
```

Run the container:

```bash
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs/challenge1a:/app/output \
  --network none \
  challenge1a
```

> 📤 Output: JSON files saved in `sample_dataset/outputs/challenge1a/`.

---

## 📙 Challenge 1B – Persona-Based PDF Analysis

### 🧠 Approach

* Parse user persona and job-to-be-done from `challenge1b_input.json`
* Extract and score relevant sections from each PDF using keyword overlap
* Rank and return top 5 matching sections with metadata
* Output JSON includes section metadata and refined content analysis

### 🧰 Libraries Used

* `PyMuPDF (fitz)` – for document parsing
* `scikit-learn` – optional TF-IDF experiments
* Standard Python libraries

### 🐳 How to Build & Run (Docker)

Navigate to Challenge\_1b:

```bash
cd ../Challenge_1b
```

Build the image:

```bash
docker build --platform linux/amd64 -t challenge1b .
```

Run for Collection 1:

```bash
docker run --rm \
  -v "$(pwd)/Collection 1:/app/input:ro" \
  -v "$(pwd)/Collection 1:/app/output" \
  --network none \
  challenge1b
```

> 📤 Output: `challenge1b_output.json` saved in the corresponding Collection folder.
> 🔁 Repeat for Collection 2 and 3.

---

## 📁 Folder Structure

```
Adobe-India-Hackathon25/
├── Challenge_1a/
│   ├── Dockerfile
│   ├── process_pdfs.py
│   ├── requirements.txt
│   └── sample_dataset/
│       ├── pdfs/
│       ├── outputs/
│       └── schema/
├── Challenge_1b/
│   ├── Dockerfile
│   ├── challenge1b.py
│   ├── requirements.txt
│   ├── Collection 1/
│   ├── Collection 2/
│   └── Collection 3/
└── README.md
```

---

## ✅ Constraints Satisfied

* ✅ Fully offline, zero-internet execution
* ✅ Runs on CPU-only machines
* ✅ Dockerized for reproducibility
* ✅ JSON output matches Adobe’s expected schema

---

## 👥 Authors

* Saumya Singh
* Saket Abhishek
* Tanishka

### 🏁 Submission For

**Adobe India Hackathon: Connecting the Dots**


### 📩 Contact

We’d love to connect! Reach out on LinkedIn for feedback or collaboration.
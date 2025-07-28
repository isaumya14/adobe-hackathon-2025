## 📄 Challenge 1A: Document Structure Extraction

### 🧠 Objective

The goal of this challenge is to automatically extract structural information from unstructured PDF documents. This includes identifying:

* The main **document title**
* **Section headings** along with their corresponding hierarchical levels (e.g., H1, H2, H3, H4)

The output should be in a structured JSON format that helps readers and systems understand the layout and semantics of the document.

---

### 🧠 Our Approach

Our solution uses a heuristic-driven visual analysis strategy. The following key steps are involved:

1. **Font Analysis**: We collect font sizes across the document and compute the global median and standard deviation. Larger-than-average fonts often signify titles or section headings.

2. **Title Detection**:

   * We look at the top 25% vertical area of the first page.
   * Text blocks with significantly larger font sizes than the median are considered as title candidates.
   * From those, the best candidate is selected as the document title.

3. **Heading Detection**:

   * We iterate through all pages and skip known footer/header areas.
   * Text blocks are analyzed for formatting cues like **bold font**, **center alignment**, and **font size**.
   * Using font size deviation from the median, we classify headings into one of four levels (H1–H4).
   * We also filter out non-heading elements like page numbers, dates, or noise using pattern matching and length constraints.

This rule-based approach avoids the need for training and ensures transparency and explainability in how headings are assigned.

---

### 📚 Models & Libraries

* **Python 3.10** — Primary programming language
* **[PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)** — To extract text blocks and font metadata from PDFs
* **NumPy** — For statistical computations on font sizes

---

### 🛠️ How to Build & Run

You can run this solution entirely in a Dockerized environment. Below are the steps to build and execute:

```bash
# Step 1: Build the Docker image
docker build -t challenge1a:latest .

# Step 2: Run the container with mounted input/output folders
docker run --rm \
  --platform=linux/amd64 \
  -v "$(pwd)/sample_dataset/pdfs:/app/input" \
  -v "$(pwd)/output:/app/output" \
  --network none \
  challenge1a:latest
```

Place all input `.pdf` files inside the `sample_dataset/pdfs/` directory. The container will generate corresponding `.json` files in the `output/` folder.

---

### ✅ Output Format

Each output file will have the same base name as the PDF and will follow this format:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Main Section Heading", "page": 1 },
    { "level": "H2", "text": "Subsection Heading", "page": 2 }
  ]
}
```

This structured output can be used to power document indexing systems, search engines, or intelligent readers that rely on content hierarchy.

---

### 📁 Folder Structure

Below is a sample folder structure expected for Challenge 1A:

```
Challenge_1a/
├── Dockerfile
├── process_pdfs.py
├── requirements.txt
├── sample_dataset/
│   └── pdfs/
│       ├── document1.pdf
│       ├── document2.pdf
│       └── ...
├── output/  # Output JSON files will be saved here
```

### 🔍 Example Use Cases

* 📖 **Smart document viewers** that let readers jump to sections easily.
* 🔍 **Search optimization** by indexing documents based on structure.
* 📚 **E-learning platforms** where structured documents improve content delivery.

---

### 👥 Authors

* Saumya Singh
* Saket Abhishek
* Tanishka

### 🌟 Submission For

**Adobe India Hackathon: Connecting the Dots**
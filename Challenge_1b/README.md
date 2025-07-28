## 📄 Challenge 1B: Persona-Driven Section Extraction

### 🧠 Objective

To extract the most relevant content from a collection of documents based on a given user's persona and their job-to-be-done. The aim is to locate the top matching sections from various PDFs by evaluating their textual relevance.

---

### 🧠 Our Approach

Our solution revolves around keyword-driven matching using a simple but effective scoring mechanism. Here's a breakdown:

1. **Keyword Extraction**:

   * We extract important keywords from the user's job description by removing stopwords and filtering out short words.

2. **PDF Parsing**:

   * Each document is processed using PyMuPDF.
   * Text blocks are extracted from each page and compared with the keyword set.

3. **Relevance Scoring**:

   * A basic frequency-based keyword match scoring is used.
   * Each section receives a score based on the number of matching keywords.

4. **Ranking & Extraction**:

   * Sections are ranked by importance score.
   * The top 5 most relevant sections are selected.
   * We return metadata like page number, section title, and full text.

---

### 📂 Output Format

```json
{
  "metadata": {
    "persona": "Hiring Manager",
    "job_to_be_done": "Evaluate product roadmap alignment",
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "timestamp": "2025-07-28T17:00:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Product Strategy Overview",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Our roadmap focuses on AI integration...",
      "page_number": 3
    }
  ]
}
```

---

### 🛠️ How to Build & Run (Example: Collection 1)

```bash
# Step 1: Build the Docker image
docker build -t challenge1b:latest .

# Step 2: Run the container
docker run --rm \
  --platform=linux/amd64 \
  -v "$(pwd)/Collection 1:/app/input" \
  -v "$(pwd)/Collection 1/output:/app/output" \
  --network none \
  challenge1b:latest
```

---

### 📁 Folder Structure

```
Challenge_1b/
├── Dockerfile
├── challenge1b.py
├── requirements.txt
├── Collection 1/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── output/
├── Collection 2/
├── Collection 3/
```

---

### 🔍 Example Use Cases

* 📊 **Competitive analysis** from research reports
* 📖 **Targeted study material** for students from textbooks
* 🏢 **Business document insights** for personas like PMs, HRs, Analysts

---

### 👥 Authors

* Saumya Singh
* Saket Abhishek
* Tanishka

### 🌟 Submission For

**Adobe India Hackathon: Connecting the Dots**
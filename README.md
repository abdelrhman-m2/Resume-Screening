## project: "HR Smart Recruiter Pro"
description: |
  🚀 AI-powered recruitment platform designed to streamline and automate the hiring process.
  Analyze, categorize, and search through candidate CVs (PDF/DOCX) quickly and efficiently using **Streamlit**.

## structure:
  root: "hr-smart-recruiter/"
  files:
    - app.py: "Main Streamlit app"
    - Smart HR.ipynb: "Notebook for dataset exploration & training"
    - UpdatedResumeDataSet.csv: "Resume dataset"
    - requirements.txt: "Dependencies"
    - README.md: "Documentation"

## features:
  - "📄 Multi-format CV parsing → Supports PDF & DOCX"
  - "🧹 Text cleaning & preprocessing"
  - "🧠 AI-powered categorization (placeholder model included)"
  - "📊 Analytics Dashboard"
  - "🔑 Keyword search"
  - "⚡ Batch Processing"

# installation:
  steps:
    - "git clone https://github.com/<your-username>/hr-smart-recruiter.git"
    - "cd hr-smart-recruiter"
    - "python -m venv venv"
    - "source venv/bin/activate   # On Mac/Linux"
    - "venv\\Scripts\\activate    # On Windows"
    - "pip install -r requirements.txt"

# usage:
  run: "streamlit run app.py"
  url: "http://localhost:8501"

# dataset:
  file: "UpdatedResumeDataSet.csv"
  description: "Dataset for model training/testing"
  notebook: "Smart HR.ipynb → exploration & analysis"

# dependencies:
  - python
  - streamlit
  - joblib
  - pandas
  - scikit-learn
  - matplotlib
  - seaborn
  - PyPDF2
  - python-docx

# future_improvements:
  - "Integrate trained ML/DL models"
  - "Add semantic search with embeddings (FAISS + E5)"
  - "Deploy with Docker or Streamlit Cloud"
  - "Add candidate ranking"

license: "MIT License"
EOF

echo "✅ README.md created in YAML format (with dependencies included)"

# AI-Powered Resume Builder - Installation & Dependencies Documentation

## **1. System Requirements**
To run the AI-Powered Resume Builder, ensure you have the following installed:

- **Python** (Version 3.11 or higher)
- **pip** (Python package manager)
- **Git** (For version control, optional)

## **2. Dependencies**
This project relies on multiple Python libraries to function effectively. The required dependencies are:

```
anthropic>=0.47.2
pandas>=2.2.3
reportlab>=4.3.1
spacy>=3.8.4
streamlit>=1.42.2
```

## **3. Installation Steps**

### **Step 1: Clone the Repository (If Using GitHub)**
If the project is hosted on GitHub, you can clone it using:
```bash
git clone https://github.com/your-repo/ai-resume-builder.git
cd ai-resume-builder
```

### **Step 2: Create a Virtual Environment (Recommended)**
Setting up a virtual environment helps manage dependencies efficiently.
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### **Step 3: Install Dependencies**
Install all necessary dependencies using:
```bash
pip install -r requirements.txt
```
If you are using `pyproject.toml`, install dependencies with:
```bash
pip install .
```

### **Step 4: Download the SpaCy Language Model**
Since the project uses SpaCy for NLP-based suggestions, install the language model:
```bash
python -m spacy download en_core_web_sm
```

### **Step 5: Run the Application**
Launch the **Streamlit** application using:
```bash
streamlit run main.py
```
By default, the application will be accessible at:
```
http://localhost:8501
```

## **4. Project Structure**
```
├── assets/              # CSS and static files
├── utils/               # Helper modules
│   ├── nlp_helper.py       # NLP processing
│   ├── pdf_generator.py    # Resume PDF generation
│   └── resume_templates.py # Predefined templates
└── main.py             # Main application entry point
```

## **5. Troubleshooting**

### **Issue: Streamlit Not Found**
If `streamlit` is not recognized, try reinstalling it:
```bash
pip install streamlit
```

### **Issue: Dependencies Not Installing Correctly**
Try upgrading `pip` and reinstalling dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **Issue: SpaCy Model Not Found**
If you encounter errors related to SpaCy models, run:
```bash
python -m spacy download en_core_web_sm
```

## **6. Additional Resources**
For further information, visit:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SpaCy Documentation](https://spacy.io/)
- [Anthropic API Docs](https://docs.anthropic.com/)

This guide provides a complete setup for the AI-Powered Resume Builder. Follow these steps to get your application running smoothly!


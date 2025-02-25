# AI-Powered Resume Builder

## Overview
The **AI-Powered Resume Builder** is an intelligent web application designed to help users create professional resumes with AI-powered suggestions and structured formatting. It enhances resumes by recommending **industry-specific keywords**, improving sentence structure, and ensuring **ATS (Applicant Tracking System) compatibility**.

## Features
- **Interactive Form** – Users enter their details via a structured web form.
- **AI-Generated Resume** – Auto-formats input into a professional template.
- **Keyword Optimization** – Enhances resumes for ATS compatibility.
- **Template Selection** – Choose from multiple resume styles.
- **PDF/Word Export** – Download completed resumes in preferred formats.

## Tech Stack
- **Backend**: Flask / FastAPI
- **Frontend**: Streamlit / HTML, CSS, JavaScript
- **AI & NLP**: spaCy, NLTK, GPT-2 (for text optimization)
- **PDF Generation**: ReportLab, pdfkit

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ai-resume-builder.git
   cd ai-resume-builder
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Download the spaCy language model:
   ```sh
   python -m spacy download en_core_web_sm
   ```

## Usage
1. Run the application:
   ```sh
   streamlit run main.py
   ```
2. Navigate through the form sections:
   - Personal Information
   - Professional Experience
   - Education & Skills
   - Preview & Export
3. Fill in your details and apply AI-powered suggestions.
4. Choose a template and generate your resume.
5. Download the resume as a **PDF** or **Word** document.

## Project Structure
```
├── main.py                 # Main application file
├── utils/
│   ├── nlp_helper.py      # AI text processing
│   ├── pdf_generator.py   # PDF generation
│   └── resume_templates.py # Resume template definitions
├── assets/
│   └── custom.css         # Custom styling
├── requirements.txt       # Dependencies
```

## Contribution
Contributions are welcome! Feel free to submit **issues** and **pull requests**.

## License
This project is licensed under the **MIT License**.


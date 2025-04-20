import streamlit as st
import spacy
import pandas as pd
from utils.nlp_helper import get_keyword_suggestions, improve_text
from utils.pdf_generator import generate_pdf
from utils.resume_templates import TEMPLATES
import base64

# Load spaCy model
@st.cache_resource
def load_spacy():
    return spacy.load('en_core_web_sm')

nlp = load_spacy()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
local_css("assets/custom.css")

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = 1
    # Personal Information
    st.session_state.name = ""
    st.session_state.email = ""
    st.session_state.phone = ""
    st.session_state.location = ""
    st.session_state.summary = ""
    # Education
    st.session_state.degree = ""
    st.session_state.institution = ""
    st.session_state.grad_year = ""
    st.session_state.gpa = ""
    # Skills
    st.session_state.skills = ""

# App title and description
st.title("AI-Powered Resume Builder")
st.markdown("""
Create a professional resume with AI-powered suggestions and optimization.
Fill out the form below and let our AI help you build an impressive resume!
""")

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    step = st.radio("Go to:", 
                    ["1. Personal Information", 
                     "2. Professional Experience",
                     "3. Education & Skills",
                     "4. Preview & Export"],
                    index=st.session_state.step - 1)
    st.session_state.step = int(step[0])

# Personal Information
if st.session_state.step == 1:
    st.header("Personal Information")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.name = st.text_input("Full Name", value=st.session_state.name)
        st.session_state.email = st.text_input("Email", value=st.session_state.email)
    with col2:
        st.session_state.phone = st.text_input("Phone", value=st.session_state.phone)
        st.session_state.location = st.text_input("Location", value=st.session_state.location)

    st.session_state.summary = st.text_area("Professional Summary", value=st.session_state.summary)
    if st.session_state.summary:
        improved_summary = improve_text(st.session_state.summary, nlp)
        if improved_summary != st.session_state.summary:
            st.info("💡 Suggested improvement for your summary:")
            st.write(improved_summary)
            if st.button("Accept Suggestion"):
                st.session_state.summary = improved_summary

# Professional Experience
elif st.session_state.step == 2:
    st.header("Professional Experience")

    num_experiences = st.number_input("Number of experiences to add", 1, 5, 1)

    for i in range(num_experiences):
        st.subheader(f"Experience {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            company_key = f"company_{i}"
            position_key = f"position_{i}"
            if company_key not in st.session_state:
                st.session_state[company_key] = ""
            if position_key not in st.session_state:
                st.session_state[position_key] = ""
            st.session_state[company_key] = st.text_input("Company", key=f"company_input_{i}", value=st.session_state[company_key])
            st.session_state[position_key] = st.text_input("Position", key=f"position_input_{i}", value=st.session_state[position_key])
        with col2:
            start_date_key = f"start_date_{i}"
            end_date_key = f"end_date_{i}"
            if start_date_key not in st.session_state:
                st.session_state[start_date_key] = ""
            if end_date_key not in st.session_state:
                st.session_state[end_date_key] = ""
            st.session_state[start_date_key] = st.text_input("Start Date", key=f"start_date_input_{i}", value=st.session_state[start_date_key])
            st.session_state[end_date_key] = st.text_input("End Date", key=f"end_date_input_{i}", value=st.session_state[end_date_key])

        experience_key = f"experience_{i}"
        if experience_key not in st.session_state:
            st.session_state[experience_key] = ""
        st.session_state[experience_key] = st.text_area("Description", key=f"experience_input_{i}", value=st.session_state[experience_key])
        if st.session_state[experience_key]:
            suggestions = get_keyword_suggestions(st.session_state[experience_key], nlp)
            if suggestions:
                st.info("💡 Suggested keywords to include:")
                st.write(", ".join(suggestions))

# Education & Skills
elif st.session_state.step == 3:
    st.header("Education & Skills")

    st.subheader("Education")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.degree = st.text_input("Degree", value=st.session_state.degree)
        st.session_state.institution = st.text_input("Institution", value=st.session_state.institution)
    with col2:
        st.session_state.grad_year = st.text_input("Graduation Year", value=st.session_state.grad_year)
        st.session_state.gpa = st.text_input("GPA (optional)", value=st.session_state.gpa)

    st.subheader("Skills")
    st.session_state.skills = st.text_area("List your skills (comma-separated)", value=st.session_state.skills)
    if st.session_state.skills:
        skill_suggestions = get_keyword_suggestions(st.session_state.skills, nlp)
        if skill_suggestions:
            st.info("💡 Consider adding these relevant skills:")
            st.write(", ".join(skill_suggestions))

# Preview & Export
else:
    st.header("Preview & Export")

    template = st.selectbox("Select Template", list(TEMPLATES.keys()))

    if st.button("Generate Resume"):
        try:
            # Validate required fields
            if not st.session_state.name or not st.session_state.email:
                st.error("Please fill in at least your name and email in the Personal Information section.")
            else:
                # Convert session state to dictionary for PDF generation
                resume_data = {
                    "name": st.session_state.name,
                    "email": st.session_state.email,
                    "phone": st.session_state.phone,
                    "location": st.session_state.location,
                    "summary": st.session_state.summary,
                    "degree": st.session_state.degree,
                    "institution": st.session_state.institution,
                    "grad_year": st.session_state.grad_year,
                    "gpa": st.session_state.gpa,
                    "skills": st.session_state.skills
                }

                # Add experience entries
                for i in range(5):  # Support up to 5 experiences
                    if f"company_{i}" in st.session_state:
                        resume_data[f"company_{i}"] = st.session_state[f"company_{i}"]
                        resume_data[f"position_{i}"] = st.session_state[f"position_{i}"]
                        resume_data[f"start_date_{i}"] = st.session_state[f"start_date_{i}"]
                        resume_data[f"end_date_{i}"] = st.session_state[f"end_date_{i}"]
                        resume_data[f"experience_{i}"] = st.session_state[f"experience_{i}"]

                pdf_bytes = generate_pdf(template, resume_data)
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="resume.pdf">Download Resume PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Preview
                st.subheader("Preview")
                st.markdown("*This is a simplified preview. Download the PDF to see the full formatted resume.*")

                st.write("**" + resume_data["name"] + "**")
                st.write(resume_data["email"] + " | " + resume_data["phone"])
                st.write(resume_data["location"])
                st.write("---")
                st.write("**Professional Summary**")
                st.write(resume_data["summary"])

        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.step > 1:
        if st.button("Previous"):
            st.session_state.step -= 1
            st.rerun()
with col2:
    if st.session_state.step < 4:
        if st.button("Next"):
            st.session_state.step += 1
            st.rerun()



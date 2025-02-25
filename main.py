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

# App title and description
st.title("AI-Powered Resume Builder")
st.markdown("""
Create a professional resume with AI-powered suggestions and optimization.
Fill out the form below and let our AI help you build an impressive resume!
""")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1

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
        name = st.text_input("Full Name", key="name")
        email = st.text_input("Email", key="email")
    with col2:
        phone = st.text_input("Phone", key="phone")
        location = st.text_input("Location", key="location")
    
    professional_summary = st.text_area("Professional Summary", key="summary")
    if professional_summary:
        improved_summary = improve_text(professional_summary, nlp)
        if improved_summary != professional_summary:
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
            st.text_input("Company", key=f"company_{i}")
            st.text_input("Position", key=f"position_{i}")
        with col2:
            st.text_input("Start Date", key=f"start_date_{i}")
            st.text_input("End Date", key=f"end_date_{i}")
        
        experience = st.text_area("Description", key=f"experience_{i}")
        if experience:
            suggestions = get_keyword_suggestions(experience, nlp)
            if suggestions:
                st.info("💡 Suggested keywords to include:")
                st.write(", ".join(suggestions))

# Education & Skills
elif st.session_state.step == 3:
    st.header("Education & Skills")
    
    st.subheader("Education")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Degree", key="degree")
        st.text_input("Institution", key="institution")
    with col2:
        st.text_input("Graduation Year", key="grad_year")
        st.text_input("GPA (optional)", key="gpa")
    
    st.subheader("Skills")
    skills = st.text_area("List your skills (comma-separated)", key="skills")
    if skills:
        skill_suggestions = get_keyword_suggestions(skills, nlp)
        if skill_suggestions:
            st.info("💡 Consider adding these relevant skills:")
            st.write(", ".join(skill_suggestions))

# Preview & Export
else:
    st.header("Preview & Export")
    
    template = st.selectbox("Select Template", list(TEMPLATES.keys()))
    
    if st.button("Generate Resume"):
        try:
            pdf_bytes = generate_pdf(template, st.session_state)
            b64_pdf = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="resume.pdf">Download Resume PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # Preview
            st.subheader("Preview")
            st.markdown("*This is a simplified preview. Download the PDF to see the full formatted resume.*")
            
            st.write("**" + st.session_state.name + "**")
            st.write(st.session_state.email + " | " + st.session_state.phone)
            st.write(st.session_state.location)
            st.write("---")
            st.write("**Professional Summary**")
            st.write(st.session_state.summary)
            
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.step > 1:
        if st.button("Previous"):
            st.session_state.step -= 1
            st.experimental_rerun()
with col2:
    if st.session_state.step < 4:
        if st.button("Next"):
            st.session_state.step += 1
            st.experimental_rerun()

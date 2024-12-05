import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from keybert import KeyBERT
from jobspy import scrape_jobs
import pandas as pd
import re

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = "".join(page.extract_text() for page in reader.pages)
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# Preprocess function (clean and prepare text)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Streamlit App Configuration
st.set_page_config(page_title="Resume-Based Job Finder", layout="wide")

# Sidebar for Settings
st.sidebar.title("Job Finder Settings")
st.sidebar.markdown("### 🔍 Job Title Selection")

# Job Title Dropdown
job_titles = ["Data Analyst", "Software Engineer", "Project Manager", "Data Scientist", "Custom"]
selected_job_title = st.sidebar.selectbox("Select a Job Title", job_titles)

# Custom Job Title Input
custom_job_title = ""
if selected_job_title == "Custom":
    custom_job_title = st.sidebar.text_input("Enter a Custom Job Title:")
job_title_to_search = custom_job_title if selected_job_title == "Custom" else selected_job_title

# Main Page Layout
st.title("📄 Resume-Based Job Finder")
st.markdown("Upload your resume (PDF, TXT, or DOCX), and we will analyze it to find matching jobs!")
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("📤 Upload your resume:", type=["pdf", "txt", "docx"])

if uploaded_file:
    with st.spinner("Processing your resume..."):
        try:
            # Extract text based on file type
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a PDF, TXT, or DOCX file.")
                st.stop()

            # Preprocess the extracted text
            resume_text_cleaned = preprocess_text(resume_text)

            # Extract keywords using KeyBERT
            kw_model = KeyBERT()
            resume_keywords = [kw[0] for kw in kw_model.extract_keywords(resume_text_cleaned, keyphrase_ngram_range=(1, 2), top_n=10)]

            st.success("Resume processed successfully!")
            st.markdown("### 🗒️ Extracted Keywords:")
            st.write(", ".join(resume_keywords))

            # Display job title being searched
            st.markdown(f"### 🔎 Searching for jobs with the title: **{job_title_to_search}**")

            # Use jobspy to fetch jobs
            jobs = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
                search_term=job_title_to_search,
                google_search_term=f"{job_title_to_search} jobs near remote",
                location="remote",
                results_wanted=20,
                hours_old=72,
                country_indeed="USA",
            )

            # Debugging: Check the structure of the jobs object
            st.write("Jobs Object Debug:")
            if isinstance(jobs, pd.DataFrame):
                st.write(jobs.columns)
                st.write(jobs.head())
            else:
                st.write(jobs)

            # Display results
            if len(jobs) > 0:
                st.markdown("### 🎯 Top Matching Jobs:")
                for _, job in jobs.iterrows():
                    title = job.get("job_title", "N/A")
                    company = job.get("company", "N/A")
                    url = job.get("job_url", "#")
                    st.markdown(f"**💼 {title}** at **{company}**")
                    st.markdown(f"[🌐 Apply Here]({url})")
                    st.markdown("---")
            else:
                st.warning("No matching jobs found. Try adjusting your resume or keywords.")

            # Download button for job results
            st.markdown("### 📥 Download Job Results:")
            jobs_csv = jobs.to_csv(index=False)
            st.download_button("Download as CSV", data=jobs_csv, file_name="jobs.csv", mime="text/csv")

        except Exception as e:
            st.error(f"An error occurred: {e}")

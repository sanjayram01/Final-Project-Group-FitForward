import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from keybert import KeyBERT
from jobspy import scrape_jobs
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    if not isinstance(text, str):  # Handle non-string and NaN values
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Function to generate feedback based on keyword comparison
def generate_feedback(resume_keywords, job_keywords):
    resume_set = set(resume_keywords)
    job_set = set(job_keywords)
    missing_keywords = job_set - resume_set
    return missing_keywords

# Streamlit App Configuration
st.set_page_config(page_title="Resume-Based Job Finder with Feedback", layout="wide")

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
st.title("📄 FitForward")
st.markdown("Upload your resume (PDF, TXT, or DOCX), and we will analyze it to find the top 5 matching jobs and provide feedback!")
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
            st.markdown("### 🗒️ Extracted Keywords from Resume:")
            st.write(", ".join(resume_keywords))

            # Display job title being searched
            st.markdown(f"### 🔎 Searching for jobs with the title: **{job_title_to_search}**")

            # Use jobspy to fetch jobs
            jobs = scrape_jobs(
                site_name=["indeed", "zip_recruiter", "glassdoor", "google"],
                search_term=job_title_to_search,
                google_search_term=f"{job_title_to_search} jobs near remote",
                location="remote",
                results_wanted=20,
                hours_old=72,
                country_indeed="USA",
            )

            # Display the jobs DataFrame for debugging
            if isinstance(jobs, pd.DataFrame):
                st.write("Jobs Object Debug:")
                st.write(jobs.head())
            else:
                st.error("No jobs found. Please refine your search.")
                st.stop()

            # Check if the "description" column exists
            if "description" in jobs.columns:
                # Preprocess the descriptions and handle missing values
                jobs["description"] = jobs["description"].apply(preprocess_text)

                # Extract keywords from job descriptions
                jobs["job_keywords"] = jobs["description"].apply(
                    lambda desc: [kw[0] for kw in kw_model.extract_keywords(desc, keyphrase_ngram_range=(1, 2), top_n=10)]
                )

                # Compute cosine similarity between resume and job descriptions
                vectorizer = TfidfVectorizer()
                all_texts = [" ".join(resume_keywords)] + jobs["job_keywords"].apply(" ".join).tolist()
                tfidf_matrix = vectorizer.fit_transform(all_texts)

                # Calculate cosine similarity
                similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
                jobs["similarity_score"] = similarities

                # Sort jobs by similarity score in descending order
                top_jobs = jobs.sort_values(by="similarity_score", ascending=False).head(5)

                # Display top 5 jobs with feedback
                st.markdown("### 🎯 Top 5 Matching Jobs with Feedback:")
                for _, job in top_jobs.iterrows():
                    title = job.get("job_title", "N/A")
                    company = job.get("company", "N/A")
                    description = job.get("description", "No description available.")
                    similarity = job.get("similarity_score", 0) * 100
                    url = job.get("job_url", "#")
                    job_keywords = job.get("job_keywords", [])

                    # Generate feedback
                    missing_keywords = generate_feedback(resume_keywords, job_keywords)

                    st.markdown(f"**💼 {title}** at **{company}**")
                    st.markdown(f"**Similarity Score**: {similarity:.2f}%")
                    st.markdown(f"**Description**: {description[:200]}...")
                    st.markdown(f"[🌐 Apply Here]({url})")
                    st.markdown("#### 📝 Feedback:")
                    if missing_keywords:
                        st.write(f"Consider adding these keywords to your resume: {', '.join(missing_keywords)}")
                    else:
                        st.write("Your resume already matches this job description well!")
                    st.markdown("---")
            else:
                st.error("Job descriptions are not available. Cannot calculate ranking or feedback.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

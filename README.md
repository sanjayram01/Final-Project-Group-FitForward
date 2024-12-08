# **FitForward: Intelligent NLP-Based Resume Feedback System**

FitForward is an innovative project designed to enhance the job application experience for candidates by providing personalized feedback on their resumes. Leveraging natural language processing (NLP) techniques, this system compares candidate resumes against job descriptions, identifies skill gaps, and generates actionable feedback.

---

## **Key Features**
- **Resume Feedback System:** Automatically compares resumes with job descriptions to highlight areas of improvement.
- **Advanced NLP Techniques:** Utilizes Python, spaCy, and KeyBERT for extracting and analyzing keywords.
- **Cosine Similarity and TF-IDF:** Employs advanced text matching techniques to ensure precise evaluation of candidate suitability.
- **Personalized Feedback:** Generates meaningful and actionable feedback, enabling candidates to align their resumes better with job requirements.
- **PDF Resume Support:** Designed to process resumes uploaded in PDF format for seamless analysis.

---

## **Technical Highlights**
- **Data Processing:**
  - Analyzed over **200+ resumes** using job-specific keywords extracted with NLP techniques.
  - Extracted text and features from PDF resumes with PyPDF and spaCy preprocessing.
- **Machine Learning Integration:**
  - Achieved **85%+ accuracy** in matching resumes to job descriptions using Cosine Similarity and TF-IDF.
- **Feedback Categorization:**
  - Feedback includes categorized insights into technical skills, soft skills, and domain knowledge.
- **Streamlit Integration:**
  - User-friendly web interface built with Streamlit for uploading resumes and receiving feedback instantly.

---

## **How It Works**
1. **Upload Resume:** Candidates upload their resumes in PDF format.
2. **Input Job Description:** Job descriptions are either provided manually or preloaded from a dataset.
3. **Resume Analysis:**
   - Extracts and preprocesses the resume and job description text.
   - Calculates similarity scores using TF-IDF and Cosine Similarity.
4. **Feedback Generation:**
   - Identifies missing skills and provides actionable insights for improvement.
5. **Download Feedback:** Generates a downloadable report for candidates to review.

---

## **Technologies Used**
- **Programming Languages:** Python
- **Libraries:** spaCy, KeyBERT, PyPDF2, NLTK, Scikit-Learn
- **Machine Learning Techniques:** TF-IDF, Cosine Similarity
- **Web Framework:** Streamlit
- **Tools:** pandas, matplotlib, seaborn

---

## **Setup and Installation**
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/fitforward.git
   ```
2. Navigate to the project directory:  
   ```bash
   cd fitforward
   ```
3. Install required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:  
   ```bash
   streamlit run streamlit.py
   ```

---

## **Project Structure**
- **script.py:** Backend logic for processing resumes and generating feedback.
- **streamlit.py:** Frontend implementation for user interaction.
- **dataset/:** Directory containing sample resumes and job descriptions for testing.
- **feedback/:** Directory to store generated feedback reports.

---

## **Future Enhancements**
- Integrate feedback analysis for cover letters.
- Provide training recommendations for identified skill gaps.
- Expand system capabilities for real-time feedback on interviews.

---

## **Contributing**
Contributions are welcome! Please open an issue or submit a pull request if you'd like to enhance the project.

---

Let me know if you need further changes or additions! 🚀

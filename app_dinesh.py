import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
@st.cache_data
def load_feedback_data(file_path):
    return pd.read_csv(file_path)

# Path to your feedback CSV file
csv_file_path = "recommendation_feedback.csv"  # Update this path to match your file location
feedback_df = load_feedback_data(csv_file_path)

# App Title
st.title("Resume Feedback System")
st.header("Explore Feedback for Resumes and Job Descriptions")

# Display Data Overview
st.subheader("Feedback Data Overview")
st.write("Preview of the feedback data:")
st.dataframe(feedback_df.head())

# Filter by Resume_ID
st.subheader("Filter Feedback")
resume_id = st.selectbox("Select Resume ID:", feedback_df['Resume_ID'].unique())
filtered_df = feedback_df[feedback_df['Resume_ID'] == resume_id]

# Filter by Job Title (optional)
job_title = st.selectbox("Select Job Title:", filtered_df['Job_Title'].unique())
filtered_feedback = filtered_df[filtered_df['Job_Title'] == job_title]

# Display Filtered Feedback
st.subheader("Filtered Feedback")
st.write(f"### Feedback for Resume ID: {resume_id}, Job Title: {job_title}")
st.dataframe(filtered_feedback[['Feedback', 'Categorized_Feedback']])

# Visualize Categorized Feedback
st.subheader("Categorized Feedback Visualization")
categorized_feedback = filtered_feedback['Categorized_Feedback'].values[0]  # Take the first feedback entry
if pd.notna(categorized_feedback):
    # Convert string to dictionary
    import ast
    feedback_dict = ast.literal_eval(categorized_feedback)

    # Prepare data for visualization
    categories = list(feedback_dict.keys())
    counts = [len(feedback_dict[cat]) for cat in categories]

    # Create a bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(categories, counts, color='skyblue')
    plt.xlabel("Categories")
    plt.ylabel("Number of Keywords")
    plt.title("Categorized Feedback Analysis")
    st.pyplot(plt)
else:
    st.write("No categorized feedback available for this entry.")

# Download Filtered Feedback
st.subheader("Download Filtered Feedback")
csv_data = filtered_feedback.to_csv(index=False)
st.download_button("Download CSV", data=csv_data, file_name=f"{resume_id}_{job_title}_feedback.csv", mime="text/csv")

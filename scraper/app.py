import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper import scrape_indeed_jobs

st.set_page_config(page_title="Job Market Analyzer", layout="wide")
st.title("welcome to Job markeet")
st.title("🔍 Job Market Trend Analyzer")


# Try to load the data first
try:
    df = pd.read_csv("jobs.csv")
except:
    df = pd.DataFrame()  # empty dataframe if file not found

# Button to scrape latest jobs
if st.button("please click fetch for search latest job"):
    with st.spinner("Scraping jobs..."):
        df = scrape_indeed_jobs()
        df.to_csv("jobs.csv", index=False)
        st.success("Data fetched successfully!")

# Now check if df has data
if not df.empty:
    st.subheader("📊 Top 5 Most In-Demand Job Titles")
    top_titles = df['title'].value_counts().head(5)
    st.bar_chart(top_titles)

    st.subheader("📍 Cities with Most Openings")
    top_cities = df['location'].value_counts().head(5)
    st.bar_chart(top_cities)

    st.subheader("🕒 Posting Trend (based on date)")
    date_data = df['date_posted'].value_counts()
    st.line_chart(date_data)

    st.subheader("🔎 Filter By Keyword")
    keyword = st.text_input("Enter job keyword (e.g., Data Analyst)")
    if keyword:
        filtered = df[df['title'].str.contains(keyword, case=False, na=False)]
        st.write(filtered)
else:
    st.warning("No job data available. Please click 'Fetch Latest Jobs' to begin.")

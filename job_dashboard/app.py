import streamlit as st
import pandas as pd
import os

FILE_NAME = "data.csv"

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard"])

# ---------------- HOME ----------------
if page == "Home":
    st.title("Job Seeker Dashboard")
    st.write("""
    Welcome to the Job Seeker Dashboard!

    This application helps you:
    - Add job seeker details
    - Store multiple candidates
    - View all job seekers
    - Search and filter candidates

    Built using:
    - Streamlit (UI)
    - Pandas (Data handling)
    """)

elif page == "Dashboard":

    st.title("Dashboard")

    st.subheader("Add Seeker Details")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    skills = st.text_input("Enter skills (comma separated)")
    experience = st.number_input("Enter experience (in years)", min_value=0, step=1)
    location = st.text_input("Enter Location")

    submit = st.button("Submit")

    if submit:
        new_data = {
            "Name": name,
            "Email": email,
            "Skills": skills,
            "Experience": experience,
            "Location": location
        }

        df_new = pd.DataFrame([new_data])

        if os.path.exists(FILE_NAME):
            df = pd.read_csv(FILE_NAME)
            df = pd.concat([df, df_new], ignore_index=True)
        else:
            df = df_new

        df.to_csv(FILE_NAME, index=False)

        st.success("Data saved successfully!")

    st.subheader("All Job Seekers")

    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        st.dataframe(df)
    else:
        st.warning("No data available")

    st.sidebar.subheader("Search & Filter")

    search_name = st.sidebar.text_input("Search by Name")
    search_skill = st.sidebar.text_input("Filter by Skill")
    min_exp = st.sidebar.number_input("Minimum Experience", min_value=0, step=1)

    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        filtered_df = df.copy()

        if search_name:
            filtered_df = filtered_df[filtered_df["Name"].str.contains(search_name, case=False)]

        if search_skill:
            filtered_df = filtered_df[filtered_df["Skills"].str.contains(search_skill, case=False)]

        if min_exp > 0:
            filtered_df = filtered_df[filtered_df["Experience"] >= min_exp]

        st.subheader("Filtered Results")
        st.dataframe(filtered_df)
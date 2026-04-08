import streamlit as st
import json
import os
import pandas as pd
from groq import Groq

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Myer's College Admission Portal", layout="wide")

# -------------------- FILE SETUP --------------------
JSON_FILE = "applications.json"


def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    return []


def save_data(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)


# -------------------- GROQ SETUP --------------------
client = Groq(api_key="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")


def generate_summary(count):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"{count} students applied. Write a short 2-line summary."}],
            model="llama-3.1-8b-instant"
        )
        return response.choices[0].message.content
    except:
        return "AI summary unavailable."


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.image("logo.png", width=100)
    st.title("Myer's College")

    st.markdown("[Visit Website](https://myers.edu.pk)")
    st.info("Registration Fee: Rs. 300/-")

    st.success("Timings: 7AM - 1PM (SUMMER)")

    st.markdown("### 📘 Student Handbook")
    if os.path.exists("stdhbk(1).pdf"):
        with open("stdhbk(1).pdf", "rb") as file:
            st.download_button(
                label="Download Handbook",
                data=file,
                file_name="Student_Handbook.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Handbook file not found.")

    st.markdown("### 📰 Newsletter")
    st.markdown("[December 2025 Newsletter](https://www.myers.edu.pk/newsletterdec25.pdf)")

    mode = st.radio("Navigation", ["Student Registration", "Admin Panel"])


# -------------------- STUDENT REGISTRATION --------------------
if mode == "Student Registration":

    st.title("Online Admission Form")
    st.warning("Submission does not guarantee admission.")

    with st.form("admission_form"):

        st.subheader("Student Information")

        col1, col2 = st.columns(2)
        name = col1.text_input("Student Name")
        student_class = col2.selectbox("Class", [
            "K-1", "K-2", "K-3", "K-4",
            "E-1", "E-2", "E-3",
            "C-1", "C-2", "C-3",
            "M-1", "M-2", "M-3"
        ])

        col3, col4 = st.columns(2)
        dob = col3.date_input("Date of Birth")
        hospital = col4.text_input("Hospital of Birth")

        col5, col6 = st.columns(2)
        religion = col5.text_input("Religion")
        nationality = col6.text_input("Nationality")

        school = st.text_input("Current School")
        kinship = st.text_input("Kinship (If applicable)")

        st.subheader("Parents Information")

        col7, col8 = st.columns(2)
        father_name = col7.text_input("Father Name")
        father_cnic = col8.text_input("Father CNIC")

        col9, col10 = st.columns(2)
        mother_name = col9.text_input("Mother Name")
        mother_cnic = col10.text_input("Mother CNIC")

        col11, col12 = st.columns(2)
        father_job = col11.text_input("Father Occupation")
        mother_job = col12.text_input("Mother Occupation")

        address = st.text_area("Address")
        phone = st.text_input("Phone Number")

        st.subheader("Medical Information")

        diseases = st.multiselect(
            "Select Diseases",
            ["Measles", "Mumps", "Rubella", "Chicken Pox"]
        )

        fitness = st.radio("Fit for Physical Activities?", ["Yes", "No"])

        st.subheader("Agreement")
        agree = st.checkbox("I agree to the rules and regulations")

        submit = st.form_submit_button("Submit Application")

        if submit:
            if name and phone and agree:

                record = {
                    "name": name,
                    "class": student_class,
                    "dob": str(dob),
                    "hospital": hospital,
                    "religion": religion,
                    "nationality": nationality,
                    "school": school,
                    "father_name": father_name,
                    "father_cnic": father_cnic,
                    "mother_name": mother_name,
                    "mother_cnic": mother_cnic,
                    "father_job": father_job,
                    "mother_job": mother_job,
                    "address": address,
                    "phone": phone,
                    "medical": diseases,
                    "fitness": fitness,
                    "status": "Pending"
                }

                data = load_data()
                data.append(record)
                save_data(data)

                st.success("Application submitted successfully!")
            else:
                st.error("Please complete required fields.")


# -------------------- ADMIN PANEL --------------------
elif mode == "Admin Panel":

    st.title("Admin Dashboard")
    password = st.text_input("Enter Password", type="password")

    if password == "I @m N0t 2NE1":

        st.success("Access Granted")

        data = load_data()

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            if st.button("Generate AI Summary"):
                summary = generate_summary(len(data))
                st.info(summary)

        else:
            st.info("No applications submitted yet.")

    elif password:
        st.error("Incorrect Password")

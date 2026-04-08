import streamlit as st
import json
import os
from groq import Groq
import pandas as pd

# --- JSON FILE SETUP ---
JSON_FILE = "applications.json"

def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- GROQ AI SETUP ---
client = Groq(api_key="YOUR_API_KEY_HERE")

def get_ai_assistance(field_name):
    try:
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Explain why school needs {field_name} in 15 words."
            }],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content
    except:
        return "Fill according to official documents."

# --- PAGE CONFIG ---
st.set_page_config(page_title="Myer's College Admission Portal", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("logo.png", width=100)
    st.title("Myer's College")
    st.markdown("[Visit Website](https://myers.edu.pk)")
    st.info("Registration fee: Rs. 300/-")

    app_mode = st.radio("Navigate", ["Student Registration", "Admin Control"])

# --- STUDENT FORM ---
if app_mode == "Student Registration":

    st.title("Myer's College Online Admission Portal")
    st.warning("Registration does not guarantee admission.")

    with st.form("form"):

        st.subheader("1. Student Information")

        col1, col2 = st.columns(2)
        name = col1.text_input("Student Name")
        app_class = col2.selectbox("Class", ["K-1","K-2","K-3","K-4","E-1","E-2","E-3","C-1","C-2","C-3","M-1","M-2","M-3"])

        col3, col4 = st.columns(2)
        dob = col3.date_input("Date of Birth")
        hospital = col4.text_input("Hospital of Birth")

        col5, col6 = st.columns(2)
        religion = col5.text_input("Religion")
        nationality = col6.text_input("Nationality")

        school = st.text_input("Current School")

        st.subheader("2. Parents Information")

        col7, col8 = st.columns(2)
        f_name = col7.text_input("Father Name")
        f_nic = col8.text_input("Father CNIC")

        col9, col10 = st.columns(2)
        m_name = col9.text_input("Mother Name")
        m_nic = col10.text_input("Mother CNIC")

        col11, col12 = st.columns(2)
        f_occ = col11.text_input("Father Occupation")
        m_occ = col12.text_input("Mother Occupation")

        address = st.text_area("Address")
        phone = st.text_input("Phone Number")

        st.subheader("3. Medical Info")

        med = st.multiselect(
            "Diseases",
            ["Measles", "Mumps", "Rubella", "Chicken Pox"]
        )

        fit = st.radio("Fit for games?", ["Yes", "No"])

        st.subheader("4. Undertaking")
        agree = st.checkbox("I agree to rules")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if agree and name and phone:

                new_entry = {
                    "student_name": name,
                    "class": app_class,
                    "dob": str(dob),
                    "hospital": hospital,
                    "religion": religion,
                    "nationality": nationality,
                    "school": school,
                    "father_name": f_name,
                    "father_nic": f_nic,
                    "mother_name": m_name,
                    "mother_nic": m_nic,
                    "father_occ": f_occ,
                    "mother_occ": m_occ,
                    "address": address,
                    "phone": phone,
                    "medical": med,
                    "fit": fit,
                    "status": "Pending"
                }

                data = load_data()
                data.append(new_entry)
                save_data(data)

                st.success("Application submitted successfully!")

            else:
                st.error("Please fill required fields")

# --- ADMIN PANEL ---
elif app_mode == "Admin Control":

    st.title("Admin Panel")
    password = st.text_input("Password", type="password")

    if password == "I @m N0t 2NE1":

        st.success("Access Granted")

        data = load_data()

        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            if st.button("Generate AI Summary"):
                count = len(data)
                prompt = f"{count} students applied. Write 2-line summary."

                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )

                st.info(res.choices[0].message.content)

        else:
            st.info("No applications yet.")

    elif password:
        st.error("Wrong password")

import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('myers_admission.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS applications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 student_name TEXT, applying_class TEXT, dob TEXT, 
                 hospital TEXT, religion TEXT, current_school TEXT,
                 nationality TEXT, father_name TEXT, father_nic TEXT,
                 mother_name TEXT, mother_nic TEXT, father_occ TEXT,
                 mother_occ TEXT, address TEXT, phone TEXT,
                 medical_history TEXT, status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

init_db()

# --- GROQ AI HELPER ---
# Used to provide helpful tips to parents filling out the form
client = Groq(api_key="your_groq_api_key_here")

def get_ai_assistance(field_name):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Briefly explain why the school needs {field_name} in 15 words."}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content
    except:
        return "Please fill this field according to official documents."

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Myer's College Online Admission Portal", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("logo.png", width=100)
    st.title("Myer's College")
    st.markdown("[Visit Website](https://myers.edu.pk)")
    st.info("Registration fee: Rs. 300/- payable to the Principal.")
    
    app_mode = st.radio("Navigate", ["Student Registration", "Admin Control"])

# --- STUDENT REGISTRATION FORM ---
if app_mode == "Student Registration":
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo.png", width=80)
    with col2:
        st.title("Myer's College Online Admission Portal")
    
    st.warning("Note: Registration does not guarantee admission.")

    with st.form("admission_form"):
        st.subheader("1. The Student")
        c1, c2 = st.columns(2)
        name = c1.text_input("Student's Name (Block Letters)")
        app_class = c2.selectbox("Applying for Class", ["K-1", "K-2", "K-3", "K-4", "E-1", "E-2", "E-3", "C-1", "C-2", "C-3", "M-1", "M-2", "M-3"])
        
        c3, c4 = st.columns(2)
        dob = c3.date_input("Date of Birth")
        hospital = c4.text_input("Name of Hospital where born")
        
        c5, c6 = st.columns(2)
        religion = c5.text_input("Religion")
        nationality = c6.text_input("Nationality")
        curr_school = st.text_input("Present School of the Child")

        st.subheader("2. The Parents")
        p1, p2 = st.columns(2)
        f_name = p1.text_input("Father's Name")
        f_nic = p2.text_input("Father's Identity Card No")
        
        p3, p4 = st.columns(2)
        m_name = p3.text_input("Mother's Name")
        m_nic = p4.text_input("Mother's Identity Card No")
        
        p5, p6 = st.columns(2)
        f_occ = p5.text_input("Father's Occupation")
        m_occ = p6.text_input("Mother's Occupation")
        
        address = st.text_area("Present Address")
        phone = st.text_input("Mobile Number")

        st.subheader("3. Compulsory Medical Questionnaire")
        med_history = st.multiselect("Has the child had any of these diseases?", 
                                     ["Measles", "Mumps", "Rubella", "Chicken Pox"])
        fit_games = st.radio("Is the child fit for normal school games?", ["Yes", "No"])
        
        st.subheader("4. Undertaking")
        agree = st.checkbox("I undertake to conform to rules and understand that fees are payable till July.")

        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if agree and name and phone:
                conn = sqlite3.connect('myers_admission.db')
                c = conn.cursor()
                c.execute('''INSERT INTO applications 
                             (student_name, applying_class, dob, hospital, religion, 
                             current_school, nationality, father_name, father_nic, 
                             mother_name, mother_nic, father_occ, mother_occ, address, phone, medical_history) 
                             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                          (name, app_class, str(dob), hospital, religion, curr_school, 
                           nationality, f_name, f_nic, m_name, m_nic, f_occ, m_occ, 
                           address, phone, str(med_history)))
                conn.commit()
                conn.close()
                st.success("Application submitted successfully!")
            else:
                st.error("Please fill all required fields and accept the undertaking.")

# --- ADMIN CONTROL SIDE ---
elif app_mode == "Admin Control":
    st.title("Admin Control Panel")
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "I @m N0t 2NE1":
        st.success("Access Granted")
        
        conn = sqlite3.connect('myers_admission.db')
        df = pd.read_sql_query("SELECT * FROM applications", conn)
        conn.close()
        
        st.subheader("Registered Students")
        if not df.empty:
            st.dataframe(df)
            
            # AI Insights for Admin
            if st.button("Generate Admission Summary (AI)"):
                count = len(df)
                prompt = f"We have {count} new applicants for Myer's College. Write a professional 2-sentence summary for the Principal."
                res = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.1-8b-instant")
                st.info(res.choices[0].message.content)
        else:
            st.info("No applications found yet.")
    elif password:
        st.error("Incorrect Password")

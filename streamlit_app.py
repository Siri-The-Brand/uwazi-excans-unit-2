import streamlit as st
import pandas as pd
import time
import os
import uuid
from datetime import datetime

# File Paths
STUDENT_CSV = "students.csv"
TASKS_CSV = "tasks.csv"
SCORES_CSV = "scores.csv"
SUBMISSIONS_CSV = "submissions.csv"

# Initialize CSV Files if they do not exist
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

initialize_csv(STUDENT_CSV, ["Student Name", "Class Code"])
initialize_csv(TASKS_CSV, ["Student", "Task", "Day", "Time Block"])
initialize_csv(SCORES_CSV, ["Student", "XP", "Rating"])
initialize_csv(SUBMISSIONS_CSV, ["Student", "Task", "File Type", "File Name", "Submission Time"])

# Generate Unique Codes
def generate_code():
    return str(uuid.uuid4())[:6]

# XP & Umeme Points System
def calculate_xp(cse_rating):
    return {"Excellent": 30, "Great": 20, "Good": 15, "Needs Improvement": 5}.get(cse_rating, 0)

def calculate_umeme(start_time, end_time):
    time_taken = (end_time - start_time).total_seconds() / 60  # Time in minutes
    if time_taken <= 10:
        return 15
    elif time_taken <= 20:
        return 10
    else:
        return 5

# Streamlit App Configuration
st.set_page_config(page_title="Uwazi Unit 2", page_icon="🎭", layout="wide")
st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# Define Unit Schedule
unit_schedule = {
    "Day 1": [
        ("Soma Time", "Logical Problem-Solving"),
        ("Siri Time", "Creative Motion Expression"),
        ("Solver Time", "Team Challenge"),
        ("Soma Time", "Numerical Analysis"),
        ("Siri Time", "Balance & Coordination"),
        ("Solver Time", "Puzzle Deduction")
    ],
    "Day 2": [
        ("Soma Time", "Inductive Reasoning"),
        ("Siri Time", "Acrobatic Challenge"),
        ("Solver Time", "Physical Coordination"),
        ("Soma Time", "Pattern Recognition"),
        ("Siri Time", "Statistical Analysis"),
        ("Solver Time", "Critical Thinking")
    ],
    "Day 3": [
        ("Soma Time", "Mathematical Operations"),
        ("Siri Time", "Dexterity Challenge"),
        ("Solver Time", "Strategic Thinking"),
        ("Soma Time", "Abstract Reasoning"),
        ("Siri Time", "Reflex & Speed Test"),
        ("Solver Time", "Real-World Simulation")
    ]
}

# Sidebar Navigation
menu_option = st.sidebar.radio("Navigation", ["🏫 Class Management", "📅 View Unit 2 Schedule", "🎓 Student Dashboard", "📊 CSE Dashboard", "🔐 Admin Dashboard"])

if menu_option == "📅 View Unit 2 Schedule":
    st.markdown("### 📅 Unit 2 Full Schedule")
    selected_day = st.selectbox("Choose a Day", list(unit_schedule.keys()))
    st.markdown(f"## {selected_day}")
    day_schedule = unit_schedule[selected_day]
    schedule_df = pd.DataFrame(day_schedule, columns=["Time Block", "Task"])
    st.dataframe(schedule_df)
    if st.button(f"Start {selected_day}"):
        st.success(f"✅ You have started {selected_day}!")

elif menu_option == "🏫 Class Management":
    st.markdown("### 🏫 Manage Your Class")
    cse_name = st.text_input("Enter Your Name (CSE)")
    class_code = st.text_input("Enter Class Code to Create")
    
    if st.button("Create Class"):
        st.success(f"✅ Class {class_code} Created! Students can now join using this code.")

elif menu_option == "📊 CSE Dashboard":
    st.markdown("### 📊 Evaluate Student Performance")
    student_df = pd.read_csv(STUDENT_CSV)
    student_names = student_df["Student Name"].tolist() if not student_df.empty else []
    selected_student = st.selectbox("Select Student", student_names)
    rating = st.selectbox("Select Rating", ["Excellent", "Great", "Good", "Needs Improvement"])
    xp_awarded = calculate_xp(rating)
    
    if st.button("Save Rating"):
        df = pd.read_csv(SCORES_CSV)
        new_entry = pd.DataFrame({"Student": [selected_student], "XP": [xp_awarded], "Rating": [rating]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(SCORES_CSV, index=False)
        st.success(f"✅ Rating Saved! {selected_student} earned {xp_awarded} XP!")
    
    st.markdown("### 📸 🎥 View Student Submissions")
    submissions_df = pd.read_csv(SUBMISSIONS_CSV)
    st.dataframe(submissions_df)

elif menu_option == "🔐 Admin Dashboard":
    st.markdown("### 🔐 Admin Dashboard")
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    if admin_password == "siriadmin123":
        st.success("✅ Admin Access Granted!")
        df_scores = pd.read_csv(SCORES_CSV)
        st.dataframe(df_scores)
        st.download_button("Download CSV", df_scores.to_csv(index=False), "scores.csv", "text/csv")

elif menu_option == "🎓 Student Dashboard":
    st.markdown("### 📝 Join Class & Start Task")
    student_name = st.text_input("Enter Your Name (Siri Solver)")
    class_code = st.text_input("Enter Class Code")
    
    if st.button("Join Class"):
        df = pd.read_csv(STUDENT_CSV)
        new_entry = pd.DataFrame({"Student Name": [student_name], "Class Code": [class_code]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(STUDENT_CSV, index=False)
        st.success(f"✅ {student_name} joined class {class_code}!")

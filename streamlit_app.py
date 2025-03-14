import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

# File Paths
STUDENT_CSV = "students.csv"
TASKS_CSV = "tasks.csv"
SCORES_CSV = "scores.csv"
SUBMISSIONS_CSV = "submissions.csv"
CLASSES_CSV = "classes.csv"
SCHEDULE_CSV = "unit_schedule.csv"

# Initialize CSV Files if they do not exist
def initialize_csv(file_path, columns):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

initialize_csv(STUDENT_CSV, ["Student Name", "Class Code"])
initialize_csv(TASKS_CSV, ["Class Code", "Task", "Time Block"])
initialize_csv(SCORES_CSV, ["Student", "XP", "Rating"])
initialize_csv(SUBMISSIONS_CSV, ["Student", "Task", "File Type", "File Name", "Submission Time"])
initialize_csv(CLASSES_CSV, ["Class Code", "CSE Name", "Time Block"])

# Load schedule from CSV
@st.cache_data
def load_schedule():
    return pd.read_csv(SCHEDULE_CSV)

unit_schedule_df = load_schedule()

# XP System
def calculate_xp(cse_rating):
    return {"Excellent": 30, "Great": 20, "Good": 15, "Needs Improvement": 5}.get(cse_rating, 0)

# Streamlit UI
st.set_page_config(page_title="Uwazi Tasks", page_icon="📝", layout="wide")
st.title("📚 Uwazi Learning Platform")

menu_option = st.sidebar.radio("Navigation", ["🏫 Class Management", "📅 View Unit Schedule", "📅 Assign & View Tasks", "🎓 Student Dashboard", "📊 CSE Dashboard"])

if menu_option == "📅 View Unit Schedule":
    st.markdown("### 📅 Full Schedule")
    selected_day = st.selectbox("Choose a Day", unit_schedule_df["Day"].unique())
    day_schedule = unit_schedule_df[unit_schedule_df["Day"] == selected_day]
    st.dataframe(day_schedule)

elif menu_option == "🏫 Class Management":
    st.subheader("🏫 Create a Class")
    cse_name = st.text_input("Enter Your Name (CSE)")
    class_code = st.text_input("Enter Class Code")
    
    selected_day = st.selectbox("Select Day", unit_schedule_df["Day"].unique())
    available_time_blocks = unit_schedule_df[unit_schedule_df["Day"] == selected_day]["Time Block"].unique()
    time_block = st.selectbox("Select Time Block", available_time_blocks)
    
    if st.button("Create Class"):
        df = pd.read_csv(CLASSES_CSV)
        new_entry = pd.DataFrame({"Class Code": [class_code], "CSE Name": [cse_name], "Time Block": [time_block]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(CLASSES_CSV, index=False)
        st.success(f"✅ Class {class_code} created with {time_block} on {selected_day}!")

elif menu_option == "📅 Assign & View Tasks":
    st.subheader("📅 Assign Tasks to Class")
    class_df = pd.read_csv(CLASSES_CSV)
    class_codes = class_df["Class Code"].tolist()
    selected_class = st.selectbox("Select Class", class_codes)
    task_description = st.text_area("Enter Task Description")
    
    if st.button("Assign Task"):
        df = pd.read_csv(TASKS_CSV)
        time_block = class_df[class_df["Class Code"] == selected_class]["Time Block"].values[0]
        new_entry = pd.DataFrame({"Class Code": [selected_class], "Task": [task_description], "Time Block": [time_block]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(TASKS_CSV, index=False)
        st.success("✅ Task Assigned Successfully!")

elif menu_option == "🎓 Student Dashboard":
    st.subheader("🎓 Join Class & View Tasks")
    student_name = st.text_input("Enter Your Name (Student)")
    class_code = st.text_input("Enter Class Code")
    
    if st.button("Join Class"):
        df = pd.read_csv(STUDENT_CSV)
        new_entry = pd.DataFrame({"Student Name": [student_name], "Class Code": [class_code]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(STUDENT_CSV, index=False)
        st.success(f"✅ {student_name} joined class {class_code}!")
    
    st.subheader("📌 View Assigned Tasks")
    task_df = pd.read_csv(TASKS_CSV)
    student_tasks = task_df[task_df["Class Code"] == class_code]
    st.dataframe(student_tasks)

elif menu_option == "📊 CSE Dashboard":
    st.subheader("📊 Evaluate Student Submissions")
    submissions_df = pd.read_csv(SUBMISSIONS_CSV)
    st.dataframe(submissions_df)
    
    st.subheader("⭐ Rate & Award XP")
    student_names = submissions_df["Student"].unique().tolist()
    selected_student = st.selectbox("Select Student", student_names)
    rating = st.selectbox("Select Rating", ["Excellent", "Great", "Good", "Needs Improvement"])
    xp_awarded = calculate_xp(rating)
    
    if st.button("Save Rating"):
        df = pd.read_csv(SCORES_CSV)
        new_entry = pd.DataFrame({"Student": [selected_student], "XP": [xp_awarded], "Rating": [rating]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(SCORES_CSV, index=False)
        st.success(f"✅ Rating Saved! {selected_student} earned {xp_awarded} XP!")

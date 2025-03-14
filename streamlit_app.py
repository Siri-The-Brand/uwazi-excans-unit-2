import streamlit as st
import pandas as pd
import time
import os
import uuid
from datetime import datetime

# --------------------------
# FILE PATHS
# --------------------------
STUDENT_CSV = "students.csv"
TASKS_CSV = "tasks.csv"
SCORES_CSV = "scores.csv"
SUBMISSIONS_CSV = "submissions.csv"

# --------------------------
# INITIALIZE CSV FILES
# --------------------------
def initialize_csv(file_path, columns):
    """Creates an empty CSV with the given columns if it does not exist."""
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

# Adjust columns to accommodate Umeme in scores and Start Time in submissions
initialize_csv(STUDENT_CSV, ["Student Name", "Class Code"])
initialize_csv(TASKS_CSV, ["Student", "Task", "Day", "Time Block"])
initialize_csv(SCORES_CSV, ["Student", "XP", "Rating", "Umeme"])  # Added "Umeme" column
initialize_csv(SUBMISSIONS_CSV, ["Student", "Task", "File Type", "File Name", 
                                 "Submission Time", "Start Time", "Day", "Time Block"])  # Added "Start Time", "Day", "Time Block"

# --------------------------
# HELPER FUNCTIONS
# --------------------------
def generate_code():
    """Generates a short unique code."""
    return str(uuid.uuid4())[:6]

def calculate_xp(cse_rating):
    """Maps CSE rating to XP."""
    xp_map = {
        "Excellent": 30,
        "Great": 20,
        "Good": 15,
        "Needs Improvement": 5
    }
    return xp_map.get(cse_rating, 0)

def calculate_umeme(start_time, end_time):
    """
    Calculates Umeme points based on how quickly
    (in minutes) the student submits after starting.
    """
    time_taken = (end_time - start_time).total_seconds() / 60.0
    if time_taken <= 10:
        return 15
    elif time_taken <= 20:
        return 10
    else:
        return 5

# --------------------------
# STREAMLIT CONFIG & HEADER
# --------------------------
st.set_page_config(page_title="Uwazi Unit 2", page_icon="🎭", layout="wide")
st.title("🌟 Uwazi Unit 2: Theatrical Innovations")
st.subheader("Building Certitude Through Logic, Motion & Creative Expression")

# --------------------------
# DEFINE UNIT SCHEDULE
# --------------------------
unit_schedule = {
    "Day 1": [
        ["LM Soma Time", "Logical Problem-Solving", "Building blocks, puzzles, problem-solving worksheets"],
        ["KIN Siri Time", "Creative Motion Expression", "Music, scarves, props for expression exercises"],
        ["KIN Solver Time", "Team Challenge", "Cooperative challenge materials (ropes, small objects for team tasks)"],
        ["LM Soma Time", "Numerical Analysis", "Graph paper, calculators, data analysis charts"],
        ["KIN Siri Time", "Balance & Coordination", "Balance beams, agility ladders, small cones"],
        ["LM Solver Time", "Puzzle Deduction", "Jigsaw puzzles, logic problem cards"]
    ],
    "Day 2": [
        ["LM Soma Time", "Inductive Reasoning", "Pattern blocks, prediction exercises"],
        ["KIN Siri Time", "Acrobatic Challenge", "Exercise mats, safety pads"],
        ["KIN Solver Time", "Physical Coordination", "Jump ropes, reaction speed tools"],
        ["LM Soma Time", "Pattern Recognition", "Color sorting games, sequencing cards"],
        ["LM Siri Time", "Statistical Analysis", "Bar charts, statistical datasets"],
        ["LM Solver Time", "Critical Thinking", "Case study problems, debate prompts"]
    ],
    "Day 3": [
        ["LM Soma Time", "Mathematical Operations", "Math manipulatives, counters"],
        ["KIN Siri Time", "Dexterity Challenge", "Fine motor skill activities (clay, threading beads)"],
        ["LM Solver Time", "Strategic Thinking", "Board games, scenario-based challenges"],
        ["LM Soma Time", "Abstract Reasoning", "Optical illusions, abstract art exploration"],
        ["KIN Siri Time", "Reflex & Speed Test", "Stopwatches, fast-paced movement drills"],
        ["Solver Time", "Real-World Simulation", "VR headset or interactive AR experience for simulations"]
    ],
    "Day 4 - Field Trip": [
        ["Soma & Siri Time", "Field Trip to Observe Real-World Practitioners", 
         "Visit a Science Lab, Math Museum, or Acrobatics Training Center"],
        ["Solver Time", "Hands-on Industry Engagement", 
         "Interview professionals using Kinesthetic and Logical-Mathematical Intelligence"],
        ["Siri Time", "Reflection & Discussion", "Journaling and group discussion on field trip learnings"]
    ]
}

# --------------------------
# SIDEBAR NAVIGATION
# --------------------------
menu_option = st.sidebar.radio("Navigation", [
    "🏫 Class Management",
    "📅 View Unit 2 Schedule",
    "🎓 Student Dashboard",
    "📊 CSE Dashboard",
    "🔐 Admin Dashboard"
])

# --------------------------
# VIEW UNIT 2 SCHEDULE
# --------------------------
if menu_option == "📅 View Unit 2 Schedule":
    st.markdown("### 📅 Unit 2 Full Schedule")
    selected_day = st.selectbox("Choose a Day", list(unit_schedule.keys()))
    
    day_schedule = unit_schedule[selected_day]
    schedule_df = pd.DataFrame(day_schedule, columns=["Time Block", "Task", "Resources Needed"])
    
    st.markdown(f"## {selected_day}")
    st.dataframe(schedule_df)
    
    # Let user also pick a specific Time Block to "start" a session
    time_blocks = schedule_df["Time Block"].unique()
    selected_time_block = st.selectbox("Choose a Time Block", time_blocks)
    
    if st.button("Start Session"):
        # We can store the active session in Streamlit's session state (optional).
        st.session_state["active_day"] = selected_day
        st.session_state["active_time_block"] = selected_time_block
        st.success(f"✅ You have started a session for **{selected_day} - {selected_time_block}**!")

# --------------------------
# CLASS MANAGEMENT (CREATE CLASS)
# --------------------------
elif menu_option == "🏫 Class Management":
    st.markdown("### 🏫 Manage Your Class")
    cse_name = st.text_input("Enter Your Name (CSE)")
    class_code = st.text_input("Enter Class Code to Create")
    
    if st.button("Create Class"):
        # You could store this in a dedicated "classes.csv" if you want to track all classes
        st.success(f"✅ Class '{class_code}' created by CSE '{cse_name}'! Students can now join using this code.")

# --------------------------
# CSE DASHBOARD
# --------------------------
elif menu_option == "📊 CSE Dashboard":
    st.markdown("## 📊 CSE Dashboard")
    
    # 1) Assign Tasks to Students
    st.markdown("### Assign Tasks to Students")
    student_df = pd.read_csv(STUDENT_CSV)
    if student_df.empty:
        st.warning("No students have joined any classes yet.")
    else:
        # Let CSE pick which student to assign, along with Day, Time Block, Task name
        all_students = student_df["Student Name"].unique().tolist()
        selected_student = st.selectbox("Select Student", all_students)
        
        # Choose from known days in the schedule
        day_choice = st.selectbox("Select Day", list(unit_schedule.keys()))
        # Once a day is picked, show possible time blocks
        day_sched = unit_schedule[day_choice]
        day_sched_df = pd.DataFrame(day_sched, columns=["Time Block", "Task", "Resources"])
        block_choice = st.selectbox("Select Time Block", day_sched_df["Time Block"].unique())
        
        # Let CSE type a custom task name or pick from the day's listed tasks
        default_tasks = day_sched_df["Task"].unique().tolist()
        task_choice = st.selectbox("Select or Type Task", default_tasks + ["(custom)"])
        custom_task = ""
        if task_choice == "(custom)":
            custom_task = st.text_input("Enter Custom Task Name")
        
        if st.button("Assign Task"):
            task_to_assign = custom_task if custom_task else task_choice
            df_tasks = pd.read_csv(TASKS_CSV)
            new_task = pd.DataFrame({
                "Student": [selected_student],
                "Task": [task_to_assign],
                "Day": [day_choice],
                "Time Block": [block_choice]
            })
            df_tasks = pd.concat([df_tasks, new_task], ignore_index=True)
            df_tasks.to_csv(TASKS_CSV, index=False)
            st.success(f"✅ Assigned task '{task_to_assign}' to {selected_student} for {day_choice} - {block_choice}.")

    # 2) Evaluate / Rate Student Submissions
    st.markdown("---")
    st.markdown("### Evaluate Student Performance")
    
    # Show submissions
    submissions_df = pd.read_csv(SUBMISSIONS_CSV)
    if submissions_df.empty:
        st.info("No submissions yet.")
    else:
        st.markdown("#### All Student Submissions")
        st.dataframe(submissions_df)
        
        # Rate a particular student
        submission_students = submissions_df["Student"].unique()
        student_for_rating = st.selectbox("Select a Student to Rate", submission_students)
        
        # Rate
        rating = st.selectbox("Select Rating", ["Excellent", "Great", "Good", "Needs Improvement"])
        xp_awarded = calculate_xp(rating)
        
        if st.button("Save Rating"):
            # Save to Scores CSV
            df_scores = pd.read_csv(SCORES_CSV)
            new_entry = pd.DataFrame({
                "Student": [student_for_rating],
                "XP": [xp_awarded],
                "Rating": [rating],
                "Umeme": [0]  # default 0 unless you want to add more logic
            })
            df_scores = pd.concat([df_scores, new_entry], ignore_index=True)
            df_scores.to_csv(SCORES_CSV, index=False)
            st.success(f"✅ Rating Saved! {student_for_rating} earned {xp_awarded} XP!")

# --------------------------
# ADMIN DASHBOARD
# --------------------------
elif menu_option == "🔐 Admin Dashboard":
    st.markdown("### 🔐 Admin Dashboard")
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    if admin_password == "siriadmin123":
        st.success("✅ Admin Access Granted!")
        
        df_scores = pd.read_csv(SCORES_CSV)
        st.markdown("### Scores Overview")
        st.dataframe(df_scores)
        
        # Download option
        st.download_button(
            "Download Scoreboard",
            data=df_scores.to_csv(index=False),
            file_name="scores.csv",
            mime="text/csv"
        )
    else:
        st.info("Please enter the correct admin password.")

# --------------------------
# STUDENT DASHBOARD
# --------------------------
elif menu_option == "🎓 Student Dashboard":
    st.markdown("### 📝 Student Dashboard")
    st.markdown("Join a Class, View Tasks, and Submit Work!")

    # 1) Join Class
    student_name = st.text_input("Enter Your Name (Siri Solver)")
    class_code = st.text_input("Enter Class Code")
    
    if st.button("Join Class"):
        if student_name.strip() == "" or class_code.strip() == "":
            st.error("Please enter both your name and a class code.")
        else:
            df_students = pd.read_csv(STUDENT_CSV)
            # Check if already in the class
            existing = df_students[
                (df_students["Student Name"] == student_name) &
                (df_students["Class Code"] == class_code)
            ]
            if existing.empty:
                # Add the new student entry
                new_entry = pd.DataFrame({
                    "Student Name": [student_name],
                    "Class Code": [class_code]
                })
                df_students = pd.concat([df_students, new_entry], ignore_index=True)
                df_students.to_csv(STUDENT_CSV, index=False)
                st.success(f"✅ {student_name} joined class '{class_code}'!")
            else:
                st.info(f"You are already in class '{class_code}'.")

    st.markdown("---")
    
    # 2) View My Assigned Tasks
    st.markdown("### My Assigned Tasks")
    df_tasks = pd.read_csv(TASKS_CSV)
    
    # Filter tasks for this student
    my_tasks = df_tasks[df_tasks["Student"] == student_name]
    
    if my_tasks.empty:
        st.warning("No tasks assigned yet. Ask your CSE to assign tasks for you.")
    else:
        st.dataframe(my_tasks)
        
        # Let student pick one of their tasks
        task_options = my_tasks["Task"] + " | " + my_tasks["Day"] + " | " + my_tasks["Time Block"]
        selected_task_info = st.selectbox("Select a task to work on", task_options)
        
        if selected_task_info:
            # Parse out the actual row
            parsed_task = selected_task_info.split(" | ")
            chosen_task = parsed_task[0]
            chosen_day = parsed_task[1]
            chosen_block = parsed_task[2]
            
            # 3) Start Task (track start time in session_state)
            if st.button("Start Task"):
                st.session_state["start_time"] = datetime.now()
                st.success(f"Started task '{chosen_task}' at {st.session_state['start_time']}")
            
            # 4) Submit Work (upload file, calculate Umeme, store submission)
            uploaded_file = st.file_uploader("Upload your submission here", type=["png", "jpg", "pdf", "mp4", "mov", "txt", "docx"])
            
            if st.button("Submit Task"):
                if "start_time" not in st.session_state:
                    st.error("You must click 'Start Task' before submitting!")
                else:
                    end_time = datetime.now()
                    umeme_points = calculate_umeme(st.session_state["start_time"], end_time)
                    
                    if uploaded_file is not None:
                        file_type = os.path.splitext(uploaded_file.name)[1]
                        file_name = uploaded_file.name
                        submission_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                        start_time_str = st.session_state["start_time"].strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Save the file (optional) – or handle it as you wish:
                        # with open(os.path.join("submissions", file_name), "wb") as f:
                        #     f.write(uploaded_file.getbuffer())
                        
                        # Record submission in SUBMISSIONS_CSV
                        submissions_df = pd.read_csv(SUBMISSIONS_CSV)
                        new_sub = pd.DataFrame({
                            "Student": [student_name],
                            "Task": [chosen_task],
                            "File Type": [file_type],
                            "File Name": [file_name],
                            "Submission Time": [submission_time],
                            "Start Time": [start_time_str],
                            "Day": [chosen_day],
                            "Time Block": [chosen_block]
                        })
                        submissions_df = pd.concat([submissions_df, new_sub], ignore_index=True)
                        submissions_df.to_csv(SUBMISSIONS_CSV, index=False)
                        
                        # Also record Umeme in SCORES_CSV (XP & Rating = 0, to be assigned later by CSE)
                        scores_df = pd.read_csv(SCORES_CSV)
                        score_entry = pd.DataFrame({
                            "Student": [student_name],
                            "XP": [0],            # Default 0 until CSE rating
                            "Rating": [""],       # Blank until CSE rating
                            "Umeme": [umeme_points]
                        })
                        scores_df = pd.concat([scores_df, score_entry], ignore_index=True)
                        scores_df.to_csv(SCORES_CSV, index=False)
                        
                        st.success(f"✅ Submission successful! You earned {umeme_points} Umeme points.")
                        # Clear start_time from session so they can do a new task
                        del st.session_state["start_time"]
                    else:
                        st.error("Please upload a file before submitting.")

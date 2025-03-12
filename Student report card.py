import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile

# App Title
st.title("🎓 Student Report Card Generator App")

# About Section
st.sidebar.header("📌 About this App")
st.sidebar.write("This Student Report Card Management System helps in managing student academic records efficiently.")
st.sidebar.markdown("- Easily add student records with subject-wise marks.")
st.sidebar.markdown("- Automatically calculate total marks, percentage, and grades.")
st.sidebar.markdown("- Search and retrieve existing student records.")
st.sidebar.markdown("- Generate professional PDF report cards.")
st.sidebar.write("\n**Developed By**")
st.sidebar.write("Manahil Nadeem!")

# Initialize students list
if 'students' not in st.session_state:
    st.session_state.students = []

# Search Section
st.header("🔍 Search Existing Report Card")
search_name = st.text_input("Search by Name")
search_roll = st.text_input("Search by Roll Number")

# Add New Student
st.header("📝 Add New Student")
name = st.text_input("Enter Student Name")
roll_number = st.text_input("Enter Roll Number")
subjects = ["Math", "Physics", "Urdu", "English", "Computer"]
marks = {subject: st.number_input(f"Enter {subject} marks", min_value=0, max_value=100, step=1) for subject in subjects}

if st.button("Add Student"):
    total_marks = sum(marks.values())
    percentage = total_marks / len(subjects)
    
    grade = (
        "A+" if percentage >= 80 else
        "A" if percentage >= 70 else
        "B" if percentage >= 60 else
        "C" if percentage >= 50 else
        "F" if percentage >= 40 else
        "Fail"
    )
    
    student_data = {
        "Name": name,
        "Roll Number": roll_number,
        "Total Marks": total_marks,
        "Percentage": round(percentage, 2),
        "Grade": grade,
        **marks
    }
    st.session_state.students.append(student_data)
    st.success(f"Record of {name} inserted successfully!")
    
    more_input = st.radio("Do you want to insert more?", ("Yes", "No"))
    if more_input == "No":
        st.write("Proceeding to report generation...")

# Display All Student Records
st.header("\U0001F4C4 All Student Report Cards")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    st.table(df)
else:
    st.write("No student records available.")

# Function to Generate PDF
def generate_pdf(student):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Student Report Card", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Name: {student['Name']}", ln=True)
    pdf.cell(0, 10, f"Roll Number: {student['Roll Number']}", ln=True)
    pdf.cell(0, 10, f"Total Marks: {student['Total Marks']}", ln=True)
    pdf.cell(0, 10, f"Percentage: {student['Percentage']}%", ln=True)
    pdf.cell(0, 10, f"Grade: {student['Grade']}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Subject Wise Marks:", ln=True)
    pdf.set_font("Arial", "", 12)
    
    for subject in subjects:
        pdf.cell(0, 10, f"{subject}: {student[subject]}", ln=True)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# PDF Download Section
st.header("\U0001F4E5 Download Report Card")
if st.session_state.students:
    selected_student = st.selectbox("Select a student", [s["Name"] for s in st.session_state.students])
    if selected_student:
        student_data = next((s for s in st.session_state.students if s["Name"] == selected_student), None)
        if student_data:
            pdf_file = generate_pdf(student_data)
            with open(pdf_file, "rb") as f:
                st.download_button("Download Report Card", f, file_name=f"{selected_student}_Report_Card.pdf", mime="application/pdf")
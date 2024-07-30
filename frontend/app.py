import streamlit as st
import requests

st.title("MCQ Generator")

# Input for topic
topic = st.text_input("Enter a topic:")

# Initialize state variables
if 'question_data' not in st.session_state:
    st.session_state.question_data = None

if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# Button to generate MCQ
if st.button("Generate MCQ"):
    response = requests.post("https://backend-app1-0icr.onrender.com/generate/", json={"topic": topic})
    if response.status_code == 200:
        st.session_state.question_data = response.json()
        st.write("Question:", st.session_state.question_data["question"])
        options = st.session_state.question_data["options"]
        st.session_state.selected_option = None  # Reset selected option

    else:
        st.write("Error:", response.json().get("detail", "Unknown error"))

# Radio buttons for options
if st.session_state.question_data:
    options = st.session_state.question_data["options"]
    st.session_state.selected_option = st.radio("Choose your answer:", options, key="radio")

# Button to submit the answer
if st.session_state.question_data:
    if st.button("Submit Answer"):
        if st.session_state.selected_option:
            question_id = st.session_state.question_data["id"]
            submit_response = requests.post("https://backend-app1-0icr.onrender.com/submit_answer/", json={
                "question_id": question_id,
                "answer": st.session_state.selected_option
            })
            if submit_response.status_code == 200:
                st.write("Answer submitted successfully")
                st.session_state.question_data = None  # Clear the data after submission
                st.session_state.selected_option = None  # Clear the selected option
            else:
                st.write("Error:", submit_response.json().get("detail", "Unknown error"))
        else:
            st.write("Please select an answer before submitting.")

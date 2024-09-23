import streamlit as st
import pandas as pd
import speech_recognition as sr
import re

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("synthetic_patient_data_for_llm.csv", dtype=str)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

df = load_data()

st.title("Patient Status Query App with Voice Input")

# Function to find the patient ID column
def get_patient_id_column(df):
    possible_names = ['patient ID', 'patientID', 'patient_id', 'PatientID', 'Patient ID']
    for name in possible_names:
        if name in df.columns:
            return name
    return None

patient_id_column = get_patient_id_column(df)

# Voice recognition function
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now.")
        audio = r.listen(source)
        st.write("Processing speech...")
    try:
        text = r.recognize_google(audio)
        st.write(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        st.write("Sorry, there was an error with the speech recognition service.")
        return None

# Function to extract patient ID from voice input
def extract_patient_id(text):
    # Try to find a sequence of digits in the text
    match = re.search(r'\d+', text)
    if match:
        return match.group()
    return None

# Voice input for patient ID
if st.button("Use Voice for Patient ID"):
    voice_text = voice_input()
    if voice_text:
        patient_id = extract_patient_id(voice_text)
        if patient_id:
            st.session_state.patient_id = patient_id
            st.write(f"Extracted Patient ID: {patient_id}")
        else:
            st.write("Couldn't extract a numeric Patient ID from the voice input.")

# Text input for patient ID
patient_id = st.text_input("Enter Patient ID:", value=st.session_state.get('patient_id', ''))

# Voice input for question
if st.button("Use Voice for Question"):
    question = voice_input()
    if question:
        st.session_state.question = question

# Text input for question
question = st.text_input("Ask a question about the patient:", value=st.session_state.get('question', ''))

if st.button("Submit"):
    if patient_id and question:
        st.write(f"Searching for patient ID: {patient_id}")
        st.write(f"Question: {question}")
        
        patient = df[df[patient_id_column].astype(str) == str(patient_id).strip()]
        
        if not patient.empty:
            st.write("Patient found. Processing question...")
            if 'status' in question.lower():
                status_column = next((col for col in df.columns if 'etc' in col.lower()), None)
                if status_column:
                    status = patient[status_column].values[0]
                    st.write(f"The status of patient {patient_id} is: {status}")
                else:
                    st.write("Status information is not available in the dataset.")
            elif 'age' in question.lower():
                age_column = next((col for col in df.columns if 'age' in col.lower()), None)
                if age_column:
                    age = patient[age_column].values[0]
                    st.write(f"The age of patient {patient_id} is: {age}")
                else:
                    st.write("Age information is not available in the dataset.")
            elif 'name' in question.lower():
                first_name_col = next((col for col in df.columns if 'first' in col.lower() and 'name' in col.lower()), None)
                last_name_col = next((col for col in df.columns if 'last' in col.lower() and 'name' in col.lower()), None)
                if first_name_col and last_name_col:
                    first_name = patient[first_name_col].values[0]
                    last_name = patient[last_name_col].values[0]
                    st.write(f"The name of patient {patient_id} is: {first_name} {last_name}")
                else:
                    st.write("Name information is not available in the dataset.")
            else:
                st.write("I'm sorry, I don't understand that question. Please ask about status, age, or name.")
        else:
            st.write(f"No patient found with ID {patient_id}")
            st.write("Available patient IDs (first 10):", df[patient_id_column].head(10).tolist())
    else:
        st.write("Please enter both a patient ID and a question.")

# Display dataset info for debugging
st.write("Dataset Information:")
st.write(f"Number of rows: {len(df)}")
st.write(f"Columns: {df.columns.tolist()}")
st.write("First few rows of the dataset:")
st.write(df.head())

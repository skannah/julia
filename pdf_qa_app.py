import streamlit as st
import speech_recognition as sr
import PyPDF2
import io
from transformers import pipeline

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def main():
    st.title("PDF Q&A App with Voice Input")

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Initialize the question-answering pipeline
    qa_pipeline = pipeline("question-answering")

    # File uploader for PDF
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    if pdf_file is not None:
        text = extract_text_from_pdf(pdf_file)
        st.success("PDF successfully loaded and text extracted!")

        # Display a sample of the extracted text
        st.subheader("Sample of extracted text:")
        st.text(text[:500] + "...")

        # Question input
        question_input_method = st.radio("Choose question input method:", ("Text", "Voice"))

        if question_input_method == "Text":
            question = st.text_input("Enter your question about the PDF content:")
        else:
            if st.button("Start Voice Input for Question"):
                with sr.Microphone() as source:
                    st.write("Listening... Speak your question now!")
                    audio = recognizer.listen(source)
                
                try:
                    question = recognizer.recognize_google(audio)
                    st.write("You asked: ", question)
                except sr.UnknownValueError:
                    st.write("Sorry, I couldn't understand that.")
                    question = ""
                except sr.RequestError:
                    st.write("Sorry, there was an error with the speech recognition service.")
                    question = ""

        if question:
            # Perform question-answering
            answer = qa_pipeline(question=question, context=text)
            st.subheader("Answer:")
            st.write(answer['answer'])
            st.write(f"Confidence: {answer['score']:.2f}")

if __name__ == "__main__":
    main()
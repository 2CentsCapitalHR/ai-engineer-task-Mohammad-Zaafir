[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/vgbm4cZ0)
# ADGM Corporate Agent Prototype

## Project Overview
This project is a prototype for an AI-powered legal assistant designed to streamline the company incorporation process within the Abu Dhabi Global Market (ADGM) jurisdiction. It was developed to fulfill the requirements of the AI Engineer Intern take-home assignment.

The agent is built with a Python backend using LangChain and Google's Gemini models, with a user interface created using Gradio.

## Core Features Implemented

### 1. RAG-Powered Knowledge Base
- An AI knowledge base was successfully created using Retrieval-Augmented Generation (RAG).
- The engine processes official ADGM legal documents (`.pdf` and `.docx`) and stores them in a FAISS vector store, making them searchable for the AI.
- The core RAG query engine is demonstrated in `engine.py`.

### 2. Document Checklist Verification
- The primary feature, a "Document Checklist Verification" system, is fully functional in the `app.py` web interface.
- The application accepts multiple `.docx` files from a user.
- It uses a reliable keyword-based classifier to identify the type of each uploaded document (e.g., "Articles of Association," "Resolution for Incorporation").
- It compares the uploaded files against a master checklist for ADGM Company Incorporation and generates a clear report for the user, highlighting which documents are present and which are missing.

## Future Work (Next Steps)
The next logical step would be to integrate the RAG engine from `engine.py` into the main `app.py` to build out the "Red Flag Detection" feature. This would involve:
- Analyzing the content of the uploaded documents for legal inconsistencies.
- Inserting contextual comments directly into the `.docx` files.
- Generating a structured JSON report of all findings.

## How to Run the Application

1.  **Setup Environment**:
    - Clone the repository.
    - Create and activate a Python virtual environment.
    - Create a `.env` file and add your `GOOGLE_API_KEY`.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the Web App**:
    ```bash
    python app.py
    ```
    - Open the local URL provided in the terminal in your web browser.
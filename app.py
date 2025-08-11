import gradio as gr
import docx # To read .docx files
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration and Constants ---
# Load environment variables from .env file
load_dotenv()
try:
    # Configure the Gemini API with your key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    print("✅ Gradio App: API Key configured successfully!")
except Exception as e:
    print(f"❌ Gradio App: Error configuring API Key: {e}")

# This is the master checklist based on the task requirements
ADGM_INCORPORATION_CHECKLIST = [
    "Articles of Association",
    "Resolution for Incorporation",
    "Incorporation Application Form",
    "Register of Members and Directors",
    "UBO Declaration Form"
]

# --- AI Helper Function ---
def classify_doc_type(file_path):
    """Uses AI to classify the type of a single document."""
    try:
        doc = docx.Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        sample_text = full_text[:4000]

        # Reverting back to the 'flash' model which we know is accessible
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # This is a very strict, final prompt to get a clean answer
        prompt = f"""
        Analyze the following text from a legal document. Your task is to identify which of the following categories it belongs to. 
        Your response MUST BE ONLY ONE of these category names. Do not add any other words, explanations, or punctuation.

        Categories:
        - Articles of Association
        - Resolution for Incorporation
        - Standard Employment Contract
        - Register of Members and Directors
        - UBO Declaration Form
        - Other

        DOCUMENT TEXT:
        ---
        {sample_text}
        ---

        RESPONSE:
        """

        response = model.generate_content(prompt)
        raw_response = response.text.strip()
        print(f"Raw AI classification for '{os.path.basename(file_path)}' was: '{raw_response}'")

        known_types = [
            "Articles of Association", "Resolution for Incorporation", "Standard Employment Contract",
            "Register of Members and Directors", "UBO Declaration Form"
        ]

        for known_type in known_types:
            if known_type.lower() in raw_response.lower():
                print(f"Successfully matched as: '{known_type}'")
                return known_type

        print(f"Could not match response to a known type.")
        return "Other"

    except Exception as e:
        print(f"Error classifying document: {e}")
        return "Error"

# --- Main Gradio Function ---
def analyze_documents(files):
    """
    Performs the document checklist verification.
    """
    if not files:
        return "Please upload documents to analyze.", None

    # 1. Classify each uploaded document
    uploaded_doc_types = []
    for file in files:
        # Gradio gives us temporary file paths, which is what we need
        doc_type = classify_doc_type(file.name)
        if doc_type and doc_type not in ["Error", "Other"]:
            uploaded_doc_types.append(doc_type)

    # 2. Compare against the master checklist
    required = set(ADGM_INCORPORATION_CHECKLIST)
    uploaded = set(uploaded_doc_types)

    missing_docs = list(required - uploaded)

    # 3. Generate the report for the UI
    report = f"PROCESS: Company Incorporation\n\n"
    report += f"Uploaded Documents Found: {len(uploaded)} / {len(required)}\n"
    if uploaded:
        report += f" - " + "\n - ".join(sorted(list(uploaded))) + "\n\n"

    if missing_docs:
        report += f"MISSING DOCUMENTS:\n"
        report += f" - " + "\n - ".join(sorted(missing_docs))
    else:
        report += "All required documents for incorporation appear to be present!"

    return report, None # No file to download yet

# --- Gradio UI Definition ---
with gr.Blocks(title="ADGM Corporate Agent") as demo:
    gr.Markdown("# ADGM-Compliant Corporate Agent")
    gr.Markdown("Upload your `.docx` files for review. The agent will check for completeness against ADGM rules, identify red flags, and provide comments.")

    with gr.Row():
        with gr.Column():
            file_uploader = gr.Files(label="Upload .docx Documents", file_types=['.docx'])
            analyze_button = gr.Button("Analyze Documents", variant="primary")

        with gr.Column():
            output_report = gr.Textbox(label="Analysis Summary", lines=10, interactive=False)
            download_file = gr.File(label="Download Reviewed Document")

    analyze_button.click(
        fn=analyze_documents, 
        inputs=[file_uploader], 
        outputs=[output_report, download_file],
        show_progress="full"
    )

# --- Run the App ---
if __name__ == "__main__":
    demo.launch()
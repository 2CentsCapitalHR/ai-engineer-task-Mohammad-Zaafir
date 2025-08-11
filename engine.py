import os
import google.generativeai as genai
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain


def create_knowledge_base():
    """Creates the knowledge base if it doesn't exist."""
    if os.path.exists("faiss_index"):
        print("✅ Knowledge Base already exists. Skipping creation.")
        return

    print("--- Starting Knowledge Base creation ---")
    loader = DirectoryLoader('./data/', glob="**/*.*", use_multithreading=True, show_progress=True)
    print("Loading documents...")
    documents = loader.load()

    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print("Creating vector store...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local("faiss_index")
    print("✅ Knowledge Base created and saved successfully!")
    print("--- Knowledge Base creation complete ---")


def get_response_from_query(db, query):
    """Queries the knowledge base and returns a response."""
    docs = db.similarity_search(query, k=5)

    prompt_template = """
    You are a helpful and precise ADGM legal assistant. 
    Answer the question based only on the provided context. 
    If the answer is not in the context, say "I cannot answer this based on the provided documents."

    CONTEXT: {context}
    QUESTION: {question}

    ANSWER:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    response = chain.invoke({"input_documents": docs, "question": query})
    return response['output_text']


# --- Main execution block ---
if __name__ == "__main__":
    load_dotenv()
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        print("✅ API Key configured successfully!")
    except Exception as e:
        print(f"❌ Error configuring API Key: {e}")

    create_knowledge_base()

    print("\n--- Loading Knowledge Base ---")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    print("✅ Knowledge Base loaded successfully.")

    print("\n--- Querying the Agent ---")
    test_question = "What are the requirements for the Articles of Association for a Private Company?"
    print(f"QUESTION: {test_question}")

    response = get_response_from_query(db, test_question)
    print("\nANSWER:")
    print(response)
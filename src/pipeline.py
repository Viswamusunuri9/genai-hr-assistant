from src.loader import load_documents
from src.splitter import split_documents
from src.embeddings import create_vectorstore
from src.retriever import get_retriever
from src.llm import get_llm


def build_pipeline(pdf_path):
    docs = load_documents(pdf_path)
    chunks = split_documents(docs)
    db = create_vectorstore(chunks)
    retriever = get_retriever(db)
    llm = get_llm()
    return retriever, llm

def answer_query(query, retriever, llm):
    docs = retriever.invoke(query)
    # Keep only top meaningful chunks
    docs = docs[:4]

    # Filter weak results (important)
    docs = [doc for doc in docs if len(doc.page_content.strip()) > 50]

    if not docs:
        return "This information is not available in the provided HR policy document."
    context = ""
    sources = []

    for i, doc in enumerate(docs):
        context += f"\nChunk {i+1}:\n{doc.page_content}\n"
        sources.append(
            f"{doc.metadata.get('source', 'Unknown')} (chunk {i+1})"
        )

    prompt = f"""
    You are a strict HR policy assistant.

    Your job is to extract and explain policy details ONLY from the provided context.

    RULES:
    - Do NOT invent information
    - If answer is not clearly in context → say: "No relevant information found"
    - Provide structured answer:
        • Policy Overview
        • Key Rules / Conditions
        • Benefits (if any)
        • Eligibility (if any)
    - Be concise but complete
    - Use bullet points

    Context:
    {context}

    Question: {query}

    Answer:
    """
    response = llm.invoke(prompt)

    unique_sources = "\n".join(sorted(set(sources)))
    final_answer = f"{response.content}\n\n---\n**Sources:**\n{unique_sources}"
    
    return final_answer


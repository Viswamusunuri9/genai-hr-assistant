import streamlit as st
from src.pipeline import build_pipeline, answer_query

st.title("💼 AI HR Policy Assistant")

pdf_path = "data/the_nestle_hr_policy_pdf_2012.pdf"

# retriever, llm = build_pipeline(pdf_path)
@st.cache_resource
def load_pipeline():
    return build_pipeline("data/the_nestle_hr_policy_pdf_2012.pdf")

retriever, llm = load_pipeline()

query = st.text_input("Ask your HR question:")

if st.button("Ask"):
    answer = answer_query(query, retriever, llm)
    st.markdown(answer)
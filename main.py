import os
import pickle
import time

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

st.set_page_config(page_title="Equity Research Tool")
st.title("Equity Research Tool")
st.sidebar.title("Article URLs")

FILE_PATH = "faiss_store_grokai.pkl"
GROQ_MODEL = "openai/gpt-oss-120b"

main_placeholder = st.empty()


@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not set. Add it to your .env file.")
        st.stop()
    return ChatGroq(api_key=api_key, model_name=GROQ_MODEL, temperature=0.9, max_tokens=500)


if "url_count" not in st.session_state:
    st.session_state.url_count = 3

urls = []
for i in range(st.session_state.url_count):
    url = st.sidebar.text_input(f"URL {i + 1}", key=f"url_{i}")
    if url:
        urls.append(url)

col1, col2 = st.sidebar.columns(2)
if col1.button("Add URL"):
    st.session_state.url_count += 1
    st.rerun()
if col2.button("Remove URL") and st.session_state.url_count > 1:
    st.session_state.url_count -= 1
    st.rerun()

process_url_clicked = st.sidebar.button("Process URLs")
llm = get_llm()

if process_url_clicked:
    if not urls:
        st.sidebar.error("Enter at least one URL.")
    else:
        try:
            main_placeholder.text("Loading articles...")
            data = UnstructuredURLLoader(urls=urls).load()

            if not data:
                st.error("Could not extract content from the URLs provided.")
            else:
                splitter = RecursiveCharacterTextSplitter(
                    separators=["\n\n", "\n", ".", ","], chunk_size=1000
                )
                docs = splitter.split_documents(data)

                main_placeholder.text("Building embeddings...")
                vectorstore = FAISS.from_documents(docs, get_embeddings())

                with open(FILE_PATH, "wb") as f:
                    pickle.dump(vectorstore, f)

                main_placeholder.text("Ready. Ask a question below.")
                time.sleep(1)
                main_placeholder.empty()
        except Exception as e:
            st.error(f"Failed to process URLs: {e}")

query = st.text_input("Question")

if query:
    if not os.path.exists(FILE_PATH):
        st.warning("Process some article URLs first.")
    else:
        try:
            with open(FILE_PATH, "rb") as f:
                vectorstore = pickle.load(f)

            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain.invoke({"question": query}, return_only_outputs=True)

            st.header("Answer")
            st.write(result["answer"])

            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources")
                for source in sources.split("\n"):
                    if source.strip():
                        st.write(source)
        except Exception as e:
            st.error(f"Failed to answer question: {e}")

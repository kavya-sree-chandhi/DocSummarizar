import streamlit as st
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_groq import ChatGroq

st.set_page_config(page_title="Web Article Summarizer", page_icon="📰")
st.title("📰 Doc Summarizer")

# --- Groq LLM Setup ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Enter your Groq API Key:", type="password")
GROQ_MODEL = "llama3-8b-8192"

st.markdown("Paste any **web article URL** (e.g., Lilian Weng's agent post):")
url = st.text_input("Web URL", value="https://lilianweng.github.io/posts/2023-06-23-agent/")
chunk_size = st.number_input("Chunk size (characters)", min_value=300, max_value=3000, value=800, step=100)

if url and GROQ_API_KEY and st.button("Summarize and Stream!"):
    with st.spinner("Loading the web page..."):
        loader = WebBaseLoader(url)
        docs = loader.load()

    st.info("Loaded document preview:")
    st.code(docs[0].page_content[:500] + " ...", language="markdown")

    # --- Chunk the document ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    st.success(f"Split into {len(chunks)} chunks. Largest chunk length: {max(len(doc.page_content) for doc in chunks)}")

    # --- LLM and Chain Setup ---
    llm = ChatGroq(
        model_name=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.0,
    )
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\n\n{context}")]
    )
    chain = create_stuff_documents_chain(llm, prompt)

    st.markdown("### Summarizing Chunks")
    summaries = []
    progress = st.progress(0)
    status = st.empty()
    for i, doc in enumerate(chunks):
        status.write(f"Summarizing chunk {i+1}/{len(chunks)} ...")
        try:
            summary = chain.invoke({"context": [doc]})
            output = summary["output"] if isinstance(summary, dict) and "output" in summary else summary
            summaries.append(output)
        except Exception as e:
            st.warning(f"Error in chunk {i+1}: {e}")
            continue
        progress.progress((i+1)/len(chunks))
    status.write("Chunks summarized. Now streaming overall summary...")

    # --- Recursive Reduce to Avoid Token Limit ---
    def recursive_reduce(summaries, chain, batch_size=8):
        if len(summaries) <= batch_size:
            summary_docs = [Document(page_content="\n".join(summaries))]
            streamed_summary = ""
            stream_area = st.empty()
            for token in chain.stream({"context": summary_docs}):
                streamed_summary += token
                stream_area.markdown("**" + streamed_summary + "**")
            return streamed_summary
        next_level = []
        for i in range(0, len(summaries), batch_size):
            batch = summaries[i:i+batch_size]
            summary_docs = [Document(page_content="\n".join(batch))]
            summary_text = chain.invoke({"context": summary_docs})
            output = summary_text["output"] if isinstance(summary_text, dict) and "output" in summary_text else summary_text
            next_level.append(output)
        return recursive_reduce(next_level, chain, batch_size)

    if summaries:
        st.markdown("### Streaming Final Summary")
        streamed_summary = recursive_reduce(summaries, chain, batch_size=8)
        st.success("Done! Scroll up to see the streamed summary.")
    else:
        st.warning("No summaries to combine.")
else:
    st.info("Enter your Groq API key and a URL, then click 'Summarize and Stream!'")

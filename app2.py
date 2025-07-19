import streamlit as st
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import Document

def get_chunk_text(chunk):
    """Return text for a chunk (Document or string) - FIXED VERSION."""
    if hasattr(chunk, "page_content"):
        return chunk.page_content
    elif isinstance(chunk, str):
        return chunk
    else:
        return str(chunk)

st.set_page_config(page_title="Web Article Summarizer", page_icon="📰")
st.title("📰 Web Article Summarizer")

# --- Groq LLM Setup ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    GROQ_API_KEY = st.text_input("Enter your Groq API Key:", type="password")
GROQ_MODEL = "llama3-8b-8192"

st.markdown("Paste any **web article URL** (e.g., Lilian Weng's agent post):")
url = st.text_input("Web URL", value="https://lilianweng.github.io/posts/2023-06-23-agent/")
chunk_size = st.number_input("Chunk size (characters)", min_value=300, max_value=3000, value=800, step=100)

if url and GROQ_API_KEY and st.button("Summarize and Stream!"):
    try:
        with st.spinner("Loading the web page..."):
            loader = WebBaseLoader(url)
            docs = loader.load()

        if not docs:
            st.error("Could not load content from the URL. Please check the URL and try again.")
            st.stop()

        st.info("Loaded document preview:")
        preview_text = get_chunk_text(docs[0])[:500] + " ..." if len(get_chunk_text(docs[0])) > 500 else get_chunk_text(docs[0])
        st.code(preview_text, language="markdown")

        # --- Chunk the document ---
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        
        if not chunks:
            st.error("Could not create chunks from the document.")
            st.stop()
        
        largest_chunk_length = max(len(get_chunk_text(doc)) for doc in chunks)
        st.success(f"Split into {len(chunks)} chunks. Largest chunk length: {largest_chunk_length}")

        # --- LLM and Chain Setup ---
        try:
            llm = ChatGroq(
                model_name=GROQ_MODEL,
                api_key=GROQ_API_KEY,
                temperature=0.0,
            )
            prompt = ChatPromptTemplate.from_messages(
                [("system", "Write a concise summary of the following:\n\n{context}")]
            )
            chain = create_stuff_documents_chain(llm, prompt)
        except Exception as e:
            st.error(f"Error setting up LLM: {e}")
            st.stop()

        st.markdown("### Summarizing Chunks")
        summaries = []
        progress = st.progress(0)
        status = st.empty()
        
        for i, doc in enumerate(chunks):
            status.write(f"Summarizing chunk {i+1}/{len(chunks)} ...")
            try:
                # Ensure we pass the document correctly to the chain
                if hasattr(doc, 'page_content'):
                    # doc is already a Document object
                    summary = chain.invoke({"context": [doc]})
                else:
                    # Convert string to Document object
                    doc_obj = Document(page_content=str(doc), metadata={})
                    summary = chain.invoke({"context": [doc_obj]})
                
                # Extract the actual summary text
                if isinstance(summary, dict) and "output" in summary:
                    output = summary["output"]
                elif isinstance(summary, str):
                    output = summary
                else:
                    output = str(summary)
                
                summaries.append(output)
                
            except Exception as e:
                st.warning(f"Error in chunk {i+1}: {e}")
                # Continue with next chunk instead of stopping
                continue
                
            progress.progress((i+1)/len(chunks))
        
        status.write("Chunks summarized. Now streaming overall summary...")

        # --- Recursive Reduce to Avoid Token Limit ---
        def recursive_reduce(summaries, chain, batch_size=8):
            if not summaries:
                return "No summaries were generated."
            
            if len(summaries) <= batch_size:
                # Create Document objects from summary strings
                summary_docs = [Document(page_content=summary, metadata={}) for summary in summaries]
                
                streamed_summary = ""
                stream_area = st.empty()
                
                try:
                    for token in chain.stream({"context": summary_docs}):
                        if isinstance(token, str):
                            streamed_summary += token
                        elif isinstance(token, dict) and "output" in token:
                            streamed_summary += token["output"]
                        else:
                            streamed_summary += str(token)
                        stream_area.markdown("**" + streamed_summary + "**")
                    return streamed_summary
                except Exception as e:
                    st.error(f"Error during streaming: {e}")
                    # Fallback to non-streaming
                    try:
                        result = chain.invoke({"context": summary_docs})
                        if isinstance(result, dict) and "output" in result:
                            return result["output"]
                        return str(result)
                    except Exception as e2:
                        st.error(f"Fallback also failed: {e2}")
                        return "Error generating final summary."
            
            # Process in batches
            next_level = []
            for i in range(0, len(summaries), batch_size):
                batch = summaries[i:i+batch_size]
                batch_docs = [Document(page_content=summary, metadata={}) for summary in batch]
                
                try:
                    summary_result = chain.invoke({"context": batch_docs})
                    if isinstance(summary_result, dict) and "output" in summary_result:
                        output = summary_result["output"]
                    else:
                        output = str(summary_result)
                    next_level.append(output)
                except Exception as e:
                    st.warning(f"Error processing batch {i//batch_size + 1}: {e}")
                    continue
            
            return recursive_reduce(next_level, chain, batch_size)

        if summaries:
            st.markdown("### Streaming Final Summary")
            final_summary = recursive_reduce(summaries, chain, batch_size=8)
            st.success("Done! Final summary generated successfully.")
        else:
            st.error("No summaries were generated. Please try with a different URL or check your API key.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.info("Please try again or check your inputs.")

else:
    st.info("Enter your Groq API key and a URL, then click 'Summarize and Stream!'")

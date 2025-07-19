# 📰 Web Article Summarizer

A Streamlit app to **summarize any web article** using LangChain, Groq LLM, and advanced document chunking.  
Paste any URL, and get a concise, streamed summary—even for long articles!

---

## 📖 Introduction

This tool loads content from any public web URL, splits the article into manageable text chunks, summarizes each chunk using Groq’s Llama3 LLM, and then recursively combines these summaries to produce an overall summary.  
It’s ideal for quickly digesting long blog posts, tech articles, news stories, or documentation.

---

## 🚀 Features

- 🔗 **Summarize any web article:** Just paste a URL and click!
- 🦙 **Groq Llama3-powered:** Fast, concise AI summaries.
- 🔬 **Smart chunking:** Handles long articles and avoids token limits.
- 🧩 **Recursive reduction:** Ensures even huge articles get a final, readable summary.
- 🎛️ **Custom chunk size:** Adjustable to optimize for your articles.
- 💻 **Runs locally:** Your API key is never shared with us.

---
<img width="1631" height="181" alt="image" src="https://github.com/user-attachments/assets/3b9c927e-aa83-41d7-b105-d25126d390ba" />

<img width="1917" height="958" alt="image" src="https://github.com/user-attachments/assets/5f467218-52df-4854-8d83-99b4b16069b7" />

<img width="1918" height="965" alt="image" src="https://github.com/user-attachments/assets/2e28bde3-8522-470c-8bbe-9169e037b8c0" />

<img width="1918" height="968" alt="image" src="https://github.com/user-attachments/assets/92c5bcd1-6f2b-41b6-985e-76a4398089b6" />



## Visual Diagram

```mermaid
graph TD
    A[User enters web URL and API key] --> B[App loads and previews article content]
    B --> C[Document is split into text chunks]
    C --> D[Each chunk summarized by Groq LLM]
    D --> E[Chunk summaries recursively combined]
    E --> F[Final summary streamed to user]




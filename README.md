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
## How it Works:

1. **Launch the App**
The terminal displays both local and network URLs where you can access your app in a web browser.
<img width="1631" height="181" alt="image" src="https://github.com/user-attachments/assets/3b9c927e-aa83-41d7-b105-d25126d390ba" />

2. **Initial App Screen**
Enter your Groq API key. Enter any web article URL (for example, Lilian Weng's LLM agents post). Set your chunk size (how large each section of text will be for summarization). Click "Summarize and Stream!" to begin.
<img width="1917" height="958" alt="image" src="https://github.com/user-attachments/assets/5f467218-52df-4854-8d83-99b4b16069b7" />

3. **Document Preview & Ready to Summarize**
After clicking the button, the app fetches the article and shows a preview of the loaded text. This ensures the document was loaded successfully before summarization starts. 
<img width="1918" height="965" alt="image" src="https://github.com/user-attachments/assets/2e28bde3-8522-470c-8bbe-9169e037b8c0" />

4. **Chunking, Summarization, and Streaming Final Summary**
The article is split into chunks, and each chunk is summarized using the LLM. Progress bars and status messages show the summarization steps. The final summary of the entire article is streamed and displayed. A green confirmation message shows that summarization completed successfully.
<img width="1918" height="968" alt="image" src="https://github.com/user-attachments/assets/92c5bcd1-6f2b-41b6-985e-76a4398089b6" />


## Visual Diagram

```mermaid
flowchart TD
    A([Start App in Terminal]) --> B[Open App in Browser (localhost:8501)]
    B --> C[Enter Groq API Key]
    C --> D[Enter Web Article URL]
    D --> E[Set Chunk Size]
    E --> F[Click "Summarize and Stream!"]
    F --> G[Fetch & Preview Article Content]
    G --> H[Split Article into Chunks]
    H --> I[Summarize Each Chunk]
    I --> J[Stream and Display Final Summary]
    J --> K([Done! Summary Available])




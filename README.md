# PDFWhisperer

The latest version of the application has been deployed on streamlit cloud, and
can be accessed through this [link](https://pdf-whisperer.streamlit.app/) [WIP].

## Description

PDFWhisperer is a chatbot designed to extract and process information from PDF files, and to enable interactive 
chat sessions with the content of the PDFs. This project includes components for:

- PDF parsing
- Managing chat sessions
- Implementing a processing chain to facilitate user interactions with PDF content

**Purpose:** This project is a hands-on learning experience for exploring and mastering Generative AI tools
and technologies.

## Run on local

1. Install the dependencies using the following command:
```bash
pip install -r requirements.txt
```

2. Fill the .env file with the required credentials.
Sample file:
```
OPENROUTER_API_KEY=""
COHERE_API_KEY=""
GROQ_API_KEY=""
COOKIES_PASSWORD=""
```

3. Run the application using the following command:
```bash
streamlit run main.py
```

## Tools and Technologies
- PyMuPDF: Used for efficient PDF parsing.
- Langchain: Utilized for implementing the chatbot functionality.
- Streamlit: Powers the frontend interface.
- Groq cloud, Openrouter, Cohere: for accessing LLMs

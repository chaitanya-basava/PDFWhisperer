# PDFWhisperer

The latest version of the application has been deployed on streamlit cloud, and
can be accessed through this [link](https://pdf-whisperer.streamlit.app/).

## Description

PDFWhisperer is a chatbot designed to extract and process information from PDF files, and to enable interactive 
chat sessions with the content of the PDFs. This project includes components for:

- PDF parsing
- Managing chat sessions
- Implementing a processing chain to facilitate user interactions with PDF content

**Purpose:** This project is a hands-on learning experience for exploring and mastering Generative AI tools
and technologies. This project gives a hands-on experience on building Gen AI applications using retrieval
augmented generation (RAG).

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

## Future Scope

There are various ways to expand the project, such as:

- giving the llm access to internet using function calling
- converting the llm chain into an agent, allowing it to make its own decisions
- adding the ability to chat with multiple pdfs at once

Thanks for checking out the repository, feel free to connect with me on
[LinkedIn](https://www.linkedin.com/in/chaitu-basava/).

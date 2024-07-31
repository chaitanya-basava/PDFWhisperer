import fitz
import hashlib
from io import BytesIO
from typing import Optional, Tuple

from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_and_urls(
        uploaded_pdf: Optional[BytesIO] = None,
        pdf_path: Optional[str] = None
) -> str:
    doc = (
        fitz.open(pdf_path) if pdf_path
        else fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    )
    _text = ""

    for page in doc:
        # Extract text and append to the _text variable
        _text += page.get_text()

        # Extract links and the corresponding text
        links = page.get_links()
        for link in links:
            if "uri" in link and "from" in link:
                link_uri = link["uri"]
                link_rect = fitz.Rect(link["from"])

                link_text = page.get_text("text", clip=link_rect)
                # Append the link URI to the extracted text
                _text += f"\n{link_text} ({link_uri})"

    doc.close()
    return _text


def process_pdf(
        uploaded_pdf: Optional[BytesIO] = None,
        pdf_path: Optional[str] = None
) -> tuple[VectorStoreRetriever, str]:
    embeddings = CohereEmbeddings(model="embed-multilingual-v2.0")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    text = (
        extract_text_and_urls(pdf_path=pdf_path) if pdf_path
        else extract_text_and_urls(uploaded_pdf=uploaded_pdf)
    )
    chunks = text_splitter.split_text(text)

    vector_store = FAISS.from_texts(chunks, embeddings)
    retriever = vector_store.as_retriever()

    return retriever, generate_hashcode(text)


def generate_hashcode(text):
    return hashlib.md5(text.encode()).hexdigest()

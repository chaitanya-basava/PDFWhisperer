import os
import uuid
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from model import LLM
from chain import get_chain, generate_response
from pdf_parser import process_pdf
from session_manager import AutoExpireDict


if "llm" not in st.session_state:
    st.session_state.llm = LLM.get_llm(LLM.get_llm_by_id(2))

if "store" not in st.session_state:
    st.session_state.store = AutoExpireDict(1800, "auto_expire_dict.pkl", 10)

cookies = EncryptedCookieManager(
    prefix="pdf_whisperer_",
    password=os.environ.get("COOKIES_PASSWORD")
)

if not cookies.ready():
    st.stop()

if 'uuid' not in cookies:
    cookies['uuid'] = str(uuid.uuid4())
    cookies.save()

unique_id = cookies['uuid']


def main():
    st.title("PDF Whisperer")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        st.success("PDF file uploaded successfully.")
        retriever, hashcode = process_pdf(uploaded_pdf=uploaded_file)
        conversational_rag_chain = get_chain(st.session_state.llm, retriever, st.session_state.store)

        session_id = f"{hashcode}-{unique_id}"

        if "messages" not in st.session_state:
            st.session_state.messages = st.session_state.store.get_messages(session_id)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What do you want to know about this PDF?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = generate_response(conversational_rag_chain, prompt, session_id)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

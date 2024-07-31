import time
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever


contextualize_q_system_prompt = """Given a chat history and the latest user question which might reference context in 
the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the 
question, just reformulate it if needed and otherwise return it as is."""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

human_prompt = """
QUESTION: {input}
CONTEXT: {context}
"""

system_prompt = """You are an assistant for question-answering tasks. Provide a clear, direct, and concise answer to 
the user's question, using the provided context. Your response should be no longer than three sentences, 
ensuring brevity and accuracy. If you don't know the answer, say that you don't know."""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", human_prompt),
    ]
)


def get_chain(llm, retriever, store):
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt, document_variable_name="context")
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        store.get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain


def generate_response(chain: RunnableWithMessageHistory, user_input: str, session: str):
    res = chain.invoke(
        {"input": user_input},
        config={
            "configurable": {"session_id": session}
        }
    )

    return res['answer']

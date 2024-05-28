import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import (
    GoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_community.chat_message_histories import (
    RedisChatMessageHistory,
)
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# load env variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")
google_api_key = os.getenv("GOOGLE_API_KEY")

# init embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# initialize pinecone
pc = Pinecone(api_key=pinecone_api_key)

index = pc.Index(index_name)

text_field = "text"

vectorstore = PineconeVectorStore(index, embeddings, text_field)


class Recommend:
    def __init__(self):
        self.embeddings = embeddings
        self.pc = pc
        self.index_name = index_name
        self.openai_api_key = openai_api_key
        self.vectorstore = vectorstore

    def recommend(self, data):

        llm = GoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=google_api_key,
        )

        ### Contextualize question ###
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        print(contextualize_q_prompt)

        history_aware_retriever = create_history_aware_retriever(
            llm,
            vectorstore.as_retriever(search_kwargs={"k": 5}),
            contextualize_q_prompt,
        )

        ### Answer question ###
        qa_system_prompt = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say that you don't know. \
        Use three sentences maximum and keep the answer concise.\

        {context}"""

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        print(qa_prompt)

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        ### chat history ###
        def get_session_history(session_id: str) -> RedisChatMessageHistory:
            return RedisChatMessageHistory(session_id, url=REDIS_URL)

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        
        response = conversational_rag_chain.invoke(
            {"input": data["message"]},
            config={
                "configurable": {"session_id": data["session_id"]}
            },
        )

        print(response)

        return response["answer"]

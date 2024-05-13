import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# load env variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")

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

    def recommend(self, message):
        prompt_template = """
        Please respond to the question with as much detail as possible based on the provided context.
        Make sure to include all relevant details. If the answer is not available in the provided context,
        please respond with 'The answer is not available in the context.' Avoid providing incorrect answers
        \n\n
        context:\n {context}?\n
        input: \n{input}\n
        answer:
        """

        llm = ChatGoogleGenerativeAI(
            model="gemini-pro", convert_system_message_to_human=True, temperature=0.3
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

        history_aware_retriever = create_history_aware_retriever(
            llm,
            vectorstore.as_retriever(search_kwargs={"k": 5}),
            contextualize_q_prompt,
        )

        ### Answer question ###
        qa_system_prompt = """Please respond to the question with as much detail as possible based on the provided context.
        Make sure to include all relevant details. If the answer is not available in the provided context,
        please respond with 'The answer is not available in the context.' Avoid providing incorrect answers

        {context}"""

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        ### Statefully manage chat history ###
        store = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        print(store)

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        response = conversational_rag_chain.invoke(
            {"input": message},
            config={
                "configurable": {"session_id": "abc123"}
            },  # constructs a key "abc123" in `store`.
        )

        print(response)

        return response["answer"]

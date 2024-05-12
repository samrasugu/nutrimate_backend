import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

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
        self.conversation_memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
        )

    def recommend(self, message):
        # Update conversation memory
        # self.conversation_memory.save_context(message)

        prompt_template = """
        Please respond to the question with as much detail as possible based on the provided context.
        Make sure to include all relevant details. If the answer is not available in the provided context,
        please respond with 'The answer is not available in the context.' Avoid providing incorrect answers
        \n\n
        context:\n {context}?\n
        input: \n{input}\n
        answer:
        """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        llm = ChatGoogleGenerativeAI(
            model="gemini-pro", convert_system_message_to_human=True, temperature=0.3
        )

        combine_docs_chain = create_stuff_documents_chain(llm, prompt)

        retrieval_chain = create_retrieval_chain(
            vectorstore.as_retriever(search_kwargs={"k": 5}), combine_docs_chain
        )

        # Include conversation history in the input
        input_with_history = {
            "input": message,
            "conversation_history": self.conversation_memory.load_memory_variables({}),
        }

        response = retrieval_chain.invoke(input_with_history)

        # Update conversation memory with the assistant's response
        self.conversation_memory.save_context(
            {"input": message}, {"output": response["answer"]}
        )

        return response["answer"]

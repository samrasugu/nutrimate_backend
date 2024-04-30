import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# load env variables
pinecone_api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('INDEX_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')

# init embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# initialize pinecone
pc = Pinecone(api_key=pinecone_api_key)

index = pc.Index(index_name)

text_field = "text"

vectorstore = PineconeVectorStore(
    index, embeddings, text_field
)

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

        prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])

        llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True, temperature=0.3)

        # conversational memory
        conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
        )

        combine_docs_chain = create_stuff_documents_chain(llm, prompt)

        retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(search_kwargs={"k": 5}), combine_docs_chain)

        response=retrieval_chain.invoke({"input":message})
        
        return response["answer"]
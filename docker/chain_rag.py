import os
from dotenv import load_dotenv

from pipeline_ingestion import PipelineIngestion
from retriever_search import RetrieverSearch

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

template = """
Answer the question based only on the following context:

context = {context}

question = {question}

answer:
"""


class Chain:
    def __init__(self):
        self.data_path = "./data"

        self.retriever = RetrieverSearch()

        self.llm = ChatMistralAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=0.2,
            max_tokens=512
        )

        #  HyDE
        hyde_prompt = ChatPromptTemplate.from_template("""
        Please write a passage to answer the question.

        Question: {question}

        Passage:
        """)

        self.hyde_chain = hyde_prompt | self.llm | StrOutputParser()

        self.prompt = ChatPromptTemplate.from_template(template)

        def retriever_with_hyde(inputs):
            question = inputs["question"]

            hyde_doc = self.hyde_chain.invoke({"question": question})

            search_query = question + " " + hyde_doc

            docs = self.retriever.search(search_query, k=3)

            return "\n\n---\n\n".join([doc.page_content for doc in docs])

        self.chain = (
            RunnableParallel({
                "context": RunnableLambda(retriever_with_hyde),
                "question": lambda x: x["question"],
            })
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def retriever_rag(self, query: str):
        return self.chain.invoke({"question": query})
        
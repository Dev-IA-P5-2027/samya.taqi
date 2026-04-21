
from config import settings 
from retriever_search import RetrieverSearch

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


template = """
Answer the question based on the following context.:

context = {context}

question = {question}

answer:
"""


class Chain:
    def __init__(self):
        self.data_path = settings.data_path

        self.retriever = RetrieverSearch()

        self.llm = ChatMistralAI(
            api_key=settings.mistral_api_key.get_secret_value(),
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
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
            k_value = inputs.get("k", settings.top_k)
            hyde_doc = self.hyde_chain.invoke({"question": question})

            search_query = f"{question}\n{hyde_doc}"

            

            docs = self.retriever.search(search_query, k=k_value)

            return "\n\n---\n\n".join([doc.page_content for doc in docs])

        self.chain = (
            RunnableParallel({
                "context": RunnableLambda(retriever_with_hyde), #transformer la focntion python en comoposant LangChain
                "question": lambda x: x["question"], #récupére la question depuis l'entrée
            })
            | self.prompt
            | self.llm
            | StrOutputParser() #convertit la sortie du LLM en sortie simple
        )

    def retriever_rag(self, query: str, k: int = None, search_type="similarity"):
        return self.chain.invoke({
            "question": query,
            "k": k or settings.top_k ,
            "search_type": search_type
        })
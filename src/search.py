import requests
# from documents import extract_content_from_html
from langchain import PromptTemplate,  LLMChain, HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# def fetchDocumentById(id, cookie):
#     url = f"https://simpl.atlassian.net/wiki/rest/api/content/{id}?expand=body.storage"
#     headers = {
#         "Cookie": cookie
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         plain_text=extract_content_from_html(dict(response.json())['body']['storage']['value'])
#         cleaned_text = ' '.join(plain_text.splitlines()).strip()
#         return  cleaned_text
#     else:
#         return None

# def getTopSimilarDocIdsFromConfluence(query,cookie_val):
#     url = 'https://simpl.atlassian.net/wiki/rest/api/search'
#     params = {
#         'cql': f"text ~ '{query}' AND space=TAC",
#         'limit': 3
#     }
#     headers = {
#         'Cookie': cookie_val
#     }

#     response = requests.get(url, params=params, headers=headers)

#     if response.status_code == 200:
#         ids=[]
#         data = dict(response.json())
#         results=data['results']
#         for result in results:
#             ids.append(result['content']['id'])
#         return ids
#     else:
#         print(f'Request failed with status code: {response.status_code}')

# def generateContexts(ids,cookie_val):
#     context=""
#     for id in ids:
#         context+=fetchDocumentById(id,cookie_val)
#     return context

# def GetSearchResultUsingConfluenceSearchAPI(query,cookie_val,llm_model):
#     ids=getTopSimilarDocIdsFromConfluence(query,cookie_val)
#     context=generateContexts(ids,cookie_val)
#     if(len(context)==0):
#         return "I dont Know"
#     else:
#         print(context)
#     template = """
#     Answer the "question" strictly based on the "context" below. Give me the answer related to question only don't add the things which is not asked in the question
#     "I don't know" if you don't find relevant context.

#     context: {context}
#     question: {instruction}
#     answer:
#     """
#     prompt_with_context = PromptTemplate(
#         input_variables=["instruction", "context"],
#         template=template)
#     llm = HuggingFacePipeline(pipeline=llm_model)
#     llm_context_chain = LLMChain(llm=llm, prompt=prompt_with_context)
#     answer = llm_context_chain.predict(instruction=query, context=context).lstrip()
#     return answer

def Similarity_Search_Using_Embeddings(query,Cookie_VAL,llm_model):
    template = """
    Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    {context}
    Question: {query}
    """
    prompt_with_context = PromptTemplate(
        input_variables=["context", "query"],
        template=template)
    llm = HuggingFacePipeline(pipeline=llm_model)
    llm_context_chain = LLMChain(llm=llm, prompt=prompt_with_context)
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    # query_embeddings = embeddings.embed_query(query) 
    def similarity_search(query_embeddings):
        try:
            vectorstore = FAISS.load_local("faiss_index", embeddings)
            fres = vectorstore.similarity_search(query_embeddings)
            return fres
        except FileNotFoundError:
            print("Error: 'faiss_index/index.faiss' file not found. Make sure 'documents.py' has been executed first.")
            return None


    def convert_into_document(query_embeddings):
        import json
        from fastapi.encoders import jsonable_encoder
        from pydantic import BaseModel, Field
        class Document(BaseModel):
            page_content: str
            metadata: dict = Field(default_factory=dict)
        fdoc=[]
        faissres= similarity_search(query_embeddings)
        for i in range (0,len(faissres)):
            fdoc.append(Document(page_content=faissres[i].page_content, metadata=faissres[i].metadata))
        return fdoc

    def convert_into_string(query_embeddings):
        fcontext="""
        """
        fdoc = convert_into_document(query_embeddings)
        for i in range (0,len(fdoc)):
            fcontext += fdoc[i].page_content
        return fcontext
    top_4_docs = convert_into_string(query)
    answer = llm_context_chain.predict(query=query, context=top_4_docs).lstrip()
    return answer 
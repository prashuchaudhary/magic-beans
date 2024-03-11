from django.shortcuts import render
from django.http import JsonResponse
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from typing import Dict
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
import os


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


module_dir = os.path.dirname(__file__) 
file_path = os.path.join(module_dir, 'templates/beans/sample_vmm.txt')

chat = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.8)
loader = TextLoader(file_path)
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(all_splits, embeddings)
retriever = db.as_retriever(k=8)

question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context, dont add own information, use default channel , follow guidelines:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

chat_history = ChatMessageHistory()

retrieval_chain_with_only_answer = (
    RunnablePassthrough.assign(
        context=parse_retriever_input | retriever,
    )
    | document_chain
)


def index(request):
    return render(request, "beans/index.html", {})


def magic(request):
    global chat_history
    global retrieval_chain_with_only_answer
    query = request.GET.get("query")
    chat_history.add_user_message(query)
    response=retrieval_chain_with_only_answer.invoke(
        {
            "messages": chat_history.messages,
        }
    )
    response = response.replace('**','')
    chat_history.add_ai_message(response)
    return JsonResponse({'message': response})


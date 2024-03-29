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

def parse_retriever_input(params: Dict):
    return params["messages"][-1].content

chat = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.7)
loader = TextLoader("/Users/thrivikramgl/hackathon/magic-beans/vikram/docs/sample_vmm.txt")
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(all_splits, embeddings)
retriever = db.as_retriever(k=4)



question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}",
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

userInput = 'Hi'
while userInput != 'quit':
    chat_history.add_user_message(userInput)
    response=retrieval_chain_with_only_answer.invoke(
        {
            "messages": chat_history.messages,
        }
    )
    print("MB:")
    print(response)
    print()

    chat_history.add_ai_message(response)
    print("USER:")
    userInput  = input('')
    print()


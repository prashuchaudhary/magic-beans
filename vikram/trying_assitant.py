from time import sleep
from openai import OpenAI
from SqliteUtil import SqliteUtil
import os


term_size = os.get_terminal_size()

sqlUtil = SqliteUtil()

brand ="VMM"
orgId = 486
assistantName = "{}'s Magic bean".format(brand)
defaultChannel = "SMS MESSAGE"
instructions = """"You are a creative and modern day assistant to  {0} brand's marketing team helping to curate 
promotional content to send to customers across various channels . 
The attached files provide information about the brand and their guidelines for promotions content. 
Strictly adhere to the guidelines while generating your responses.
when no communication channel is provided, ask for the communication channel before responding to the query.
""".format(brand)

client = OpenAI()

assistant = None
assistantId = sqlUtil.getAssistantIdForOrg(brand)
if assistantId==None:
    assistant = client.beta.assistants.create(
        name=assistantName,
        instructions=instructions,
        tools=[{"type": "retrieval"}],
        model="gpt-4-turbo-preview"
    )
    sqlUtil.addNewAssistantToDb(orgId,brand,assistant.id)
else:
    allAssisstants = client.beta.assistants.list(
        order="desc",
        limit="20"
        )
    assistant = next(x for x in allAssisstants.data if x.id == assistantId[0] )

#print(assistant)

thread = client.beta.threads.create()

print('MB: Hello , How may i help you today?')
userInput = ''
userInput = input('USER: ')
while userInput!='quit':
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=userInput
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistantId[0],
        instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    while run.status!='completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
        sleep(5)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order='desc'
        )
    print("MB: {}".format(messages.data[0].content[0].text.value))
    print('_' * term_size.columns)
    userInput = input("USER:")

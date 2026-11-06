from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FN_NAME_TO_FN_MAP
import json
import os

load_dotenv()


client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

# Safety limit : The max number of model rounds for one user question
MAX_STEPS = 5

messages.append(
        {
        "role": "system",
        "content": (
            "You are a humble and helpful conversational assistant and you answer under 25 words."
        )
    }
)

while True: # chat loop
    user_input = input("\nPriyanshu: ")

    if user_input.strip().lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append({
        "role":"user",
        "content":user_input
    })

    # 1st call to LLM API with tools
    # response = client.chat.completions.create(
    #     model=os.getenv("MODEL"),
    #     messages=messages,
    #     tools=TOOLS,
        # [
        #     {
        #     "role":"user",
        #     "content":user_input
        #     }
        # ]
    #)

    '''
    messages.append({
        "role":"assistant",
        "content":response.choices[0].message.content
    })
    print("Assistant: " + response.choices[0].message.content)
    '''
    #print("Assistant (raw): " + str(response))

    #msg = response.choices[0].message

    #if msg.tool_calls: # checking if the response contains any tool call
    #while True: # chained tool calling
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message

        if not msg.tool_calls: # if there is no tool call break
            break

        messages.append(msg) # appending the response from LLM

        for tool_call in msg.tool_calls: # using a for loop because we want to check and process a bunch of function calls
            func_name = tool_call.function.name # getting the function name which LLM wants to call
            func_args = {}

            try:
                func_args = json.loads(tool_call.function.arguments or "{}")  # converting json string to dictionary

                fn = FN_NAME_TO_FN_MAP[func_name] # finding the corresponding function to the function string
                result = fn(**func_args) # ** is dictionary unpacking operator converting the dictionary to be passed as argument in function
            except Exception as e:
                result = f"Error while running {func_name} : {e}"

            messages.append({
                "role":"tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })  #appending the result that came from the tool call

        #2nd call to LLM API with the updated msg along with the tool response
        # response = client.chat.completions.create(
        #     model=os.getenv("MODEL"),
        #     messages=messages
        # )

        # msg = response.choices[0].message # accessing the response from LLM

    #In python, else after a for loop runs only if the loop finishes normally, meaning it wasn't ended early by a break.
    else:
        #Ran out of steps: The model never gave the final answer.
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append({
            "role": "Assistant",
            "content": fallback
        })
        print("Assistant : " + fallback)
        continue

    messages.append({
        "role":"assistant",
        "content": msg.content
    }) # appending the response from LLM whether tool_call is called or not

    print("Assistant: " + msg.content)
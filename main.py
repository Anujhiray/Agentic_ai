import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from tools import requirement_parser_tool,test_case_generator_tool,formatter_tool

load_dotenv()
client=OpenAI()

def log_to_file(text):
with open("log.txt","a",encoding="utf-8") as f:
f.write(f"\n[{datetime.now()}]\n{text}\n")

tools=[
{
"type":"function",
"function":{
"name":"requirement_parser_tool",
"description":"Extracts the core requirement from user input",
"parameters":{
"type":"object",
"properties":{"text":{"type":"string"}},
"required":["text"]
}
}
},
{
"type":"function",
"function":{
"name":"test_case_generator_tool",
"description":"Generates test cases from a parsed requirement",
"parameters":{
"type":"object",
"properties":{"text":{"type":"string"}},
"required":["text"]
}
}
},
{
"type":"function",
"function":{
"name":"formatter_tool",
"description":"Formats test cases cleanly",
"parameters":{
"type":"object",
"properties":{"text":{"type":"string"}},
"required":["text"]
}
}
}
]

tool_map={
"requirement_parser_tool":requirement_parser_tool,
"test_case_generator_tool":test_case_generator_tool,
"formatter_tool":formatter_tool
}

system_prompt="""
You are a ReAct agent. You must think step by step and decide which tool to call.
First understand the input. Then call tools one by one until final test cases are ready.
Always finish by returning only formatted test cases.
"""

def run_agent(user_input):
messages=[
{"role":"system","content":system_prompt},
{"role":"user","content":user_input}
]

log_to_file("Input: "+user_input)

while True:
r=client.chat.completions.create(model="gpt-4.1-mini",messages=messages,tools=tools)
m=r.choices[0].message

if m.tool_calls:
for call in m.tool_calls:
name=call.function.name
args=json.loads(call.function.arguments)
print("Action: Call",name)
log_to_file("Action: Call "+name)
result=tool_map[name](**args)
print("Observation:",result)
log_to_file("Observation: "+result)
messages.append(m)
messages.append({"role":"tool","tool_call_id":call.id,"content":result})
else:
print("\nFinal Answer:\n"+m.content)
log_to_file("Final Answer:\n"+m.content)
break

if __name__=="__main__":
user_input=input("Enter requirement: ")
run_agent(user_input)

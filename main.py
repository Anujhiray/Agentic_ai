from datetime import datetime
from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from tools import requirement_parser_tool,test_case_generator_tool,formatter_tool

load_dotenv()

def log_to_file(text):
with open("log.txt","a",encoding="utf-8") as f:
f.write(f"\n[{datetime.now()}]\n{text}\n")

class State(dict):
pass

def think(state):
if "parsed" not in state:
t="I need to understand the requirement."
state["next"]="parse"
elif "cases" not in state:
t="Now I should generate test cases."
state["next"]="generate"
elif "final" not in state:
t="I should format the test cases."
state["next"]="format"
else:
state["next"]="end"
return state
print("\nThought:",t)
log_to_file("Thought: "+t)
return state

def parse(state):
print("Action: Call Requirement Parser Tool")
log_to_file("Action: Call Requirement Parser Tool")
r=requirement_parser_tool(state["input"])
print("Observation:",r)
log_to_file("Observation: "+r)
state["parsed"]=r
return state

def generate(state):
print("Action: Call Test Case Generator Tool")
log_to_file("Action: Call Test Case Generator Tool")
r=test_case_generator_tool(state["parsed"])
print("Observation:",r)
log_to_file("Observation: "+r)
state["cases"]=r
return state

def format_output(state):
print("Action: Call Formatter Tool")
log_to_file("Action: Call Formatter Tool")
r=formatter_tool(state["cases"])
print("\nFinal Answer:\n"+r)
log_to_file("Final Answer:\n"+r)
state["final"]=r
return state

def router(state):
return state["next"]

g=StateGraph(State)
g.add_node("think",think)
g.add_node("parse",parse)
g.add_node("generate",generate)
g.add_node("format",format_output)

g.set_entry_point("think")

g.add_conditional_edges("think",router,{
"parse":"parse",
"generate":"generate",
"format":"format",
"end":END
})

g.add_edge("parse","think")
g.add_edge("generate","think")
g.add_edge("format","think")

app=g.compile()

if __name__=="__main__":
user_input=input("Enter requirement: ")
print("\nInput:",user_input)
log_to_file("Input: "+user_input)
app.invoke({"input":user_input})

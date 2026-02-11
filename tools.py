import os
from openai import OpenAI

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def requirement_parser_tool(text):
r=client.chat.completions.create(model="gpt-4.1-mini",messages=[{"role":"user","content":f"Extract the core requirement clearly:\n{text}"}])
return r.choices[0].message.content.strip()

def test_case_generator_tool(text):
r=client.chat.completions.create(model="gpt-4.1-mini",messages=[{"role":"user","content":f"Generate 3 test cases in this format:\nTC-001: ...\nTC-002: ...\nTC-003: ...\n\n{text}"}])
return r.choices[0].message.content.strip()

def formatter_tool(text):
r=client.chat.completions.create(model="gpt-4.1-mini",messages=[{"role":"user","content":f"Format this cleanly:\n{text}"}])
return r.choices[0].message.content.strip()

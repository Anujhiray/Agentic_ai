# LangGraph ReAct Agent for Test Case Generation

## Objective
To demonstrate the **ReAct (Reason + Act)** pattern using LangGraph. The agent takes a software requirement and autonomously generates formatted test cases by reasoning through a sequence of tool calls.

## How It Works (The ReAct Pattern)
The agent follows a loop:
1. **Thought:** Analyzes the user request.
2. **Act:** Decides to call a specific tool (e.g., `requirement_parser`).
3. **Observe:** Receives the output from the tool.
4. **Repeat:** Uses the new information to decide the next step until the final answer is ready.

## Tools Implemented
1. **`requirement_parser`**: Extracts actionable logic from natural language.
2. **`test_case_generator`**: Creates raw test scenarios based on parsed data.
3. **`formatter_tool`**: Converts the list of tests into a structured final report.

## Setup & Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add API key to `.env`: `OPENAI_API_KEY=sk-...`
3. Run the agent: `python main.py`



## Example Output

**Input:**  
User should be able to close the pop-up window.

**Console Output Flow:**

Thought: I need to understand the requirement.  
Action: Call Requirement Parser Tool  
Observation: User wants the pop-up window to be closable.  

Thought: Now I should generate test cases.  
Action: Call Test Case Generator Tool  
Observation:  
TC-001: Verify pop-up window closes when user clicks the close icon.  
TC-002: Verify pop-up window closes when user clicks outside the pop-up.  
TC-003: Verify pop-up window remains visible if no close action is taken.  

Thought: I should format them clearly.  
Action: Call Formatter Tool  

Final Answer:
TC-001: Verify pop-up window closes when user clicks the close icon.  
TC-002: Verify pop-up window closes when user clicks outside the pop-up.  
TC-003: Verify pop-up window remains visible if no close action is taken.

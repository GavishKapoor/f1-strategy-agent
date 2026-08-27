# agent.py
# Ye file LLM ko humare F1 tools ke saath jodta hai — yahi "agent" hai.

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

from f1_tools import get_sessions, get_drivers, get_laps, get_stints, get_weather

load_dotenv()

# --- Tools ko LangChain ke "tool" format mein wrap karo ---
# @tool decorator LLM ko bata deta hai ki ye function available hai,
# aur docstring padh ke LLM samajhta hai ki kab use karna hai.

@tool
def find_race_session(year: int, country_name: str = None) -> str:
    """Find the session_key for a specific F1 race by year and country name.
    Always call this FIRST before getting laps/stints/drivers, since they need session_key."""
    result = get_sessions(year, country_name)
    return json.dumps(result)

@tool
def get_race_drivers(session_key: int) -> str:
    """Get the list of all drivers who participated in a given race session."""
    result = get_drivers(session_key)
    return json.dumps(result)

@tool
def get_driver_laps(session_key: int, driver_number: int = None) -> str:
    """Get lap-by-lap timing data for a race session. Pass driver_number for one driver, or omit for all drivers."""
    result = get_laps(session_key, driver_number)
    return json.dumps(result)

@tool
def get_tyre_stints(session_key: int, driver_number: int = None) -> str:
    """Get tyre stint data (which compound, how many laps) — the core data for pit strategy analysis."""
    result = get_stints(session_key, driver_number)
    return json.dumps(result)

@tool
def get_race_weather(session_key: int) -> str:
    """Get weather conditions (temperature, rainfall, humidity) for a race session. Useful for explaining tyre choices."""
    result = get_weather(session_key)
    return json.dumps(result)


# Saare tools ki list — LLM ko yahi dikhaye jayenge
tools = [find_race_session, get_race_drivers, get_driver_laps, get_tyre_stints, get_race_weather]

# LLM banao aur usko tools ke baare mein bata do
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
llm_with_tools = llm.bind_tools(tools)


def run_agent(user_question):
    messages = [{"role": "user", "content": user_question}]

    # Loop chalao jab tak LLM tools maangna band na kare
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # Agar LLM ne koi tool call nahi maanga, to matlab final answer aa gaya
        if not response.tool_calls:
            return response.content

        # LLM ne jitne tools maange, sab chalao
        for tool_call in response.tool_calls:
            print(f"  [Agent calling tool: {tool_call['name']}({tool_call['args']})]")

            # Sahi tool function dhundo naam se
            selected_tool = {t.name: t for t in tools}[tool_call["name"]]
            tool_result = selected_tool.invoke(tool_call["args"])

            # Result ko conversation mein wapas daalo, taaki LLM aage soch sake
            messages.append({
                "role": "tool",
                "content": str(tool_result),
                "tool_call_id": tool_call["id"]
            })


# --- Quick test ---
if __name__ == "__main__":
    question = "What tyre strategy did drivers use in the 2024 Monaco Grand Prix?"
    answer = run_agent(question)
    print("\nFinal Answer:\n", answer)
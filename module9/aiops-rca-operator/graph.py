
from langgraph.graph import StateGraph
from state import RCAState
from agents import planner, debugger, analyzer, fixer

builder = StateGraph(RCAState)

builder.add_node("planner", planner.run)
builder.add_node("debugger", debugger.run)
builder.add_node("analyzer", analyzer.run)
builder.add_node("fixer", fixer.run)

builder.set_entry_point("planner")
builder.add_edge("planner", "debugger")
builder.add_edge("debugger", "analyzer")
builder.add_edge("analyzer", "fixer")

graph = builder.compile()

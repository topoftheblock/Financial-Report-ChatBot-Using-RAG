from langgraph.graph import MessagesState
from typing import Annotated, List
import operator

def append_strings(existing: List[str], new: List[str]) -> List[str]:
    return existing + new

class AgentState(MessagesState):
    current_plan: str                       # Orchestrator's breakdown of tasks
    retrieved_context: Annotated[List[str], append_strings]  # Dossier built by Researcher
    calculation_results: Annotated[List[str], append_strings] # Output from Quant
    final_answer: str                       # Drafted by Reviewer
    needs_rework: bool                      # CRAG flag to route back to Researcher
    iteration_count: int                    # Track loops to prevent infinite routing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid

from agent import Agent

app = FastAPI(
    title="Memory Agent API",
    description="Multi-tenant conversational agent with semantic memory",
    version="1.0.0"
)

_session_cache: Dict[str, Agent] = {}


class InvocationRequest(BaseModel):
    user_id: str = Field(..., description="User identifier for memory isolation")
    run_id: Optional[str] = Field(None, description="Session identifier")
    query: str = Field(..., description="User message")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class InvocationResponse(BaseModel):
    user_id: str
    run_id: str
    response: str


def _get_or_create_agent(user_id: str, run_id: str) -> Agent:
    if run_id in _session_cache:
        return _session_cache[run_id]

    agent = Agent(user_id=user_id, run_id=run_id)
    _session_cache[run_id] = agent
    return agent


@app.get("/ping")
def ping():
    return {
        "status": "ok",
        "message": "Memory Agent API is running"
    }


@app.post("/invocation", response_model=InvocationResponse)
def invoke(request: InvocationRequest):
    try:
        run_id = request.run_id or str(uuid.uuid4())
        agent = _get_or_create_agent(request.user_id, run_id)

        result = agent.chat(request.query)

        if isinstance(result, str):
            response_text = result
        elif hasattr(result, "response"):
            response_text = result.response
        elif hasattr(result, "content"):
            response_text = result.content
        elif isinstance(result, dict):
            response_text = result.get("response", str(result))
        else:
            response_text = str(result)

        return InvocationResponse(
            user_id=request.user_id,
            run_id=run_id,
            response=response_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
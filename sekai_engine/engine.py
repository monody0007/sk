from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Tuple, Union
import uuid
from langgraph.graph import StateGraph, START, END

from .memu_adapter import MemUAdapter
from .llm_service import LLMService
from .utils.env import ensure_env_loaded
from .prompts.helpers import build_system_message
from .prompts.templates import CHARACTER_IDENTITY_TEMPLATE, WORLD_CONTEXT_TEMPLATE
from .crews.world_parser import CrewAIWorldParser
from .crewai_runner import CrewAIResponder

class SekaiEngine:
    """
    Main engine class for Sekai Engine - a memory-enabled AI character roleplay system.
    
    This engine combines MemU memory framework with CrewAI multi-agent system to create
    AI characters with persistent memory and consistent personality. It uses LangGraph
    for orchestrating the memory retrieval -> conversation -> memory storage workflow.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Sekai Engine with all required components.
        
        Sets up MemU adapter, LLM service, CrewAI responder, and world parser.
        Creates a LangGraph pipeline for orchestrating the conversation workflow.
        """
        # Ensure environment variables from .env are loaded before creating clients
        ensure_env_loaded()
        self.adapter = MemUAdapter()
        self.llm_service = LLMService()
        self.crewai = CrewAIResponder()
        self.world_parser = CrewAIWorldParser()

        # Public state after init(): engine identifier and created agents
        self.engine_id: Optional[str] = None
        self.agents: List[Tuple[str, str]] = []

        # Build a LangGraph pipeline for pre/post hooks orchestration.

        def node_retrieve(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            LangGraph node: Retrieve relevant memories from MemU based on user query.
            
            Args:
                state: Current graph state containing user_id, agent_id, and input
                
            Returns:
                Updated state with memu_response added
            """
            # Preserve upstream state keys explicitly between nodes
            user_id = state.get("user_id")
            agent_id = state.get("agent_id")
            query = state.get("input", "")
            memu_resp = self.adapter.retrieve_context(
                user_id=user_id,
                agent_id=agent_id,
                query=query,
            )
            return {
                "user_id": user_id,
                "agent_id": agent_id,
                "input": query,
                "memu_response": memu_resp,
            }

        def node_llm(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            LangGraph node: Generate AI response using CrewAI with memory context.
            
            Args:
                state: Current graph state containing user input and memory context
                
            Returns:
                Updated state with AI output added
            """
            # Preserve identifiers; append model output
            user_id = state.get("user_id")
            agent_id = state.get("agent_id")
            query = state.get("input", "")
            memu_resp = state.get("memu_response")
            context_str = str(memu_resp) if memu_resp is not None else ""
            system_message = build_system_message(context_str)
            
            # Use session-level persistent Agent, session ID generated from user_id and agent_id
            session_id = f"{user_id}_{agent_id}"
            reply = self.crewai.respond(query, system_message, session_id)
            
            return {
                "user_id": user_id,
                "agent_id": agent_id,
                "input": query,
                "memu_response": memu_resp,
                "output": reply,
            }

        def node_memorize(state: Dict[str, Any]) -> Dict[str, Any]:
            """
            LangGraph node: Store conversation in MemU memory system.
            
            Args:
                state: Current graph state containing user input and AI output
                
            Returns:
                Empty dict (post-hook node)
            """
            user_id = state.get("user_id")
            agent_id = state.get("agent_id")
            user_message = state.get("input", "")
            assistant_message = state.get("output", "")
            # Post-hook: must trigger memorize after LLM returns
            try:
                self.adapter.memorize_dialogue(
                    user_id=user_id,
                    user_name=user_id,
                    agent_id=agent_id,
                    agent_name=agent_id,  # Use agent_id as agent_name temporarily
                    user_message=user_message,
                    assistant_message=assistant_message,
                )
            except Exception as e:
                print(f"Warning: failed to memorize dialogue for agent {agent_id}: {e}")
            return {}

        graph = StateGraph(dict)
        graph.add_node("retrieve", node_retrieve)
        graph.add_node("llm", node_llm)
        graph.add_node("memorize", node_memorize)
        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "llm")
        graph.add_edge("llm", "memorize")
        graph.add_edge("memorize", END)
        self._graph_app = graph.compile()

    def init(self, world_input: Union[str, Dict[str, Any]], *, engine_id: Optional[str] = None) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Initialize the world and create AI characters based on world description.
        
        This method parses the world input to extract character information,
        creates unique agent IDs for each character, and seeds their memories
        with character background and world context.
        
        Args:
            world_input: World description as string or dict containing chapters
            engine_id: Optional custom engine ID, auto-generated if not provided
            
        Returns:
            Tuple of (engine_id, list of (agent_id, character_name) pairs)
            
        Raises:
            Exception: If character creation or memory seeding fails
        """
        eid = engine_id or f"engine_{hash(str(world_input))}"
        self.engine_id = eid
        characters = self.world_parser.parse(world_input)
        created: List[Tuple[str, str]] = []
        
        # Convert world input to string for world memory
        world_memory = world_input if isinstance(world_input, str) else json.dumps(world_input)
        
        for name, background in characters:
            # Generate unique agent ID
            aid = str(uuid.uuid4())
            
            # Create two system prompts: one for identity/background/rules and another for world context
            character_identity_prompt = CHARACTER_IDENTITY_TEMPLATE.format(name=name, background=background)
            world_context_prompt = WORLD_CONTEXT_TEMPLATE.format(world_memory=world_memory)
            
            # Send character identity/background/rules first, then world context as a second system message

            try:
                self.adapter.memorize_messages(
                    conversation=[
                        {"role": "system", "content": character_identity_prompt},
                        {"role": "assistant", "content": world_context_prompt},
                    ],
                    user_id="system",
                    user_name="System",
                    agent_id=aid,
                    agent_name=name,
                )
            except Exception as e:
                print(f"Warning: failed to seed memories for agent {name} ({aid}): {e}")
            
            created.append((aid, name))
        # Expose as public attributes for convenient external access
        self.agents = created
        return eid, created

    def engine_service(self, user_id: str, agent_id: str, content: str) -> str:
        """
        Process a user message and return AI response using the LangGraph pipeline.
        
        This is the main entry point for conversation with AI characters.
        The method runs the complete workflow: memory retrieval -> AI response -> memory storage.
        
        Args:
            user_id: Unique identifier for the user
            agent_id: Unique identifier for the AI character
            content: User's message content
            
        Returns:
            AI character's response as string
            
        Raises:
            RuntimeError: If LangGraph app is not initialized
        """
        # Always run the LangGraph pipeline.
        if self._graph_app is None:
            raise RuntimeError("LangGraph app not initialized")
        state: Dict[str, Any] = {
            "user_id": user_id,
            "agent_id": agent_id,
            "input": content,
        }
        result: Dict[str, Any] = self._graph_app.invoke(state)  # type: ignore[attr-defined]
        return str(result.get("output", ""))

    def engine_service_struct(self, user_id: str, agent_id: str, content: str) -> Dict[str, Any]:
        """
        Run the pipeline and return a structured response including latest assistant reply.

        This method provides detailed information about the conversation process,
        including memory context, conversation history, and session information.
        Useful for debugging and advanced conversation management.

        Args:
            user_id: Unique identifier for the user
            agent_id: Unique identifier for the AI character
            content: User's message content

        Returns:
            Dictionary containing:
            - user_id: User identifier
            - agent_id: Agent identifier
            - input: Original user input
            - memu_response: Retrieved memory context
            - output: AI response
            - session_id: Session identifier
            - history: Full conversation history
            - latest_assistant: Most recent assistant message

        Raises:
            RuntimeError: If LangGraph app is not initialized
        """
        if self._graph_app is None:
            raise RuntimeError("LangGraph app not initialized")
        state: Dict[str, Any] = {
            "user_id": user_id,
            "agent_id": agent_id,
            "input": content,
        }
        result: Dict[str, Any] = self._graph_app.invoke(state)  # type: ignore[attr-defined]
        # Build session context and derive latest assistant reply from conversation history
        session_id = f"{user_id}_{agent_id}"
        history = self.crewai.get_history(session_id)
        latest_assistant: Optional[str] = None
        for role, msg in reversed(history):
            if role == "assistant":
                latest_assistant = msg
                break
        return {
            "user_id": user_id,
            "agent_id": agent_id,
            "input": content,
            "memu_response": result.get("memu_response"),
            "output": result.get("output"),
            "session_id": session_id,
            "history": history,
            "latest_assistant": latest_assistant or str(result.get("output", "")),
        }

    # ================================
    # Session Management Methods
    # ================================
    
    def clear_user_session(self, user_id: str, agent_id: str) -> None:
        """
        Clear the conversation session for a specific user-agent pair.
        
        This removes the session-level Agent instance and conversation history
        for the specified user and agent combination.
        
        Args:
            user_id: User identifier
            agent_id: Agent identifier
        """
        session_id = f"{user_id}_{agent_id}"
        self.crewai.clear_session(session_id)
    
    def clear_all_sessions(self) -> None:
        """
        Clear all active conversation sessions.
        
        This removes all session-level Agent instances and conversation histories,
        effectively resetting the conversation state for all users and agents.
        """
        self.crewai.clear_all_sessions()
    
    def get_active_session_count(self) -> int:
        """
        Get the current number of active conversation sessions.
        
        Returns:
            Number of active sessions
        """
        return self.crewai.get_session_count()
    
    def get_active_session_ids(self) -> list[str]:
        """
        Get all active session identifiers.
        
        Returns:
            List of active session IDs
        """
        return self.crewai.get_session_ids()
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Get comprehensive session statistics and information.
        
        Returns:
            Dictionary containing:
            - active_sessions: Number of active sessions
            - session_ids: List of active session IDs
            - engine_id: Current engine identifier
            - total_agents: Total number of created agents
        """
        return {
            "active_sessions": self.get_active_session_count(),
            "session_ids": self.get_active_session_ids(),
            "engine_id": self.engine_id,
            "total_agents": len(self.agents)
        }

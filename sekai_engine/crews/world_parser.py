from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple, Union
from crewai import Agent, Task, Crew, LLM

from ..prompts.templates import (
    WORLD_PARSE_SYSTEM_TEMPLATE,
    WORLD_PARSE_USER_TEMPLATE,
)


class CrewAIWorldParser:
    """
    Parse world description into characters using a small CrewAI pipeline.

    This class uses a two-agent CrewAI system to extract character information
    from world descriptions. The flow consists of:
    1) Generator agent produces strict JSON according to schema
    2) Reviewer agent validates schema and fixes output if needed
    
    The final Crew result is parsed here; on failure it falls back to a simple default.
    """

    def __init__(self, model: str | None = None, temperature: float = 0.1) -> None:
        """
        Initialize world parser with model configuration.
        
        Args:
            model: LLM model name (defaults to gpt-4o-mini)
            temperature: Model temperature for generation
        """
        self.model = model
        self.temperature = temperature

    def parse(self, world_input: Union[str, Dict[str, Any]] , max_retries: int = 1) -> List[Tuple[str, str]]:
        """
        Parse world input to extract character information.
        
        This method uses a CrewAI pipeline with two agents to extract
        character names and backgrounds from world descriptions. It includes
        retry logic and fallback behavior for robustness.
        
        Args:
            world_input: World description as string or dictionary
            max_retries: Maximum number of parsing attempts
            
        Returns:
            List of (character_name, character_background) tuples
            
        Raises:
            Exception: If parsing fails after all retries
        """
        input_text = str(world_input)
        system_message = WORLD_PARSE_SYSTEM_TEMPLATE
        user_prompt = WORLD_PARSE_USER_TEMPLATE.format(input_text=input_text)

        # Configure LLM for CrewAI
        llm = LLM(model=(self.model or "gpt-4o-mini"), temperature=self.temperature)

        generator = Agent(
            name="World Character Extractor",
            role="Story Structurer",
            goal=(
                "Extract characters from the input and output strictly valid JSON per the schema."
            ),
            backstory=system_message,
            llm=llm,
            verbose=False,
            allow_delegation=False,
        )

        reviewer = Agent(
            name="JSON Schema Enforcer",
            role="Validator",
            goal=(
                "Ensure output strictly conforms to the schema and contains only JSON, no extra text."
            ),
            backstory=(
                "You check correctness and format. If the JSON is invalid, fix it and output only the corrected JSON."
            ),
            llm=llm,
            verbose=False,
            allow_delegation=False,
        )

        gen_task = Task(
            description=user_prompt,
            agent=generator,
            expected_output=(
                "A JSON string with this structure only: {\n"
                "  \"characters\": [\n"
                "    {\n"
                "      \"name\": \"...\",\n"
                "      \"background\": \"...\"\n"
                "    }\n"
                "  ]\n"
                "}"
            ),
        )

        review_instructions = (
            "Review the previous output. If it's strictly valid JSON per the schema,"
            " reprint the exact same JSON. If not valid, output a corrected JSON that strictly conforms."
            " Output only JSON and nothing else."
        )
        review_task = Task(
            description=review_instructions,
            agent=reviewer,
            expected_output="A strictly valid JSON string only, no explanations.",
        )

        crew = Crew(agents=[generator, reviewer], tasks=[gen_task, review_task], verbose=False)

        attempt = 0
        while attempt < max_retries:
            try:
                result = crew.kickoff()
                data = json.loads(str(result).strip())
                characters: List[Tuple[str, str]] = []
                for char in data.get("characters", []):
                    name = str(char.get("name", "")).strip()
                    background = str(char.get("background", "")).strip()
                    if name and background:
                        characters.append((name, background))
                if characters:
                    return characters
            except Exception:
                attempt += 1
                continue

        return [("Character", f"You are a character in: {input_text}")]

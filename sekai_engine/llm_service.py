import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env eagerly; engine also calls its own loader, duplicate loads are harmless.
load_dotenv()


class LLMService:
    """
    Service class for interacting with OpenAI's language models.
    
    This class provides a simplified interface for sending prompts to OpenAI's
    chat completion API, with support for system prompts and detailed logging.
    """
    
    def __init__(self):
        """
        Initialize OpenAI client with API key from environment variables.
        
        Raises:
            ValueError: If OPENAI_API_KEY is not found in environment variables
        """
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or .env file")
        
        self.client = OpenAI(api_key=api_key)
    
    def get_response(self, prompt, system_prompt=None):
        """
        Send prompt to LLM and return raw text response.
        
        This method sends a user prompt and optional system prompt to OpenAI's
        chat completion API and returns the generated response. It includes
        detailed logging for debugging purposes.
        
        Args:
            prompt: The user's input message
            system_prompt: Optional system message to guide the model's behavior
            
        Returns:
            The model's response as a string
            
        Raises:
            Exception: If the API call fails
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": str(system_prompt)})
        messages.append({"role": "user", "content": str(prompt)})
        
        # Print input with clear separators
        print("=" * 80)
        print("🔵 LLM SERVICE INPUT")
        print("=" * 80)
        if system_prompt:
            print("📋 SYSTEM PROMPT:")
            print(f"{system_prompt}")
            print("-" * 40)
        print("💬 USER PROMPT:")
        print(f"{prompt}")
        print("=" * 80)
        
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        
        # Print output with clear separators
        print("🔴 LLM SERVICE OUTPUT")
        print("=" * 80)
        print("🤖 RESPONSE:")
        print(f"{result}")
        print("=" * 80)
        print()  # Add extra newline for spacing
        
        return result

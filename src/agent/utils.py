import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from typing import Optional

load_dotenv()

client = InferenceClient(api_key=os.getenv("HUGGINGFACE_API_TOKEN"))

def call_llm(message: str, mock_response: Optional[str] = None,
            model: str = "mistralai/Mistral-7B-Instruct-v0.2",
            max_tokens: int = 200,
            temperature: float = 0.3) -> str:
    """Call the LLM with the given message, returning the response.
    
    Args:
        message (str): The input message to send to the LLM.
        mock_response (Optional[str]): Mock response for testing purposes.
        model (str): The model to use for the LLM call.
        max_tokens (int): Maximum number of tokens in the response.
        temperature (float): Sampling temperature for the LLM response.
        
    Returns:
        str: The response from the LLM or mock response.
    
    """
    if mock_response is not None:
        return mock_response
    
    try:
        result = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
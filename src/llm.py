import os
from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from nest_asyncio import apply
from configparser import ConfigParser
apply()  # Apply nest_asyncio to allow nested event loops


class LLM:
    def __init__(self, provider_type:str,model_name:str):
        """
        Initializes the LLM with a specified provider type and model name.
        
        Args:
            provider_type (str): The type of provider (e.g., 'ollama').
            model_name (str): The name of the model to use.
        """
        self.config= self._config_loader()
        self.provider_type = provider_type
        self.model_name = model_name

    def _config_loader(self):
        self.config=ConfigParser()
        self.config.read('config.ini')

    def _setup_agent(self):
        if self.provider_type != "ollama":
            client = OpenAIProvider(
                base_url=self.config["base_url"],  # Ollama default API URL
                api_key=os.getenv('api_key'),  # Ollama does not require an API key by default
            )
            raise ValueError("check if the model is supported by the provider")
        else:
            client = OpenAIProvider(
                base_url=self.config["ollama_url"],  # Ollama default API URL
                api_key="",  # Ollama does not require an API key by default
            )
            
        model = OpenAIModel(
            self.model_name,
            provider=client,
        )
        agent = Agent(model)
        
        return agent
    
    def run(self, prompt: str):
        """
        Runs the LLM with the given prompt.
        
        Args:
            prompt (str): The input prompt for the LLM.
        
        Returns:
            str: The output from the LLM.
        """
        agent = self._setup_agent()
        result = agent.run_sync(prompt)
        return result.output
    
# Example usage
if __name__ == "__main__":
    llm = LLM(provider_type="ollama", model_name="qwen3:8b")
    prompt = "Hello, world!"
    result = llm.run(prompt)
    print(result)
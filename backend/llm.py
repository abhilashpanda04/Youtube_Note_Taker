import os
from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from nest_asyncio import apply
from configparser import ConfigParser
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
import asyncio

# apply()  # Apply nest_asyncio to allow nested event loops


class LLM:
    def __init__(self, provider_type:str,model_name:str):
        """
        Initializes the LLM with a specified provider type and model name.
        
        Args:
            provider_type (str): The type of provider (e.g., 'ollama').
            model_name (str): The name of the model to use.
        """
        self._config_loader()
        self.provider_type = provider_type
        self.model_name = model_name

    def _config_loader(self):
        self.config=ConfigParser()
        self.config.read('config.ini')

    def _setup_agent(self):
        if self.provider_type != "ollama":
            client = OpenAIProvider(
                base_url=self.config["general"]["openai_base_url"],  # Ollama default API URL
                api_key=os.getenv('api_key'),  # Ollama does not require an API key by default
            )
            raise ValueError("check if the model is supported by the provider")
        else:
            client = OpenAIProvider(
                base_url=self.config["general"]["ollama_base_url"],  # Ollama default API URL
                api_key="",  # Ollama does not require an API key by default
            )
            
        model = OpenAIModel(
            self.model_name,
            provider=client,
        )
        agent = Agent(model)
        
        return agent
    
    async def run(self, prompt: str):
        """
        Runs the LLM with the given prompt.
        
        Args:
            prompt (str): The input prompt for the LLM.
        
        Returns:
            str: The output from the LLM.
        """
        agent = self._setup_agent()
        result = await agent.run(prompt)
        return result.output
    
    async def run_stream(self, prompt: str):
        """
        Runs the LLM with the given prompt.
        
        Args:
            prompt (str): The input prompt for the LLM.
        
        Returns:
            str: The output from the LLM.
        """
        agent = self._setup_agent()
        console = Console()
        console.log(f'Using model: {self.model_name}')
        with Live('', console=console, vertical_overflow='visible') as live:
            async with agent.run_stream(prompt) as result:
                async for message in result.stream():
                    live.update(Markdown(message))
        console.log(result.usage())

# Example usage
if __name__ == "__main__":
    llm = LLM(provider_type="ollama", model_name="qwen3:8b")
    prompt = "Hello, world!"
    mode="classic" #stream or classic
    if mode=="stream":
        result = asyncio.run(llm.run_stream(prompt))
    else:
        result =asyncio.run(llm.run(prompt))
        print(result)
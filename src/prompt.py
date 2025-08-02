from pathlib import Path
import sys

class Prompt:
   
    def __init__(self, 
                user_prompt_path:str= "src/prompts/summarizer.txt",
                system_prompt_path: str = None):
        final_user_prompt_path = user_prompt_path
        self.user_prompt = self.load_prompt(final_user_prompt_path)
        self.system_prompt = self.load_prompt(system_prompt_path) if system_prompt_path else "you are a helpful assistant"

    def load_prompt(self,prompt) -> str:
        with open(prompt, 'r') as file:
            prompt = file.read()
        return prompt.strip()
        
if __name__ == "__main__":
    prompt = Prompt()
    print(prompt.user_prompt)
    print(prompt.system_prompt)
import asyncio
from jinja2 import BaseLoader, Environment
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

SYSTEM_PROMPT = open("backend/templates/system_prompt.jinja2").read().strip()
USER_PROMPT = open("backend/templates/user_prompt.jinja2").read().strip()


class LLMService:
    """Service for interacting with the LLM"""
    MODEL_NAME = "microsoft/Phi-4-mini-instruct"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.device = torch.device(
            "mps" if torch.backends.mps.is_available() else "cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.MODEL_NAME,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        ).to(self.device)

        self.env = Environment(loader=BaseLoader())
        self.conversation_history = []
        self._initialized = True

    def render(self, user_message: str) -> str:
        """Render the user message with Jinja2

        param user_message: The message from the user
        return: The rendered prompt
        """
        history = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}"
                            for msg in self.conversation_history])

        template = self.env.from_string(
            SYSTEM_PROMPT + "\n\n" +
            "Previous conversation:\n" + history + "\n\n" +
            USER_PROMPT
        )
        return template.render(user_message=user_message)

    def generate_response(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if response.startswith(prompt):
            response = response[len(prompt):].strip()

        return response

    async def get_ai_response(self, user_message: str) -> str:
        """Process a user message and maintain conversation history

        param user_message: The message from the user
        return: The AI-generated response
        """
        prompt = self.render(user_message=user_message)
        response = self.generate_response(prompt)

        self.conversation_history.append({
            "user": user_message,
            "ai": response
        })

        return response


llm_service = LLMService()


async def test_llm():
    """Test function for the LLM service"""
    # Simulate a conversation
    messages = [
        "My name is Johnson",
        "I'm doing well, thank you. How are you?",
        "What was my name again?"
    ]

    for message in messages:
        logger.info(f"User message: {message}")
        logger.info("Generating response...")
        response = await llm_service.get_ai_response(message)
        logger.info(f"AI response: {response}")
        logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(test_llm())

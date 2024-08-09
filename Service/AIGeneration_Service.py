from openai import AsyncOpenAI
import os
import asyncio
class AIGeneration_Service:

    def __init__(self) -> None:
        pass

    #openai.api_key = os.environ["API_KEY"]

    async def GenerateResponse(self, prompt):
        client = AsyncOpenAI(
            api_key = os.environ["API_KEY"]

        )
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using the ChatGPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        message = response.choices[0].message
        print(message.content)
        return message.content


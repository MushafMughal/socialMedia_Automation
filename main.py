import requests
from openai import OpenAI
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
import os
import re

load_dotenv(override=True)


def generateContent(topic):
    print("Generating content...")

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Topic: {topic}",
        config=types.GenerateContentConfig(
            system_instruction="You are a Expert Social Media content creator. Write a compelling LinkedIn post based on the given topic. The post should be engaging, professional, and encourage interaction from the audience.\n\nAt the end of your response, provide a detailed image generation prompt that describes a visual to accompany this post. The image prompt should be relevant to the content you wrote. Start the image prompt with the exact text 'IMAGE_PROMPT:' on a new line.",
            thinking_config=types.ThinkingConfig(thinking_level="high")
        )
    )

    return response.text

    # client = OpenAI()

    # response = client.responses.create(
    #     model= "gpt-5-mini",
    #     instructions= "You are a Expert Social Media content creator. Write a compelling LinkedIn post based on the given topic. The post should be engaging, professional, and encourage interaction from the audience.",
    #     input= f"Topic: {topic}"
    # )

    # return response.output_text


if __name__ == "__main__":
    # topic = input("Enter the topic: ")

    topic = "How can we kill Procrastination and be more productive?"
    
    full_response = generateContent(topic)
    
    content = full_response
    image_prompt = topic

    if "IMAGE_PROMPT:" in full_response:
        parts = full_response.split("IMAGE_PROMPT:")
        content = parts[0].strip()
        image_prompt = parts[1].strip()
    

    print(f"\nGenerated Content:\n{content}\n")
    print(f"\nGenerated Image Prompt:\n{image_prompt}\n")
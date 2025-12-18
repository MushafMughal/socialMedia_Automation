import requests
from openai import OpenAI
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
import os
import re

load_dotenv(override=True)

def format_linkedin_text(text):
    """
    Converts Markdown bold (**text**) to Unicode bold characters for LinkedIn.
    """
    def to_bold(match):
        content = match.group(1)
        bold_text = ""
        for char in content:
            if 'a' <= char <= 'z':
                bold_text += chr(ord(char) + 0x1D41A - ord('a'))
            elif 'A' <= char <= 'Z':
                bold_text += chr(ord(char) + 0x1D400 - ord('A'))
            elif '0' <= char <= '9':
                bold_text += chr(ord(char) + 0x1D7CE - ord('0'))
            else:
                bold_text += char
        return bold_text

    return re.sub(r'\*\*(.*?)\*\*', to_bold, text)

def generateImage(prompt):
    print("Generating image...")

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt],
    )

    # image_parts = [part for part in response.parts if part.inline_data]
    # if image_parts:
    #     image = image_parts[0].as_image()
    #     image.save('weather_tokyo.png')
    #     image.show()

    for part in response.parts:
        if part.text is not None:
            print(part.text)

        if part.inline_data is not None:
            image = part.as_image()
            image.save("generated_image.png")
            return "generated_image.png"

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

def sendPost_linkedin(text, image_path):
    print("Sending post to LinkedIn...")
    url = "https://api25.unipile.com:15543/api/v1/posts"
    
    files = []
    if image_path and os.path.exists(image_path):
        files = [
            ("attachments", (os.path.basename(image_path), open(image_path, "rb"), "image/png"))
        ]

    payload = {
        "account_id": "FhOWYYCNSoST4cYtMsXDEw",
        "text": text
    }
    headers = {
        "accept": "application/json",
        "X-API-KEY": "y4NaOruH./A1O3D/+QnpmeTyHzQWR8esTOEf9Ata4P4K3LiXlTJM="
    }

    response = requests.post(url, data=payload, files=files, headers=headers)
    return response.text


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
    
    # Apply LinkedIn formatting (convert **bold** to Unicode bold)
    content = format_linkedin_text(content)
        
    print(f"\nGenerated Content:\n{content}\n")
    print(f"\nGenerated Image Prompt:\n{image_prompt}\n")
    
    image_file = generateImage(image_prompt)
    
    if content:
        response = sendPost_linkedin(content, image_file)
        print(f"\nPost Response: {response}")
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY") or os.getenv("GROQ_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME", "ai-practicum")

client = OpenAI(api_key=api_key, base_url=base_url)

print(f"Testing connection to: {base_url or 'default'} using model: {model_name}")
resp = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": "Jelaskan dalam satu kalimat: apa itu klasifikasi teks?"}],
    max_tokens=50,
    temperature=0
)
print("Response:", resp.choices[0].message.content)

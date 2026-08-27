# test_groq.py
# Sirf ye check karne ke liye ki Groq API se connection ho raha hai ya nahi

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",   # naya model, purana wala deprecated ho chuka hai
    api_key=os.getenv("GROQ_API_KEY")
)

response = llm.invoke("Say hello and tell me you are ready to help with F1 data analysis.")

print(response.content)
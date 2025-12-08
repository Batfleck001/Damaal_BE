import os
from groq import Groq
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#--- AI Integration -----

def groq_chat(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="openai/gpt-oss-20b",  
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=256,
    )
    return resp.choices[0].message.content

# ----- DB Integration --------


SUPABASE_URL = os.getenv("project_url")
SUPABASE_KEY = os.getenv("service_role")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert(tablename,data):
    return supabase.table(tablename).insert(data).execute()

def getall(tablename):
    return supabase.table(tablename).select("*").execute()
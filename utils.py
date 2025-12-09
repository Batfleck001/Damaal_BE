import os
from groq import Groq
from dotenv import load_dotenv
from supabase import create_client, Client
import json

load_dotenv()

#--- AI Integration -----
class Utils:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.SUPABASE_URL = os.getenv("project_url")
        self.SUPABASE_KEY = os.getenv("service_role")
        self.supabase: Client = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)
        
    def groq_chat(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=256,
        )
        return resp.choices[0].message.content

    # ----- DB Integration --------

    def insert(self, tablename,data):
        return self.supabase.table(tablename).insert(data).execute()

    def getall(self, tablename):
        return self.supabase.table(tablename).select("*").execute()
    
    def get(self, tablename, columnname):
        return self.supabase.table(tablename).select(columnname).execute()

    def last_updated_get(self, tablename, columnname):
        return (
            self.supabase.table(tablename)
            .select(columnname)
            .order("id", desc=True)
            .limit(1)
            .execute()
        )


    # ----- Utility functions ---------

    def add_json_nums(self, obj):
        total = 0
        if isinstance(obj, dict):
            for value in obj.values():
                total += self.add_json_nums(value)
        elif isinstance(obj, list):
            for item in obj:
                total += self.add_json_nums(item)
        elif isinstance(obj, (int,float)):
            total += obj
        return total
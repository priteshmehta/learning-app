from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseDB, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    def save_to_supabase(self, data):
        try:
            # Insert data into the "maths_questions" table
            response = self.client.table("maths_questions").insert(data).execute()
            if response is None:
                print(f"Error saving data: {response}")
            else:
                print(f"Response: {response}")
        except Exception as e:
            print(f"Failed to save data: {e}")
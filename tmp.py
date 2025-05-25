from openai import OpenAI
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions
import os
import psycopg2
from psycopg2 import sql

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def supabase_connection():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(postgrest_client_timeout=10,storage_client_timeout=10,schema="public",))
    return supabase

def save_to_supabase(supabase, data):
    try:
        # Insert data into the "chat_history" table
        response = supabase.table("maths_questions").insert(data).execute()
        if response is None:
            print(f"Error saving data: {response}")
        else:
            print (f"Response: {response}")    
    except Exception as e:
        print(f"Failed to save data: {e}")

def db_connection():    
    print("PASSWORD: ", PASSWORD)
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        print("Connection successful!")
        
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        
        # Example query
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Current Time:", result)

        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("Connection closed.")

    except Exception as e:
        print(f"Failed to connect: {e}")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def chat_gpt(client):
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # or "gpt-4"
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ])

    answer = response.choices[0].message.content
    return answer
if __name__ == "__main__":
    #answer = chat_gpt(client)
    #print("answer: {}".format(answer))  
    save_to_supabase(supabase_connection(), {"question": "What is the capital of India?", "answer": "New Delhi"})

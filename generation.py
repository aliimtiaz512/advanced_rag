from ingestion import collection
import chromadb
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
def generate_answer(query):
    results=collection.query(
        query_texts=[query],
        n_results=1
    )
    context=results['documents']
    groq_client=Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion=groq_client.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content":f"You are a helpful assistant. Answer the question using ONLY the provided context: {context}"
            },
            {
                "role":"user",
                "content":query,
            }
        ],
        model="openai/gpt-oss-120b",
    )

    return chat_completion.choices[0].message.content


def evaluate_query(query):
    groq_client=Groq(api_key=os.environ.get("GROQ_API_KEY"))
    system_prompt = (
        "You are a pre-retrieval query evaluator for a RAG system focused entirely on the novel 'The Great Gatsby'. "
        "Your job is to evaluate the user's query based on two criteria:\n"
        "1. Spelling and Grammar: Is the query readable and free of major typos?\n"
        "2. Meaning and Context: Does the query logically make sense and is it relevant to the topic of The Great Gatsby?\n\n"
        "Return a Confidence Score from 0 to 100 representing how well-formed and relevant the query is. "
        "Return ONLY a valid JSON object with a single key 'score' containing an integer. Example: {\"score\": 85}. Do not include anything else."
    )
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}"}
            ],
            model="openai/gpt-oss-120b",
        )
        content = chat_completion.choices[0].message.content
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_string = content[start_idx:end_idx+1]
            data = json.loads(json_string)
            return int(data.get("score", 0))
        return 0
    except Exception as e:
        print("Error evaluating query:", e)
        return 0

def generate_query_options(query):
    groq_client=Groq(api_key=os.environ.get("GROQ_API_KEY"))
    system_prompt = "You help users formulate better queries about the novel The Great Gatsby. Given a vague or misspelled query, provide exactly 5 clarified and well-formed query options. Return ONLY a valid JSON object with a key 'options' that maps to a list of 5 strings. Example: {\"options\": [\"opt1\", \"opt2\", \"opt3\", \"opt4\", \"opt5\"]}. Do not include any other text."
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Query: {query}"}
            ],
            model="openai/gpt-oss-120b",
        )
        content = chat_completion.choices[0].message.content
        
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_string = content[start_idx:end_idx+1]
            data = json.loads(json_string)
            return data.get("options", [])[:5]
        return []
    except Exception as e:
        print("Error generating options:", e)
        return []

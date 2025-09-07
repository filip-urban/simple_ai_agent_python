import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.agent import start_agent
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    prompt = sys.argv[1]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments, if no arguments are provided, you always run the Python file without any arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    start_agent(client, prompt, messages, config)


if __name__ == "__main__":
    main()

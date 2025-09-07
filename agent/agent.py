import sys

from google.genai import types

from config import MODEL
from functions.call_function import call_function


def start_agent(client, prompt, messages, config):
    # querry the model
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=config,
    )
    # add models response to the list of messages
    for message in response.candidates:
        messages.append(message.content)

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)
            function_call_result_message = function_call_result.parts[
                0
            ].function_response.response
            print(f"-> {function_call_result_message}")
            # create a message with the function call output
            result_message = types.Content(
                role="user",
                parts=[
                    types.Part(text=function_call_result_message["result"]),
                ],
            )
            messages.append(result_message)
    else:
        print(response.text)
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

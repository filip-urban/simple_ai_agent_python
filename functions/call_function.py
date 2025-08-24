from google.genai import types
import sys

sys.path.append("functions")

from config import WORKING_DIRECTORY
from get_file_content import get_file_content
from get_files_info import get_files_info
from run_python import run_python_file
from write_file import write_file


def function_name_to_function(function_name):
    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    return functions.get(function_name, None)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    function = function_name_to_function(function_call_part.name)
    if not function:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    result = function(WORKING_DIRECTORY, **function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

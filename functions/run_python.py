import os
import subprocess
from pathlib import Path
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_file_path = os.path.join(os.path.abspath(working_directory), file_path)
        if (
            not Path(full_file_path)
            .resolve()
            .is_relative_to(Path(working_directory).resolve())
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as exc:
        return f"Error: {exc}"
    try:
        python_bin = os.getcwd() + "/.venv/bin/python3"
        process_with_args = [python_bin]
        process_with_args.append(full_file_path)
        process_with_args.extend(args)
        process_result = subprocess.run(
            process_with_args,
            timeout=30,
            capture_output=True,
            cwd=working_directory,
            text=True,
        )
        result = ""
        if process_result.stdout:
            result = f"STDOUT:\n{process_result.stdout}"
        if process_result.stderr:
            if result:
                result += "\n"
            result += f"STDERR:\n{process_result.stderr}"
        if not result:
            result = "No output produced."
        if process_result.returncode:
            result += "Process exited with code X"
        return result
    except Exception as exc:
        return f"Error: executing Python file: {exc}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python file in the specified file path, constrained to the working directory. Optionally accepts a list of arguments. Always runs without argumenents, if no arguments are provided.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional. The list of arguments for the Python file.",
                default=[],
            ),
        },
    ),
)

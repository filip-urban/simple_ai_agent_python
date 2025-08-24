import os
from pathlib import Path
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        full_file_path = os.path.join(os.path.abspath(working_directory), file_path)
        if (
            not Path(full_file_path)
            .resolve()
            .is_relative_to(Path(working_directory).resolve())
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(Path(full_file_path).parent):
            os.makedirs(Path(full_file_path).parent)
        if os.path.isdir(full_file_path):
            return f"Error: destination is a directory."
        with open(full_file_path, "w+") as fh:
            fh.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as exc:
        return f"Error: {exc}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to the file in the specified file path, constrained to the working directory. If the destination file doesn't exist, creates the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
            ),
        },
    ),
)

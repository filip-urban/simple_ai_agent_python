import os
from pathlib import Path
from google.genai import types

from config import MAX_FILE_LENGTH


def get_file_content(working_directory, file_path):
    try:
        full_file_path = os.path.join(os.path.abspath(working_directory), file_path)
        if (
            not Path(full_file_path)
            .resolve()
            .is_relative_to(Path(working_directory).resolve())
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_file_path, "r") as fh:
            file_content = fh.read()
            if (len(file_content)) > MAX_FILE_LENGTH:
                return (
                    file_content[: MAX_FILE_LENGTH - 1]
                    + f'[...File "{file_path}" truncated at 10000 characters]'
                )
        return file_content
    except Exception as exc:
        return f"Error: {exc}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of the file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the contents of file from, relative to the working directory.",
            ),
        },
    ),
)

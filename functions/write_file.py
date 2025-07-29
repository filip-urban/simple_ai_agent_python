import os
from pathlib import Path


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

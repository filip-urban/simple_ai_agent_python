import os
from pathlib import Path


def get_files_info(working_directory, directory="."):
    try:
        files_info = f"Result for {f'\'{directory}\'' if directory != "." else "current"} directory:\n"
        full_directory_path = os.path.join(
            os.path.abspath(working_directory), directory
        )
        if (
            not Path(full_directory_path)
            .resolve()
            .is_relative_to(Path(working_directory).resolve())
        ):
            return f'{files_info}Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(os.path.abspath(full_directory_path)):
            return f'{files_info}Error: "{directory}" is not a directory'
        directory_contents = os.listdir(full_directory_path)
        for file in directory_contents:
            is_directory = False
            file_path = os.path.join(full_directory_path, file)
            file_size = os.path.getsize(file_path)
            if not os.path.isfile(file_path):
                is_directory = True
            files_info += (
                f" - {file}: file_size={file_size} bytes, is_dir={is_directory}\n"
            )
    except Exception as ex:
        return f"Error: {ex}"
    return files_info

import os
from config import *

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_file_full_path = os.path.normpath(os.path.join(working_dir_absolute, file_path))
        valid_target_file = os.path.commonpath([working_dir_absolute, target_file_full_path]) == working_dir_absolute

        if not valid_target_file:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(target_file_full_path):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_file_full_path) as file:
            file_content = file.read(NUMBER_OF_CHARS_TO_READ)
            if file.read(1):
                file_content += f'[...File "{target_file_full_path}" truncated at {NUMBER_OF_CHARS_TO_READ} characters]'
        return file_content

    except Exception as error:
        msg = str(error)
        return msg if msg.startswith("Error:") else f"Error: {msg}"


#JSON schema for use with OpenAI SDK
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file and displays the first 10,000 characters of the file. If file is longer than 10,000 characters it is truncated and a descriptive message is added.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to target file to be read, relative to the working directory",
                    },
                },
            },
        "required": ["file_path"]
        },
    }

import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_file_full_path = os.path.normpath(os.path.join(working_dir_absolute, file_path))
        valid_target_file = os.path.commonpath([working_dir_absolute, target_file_full_path]) == working_dir_absolute


        if not valid_target_file:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

        if os.path.isdir(target_file_full_path):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')

        os.makedirs(os.path.dirname(target_file_full_path), exist_ok=True)

        with open(target_file_full_path, mode='w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as error:
        msg = str(error)
        return msg if msg.startswith("Error:") else f"Error: {msg}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the specified content to the file defined in file_path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file that should be written to, relative to the working directory",
                    },
                "content": {
                    "type": "string",
                    "description": "Writes data defined by content argument to file defined by file_path",
                    },
                },
            },
        "required": ["file_path", "content"],
        },
    }

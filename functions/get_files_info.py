import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_dir_full_path = os.path.normpath(os.path.join(working_dir_absolute, directory))
        valid_target_dir = os.path.commonpath([working_dir_absolute, target_dir_full_path]) == working_dir_absolute

        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.isdir(target_dir_full_path):
            raise Exception(f'Error: "{directory}" is not a directory')

        dir_contents = os.listdir(target_dir_full_path)
        contents_metadata = []
        for entry in dir_contents:
            path_to_item = os.path.join(target_dir_full_path, entry)
            contents_metadata.append(f"- {entry}: file_size={os.path.getsize(path_to_item)} bytes, is_dir={os.path.isdir(path_to_item)}")
        return "\n".join(contents_metadata)

    except Exception as error:
        msg = str(error)
        return msg if msg.startswith("Error:") else f"Error: {msg}"

#JSON schema for use with OpenAI SDK
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    }
                }
            }
        }
    }

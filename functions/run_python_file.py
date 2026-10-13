import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_absolute = os.path.abspath(working_directory)
        target_file_full_path = os.path.normpath(os.path.join(working_dir_absolute, file_path))
        valid_target_file = os.path.commonpath([working_dir_absolute, target_file_full_path]) == working_dir_absolute

        if not valid_target_file:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.isfile(target_file_full_path):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')

        if not target_file_full_path.endswith('py'):
            raise Exception(f'Error: "{file_path}" is not a Python file')

        command = ["python", target_file_full_path]
        if args != None:
            ext_command = command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd=working_dir_absolute,
            capture_output=True,
            text=True,
            timeout=30
            )
        if completed_process.check_returncode():
            raise Error(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout == "" and completed_process.stderr == "":
            return "No output produced"
        else:
            return f"STDOUT: {completed_process.stdout}STDERR: {completed_process.stderr}"

    except Exception as error:
        msg = str(error)
        return msg if msg.startswith("Error:") else f"Error: executing Python file: {msg}"

#JSON schema for use with OpenAI SDK
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python (*.py) file located at a specified file path, relative to the working directory, with the specified arguments, if any.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to target file to be run, relative to the working directory",
                    },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                        },
                    },
                    "description": "A list of strings to be handed to the run python program as arguments. Can be empty."
                },
            },
        "required": ["file_path"],
        },
    }

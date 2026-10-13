#To activate the UV virtual environment in your CLI, change dir to '~/bootdev-ai-agent' and run the 'source .venv/bin/activate'

import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import *
from available_functions import *



def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("OpenRouter API key not found")

    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.user_prompt},
        ]
    for iteration in range(20):
        response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_functions,
                )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception("Function returned an empty result")
                if args.verbose:
                    print(f"-> {result_message['content']}")

        if not message.tool_calls:
            print(f"{message.content}")
            break

        else:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                if response.usage is None:
                    raise RuntimeError("Cannot access response usage property")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"Response: {message.content}")

    else:
        print(f"THis request required too many iterations of AI Model")
        sys.exit(1)


if __name__ == "__main__":
    main()

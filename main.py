import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from functions.call_function import available_functions, call_function

MAX_ITERATIONS = 20


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERATIONS):
        final_content = generate_content(client, messages, args.verbose)
        if final_content is not None:
            print("Final response:")
            print(final_content)
            return

    print(f"Error: agent did not produce a final response after {MAX_ITERATIONS} iterations")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        # temperature=0,
    )

    if not response.usage:
        raise RuntimeError("An OpenRouter error occurred, please try again")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose)
        if not result_message["content"]:
            raise RuntimeError(f"Fatal: no content returned for tool call {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)

    return None


if __name__ == "__main__":
    main()

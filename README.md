# Gemini Structured Output Handler

A robust and reusable Python wrapper for the Google Gemini API that simplifies getting structured JSON output.

This function is built on the `google-genai` client library and provides a clean, reliable interface to leverage the native JSON mode of the **Gemini 2.5 Flash** model. It properly handles system prompts, multi-turn chat history, temperature settings, and API key management, returning a parsed Python dictionary every time.

Say goodbye to unreliable string parsing and prompt-hacking for JSON output!

## Key Features

-   **Guaranteed JSON Output:** Uses Gemini's native `response_mime_type="application/json"` for reliable, valid JSON.
-   **Optimized for Gemini 2.5 Flash:** Specifically tailored for the speed and efficiency of the `gemini-2.5-flash` model.
-   **Structured Schema Definition:** Define your desired output using a simple Python dictionary.
-   **Full Chat History Support:** Natively handles multi-turn conversations for contextual responses.
-   **Flexible API Key Handling:** Pass the API key directly to the function or use an environment variable.
-   **Configurable:** Easily set the generation `temperature`.
-   **Error Handling:** Includes checks for API keys and gracefully handles API exceptions.
-   **Reusable & Clean:** A single, well-documented function to drop into any project.

## Prerequisites

-   Python 3.9+
-   A Google Gemini API Key with access to the Gemini 2.5 Flash model.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/gemini-json-handler.git
    cd gemini-json-handler
    ```

2.  **Install the required dependency:**
    ```bash
    pip install google-genai
    ```

3.  **Set your API Key (Optional):**
    You can pass the API key directly to the function. Alternatively, you can set it as an environment variable.
    ```bash
    # On Linux/macOS
    export GEMINI_API_KEY="YOUR_API_KEY"

    # On Windows (Command Prompt)
    set GEMINI_API_KEY="YOUR_API_KEY"
    ```

## Usage

The core of the repository is the `call_gemini_api` function. Here's how to use it:

```python
import os
import json
from gemini_handler import call_gemini_api # Assuming the code is in gemini_handler.py

# 1. Define your instructions and desired output structure
my_system_prompt = "You are an entity extraction expert. Analyze the user's text and extract key information into a structured JSON format."

my_output_schema = {
    "type": "object",
    "properties": {
        "project_name": {
            "type": "string",
            "description": "The name of the project mentioned."
        },
        "lead_person": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "title": {"type": "string"},
            }
        },
        "contact_email": {
            "type": "string",
            "description": "The contact email address found in the text."
        }
    },
    "required": ["project_name", "lead_person"]
}

# 2. Provide the new user message
new_user_input = "The new initiative is 'Project Phoenix', led by software engineer John Doe. His email is john.doe@example.com."

# 3. Get your API Key
# For security, load from environment variables or a secret manager
my_api_key = os.environ.get("GEMINI_API_KEY")

# 4. Call the function!
if my_api_key:
    try:
        structured_response = call_gemini_api(
            system_prompt=my_system_prompt,
            user_message=new_user_input,
            output_schema=my_output_schema,
            api_key=my_api_key # Pass the key directly
        )

        # 5. Use the result as a standard Python dictionary
        print("--- Parsed JSON Response ---")
        print(json.dumps(structured_response, indent=2))

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
else:
    print("ERROR: Please set the GEMINI_API_KEY environment variable.")

```

### 🚀 PRO-TIP: Generate Your Schema with AI!

Defining the `my_output_schema` dictionary by hand can be tedious, especially for complex objects. To make this even easier, you can use an AI assistant like Perplexity to generate the schema for you!

Just describe the JSON structure you need in plain English, and it can write the Python dictionary. This dramatically speeds up the entire development workflow.

See it in action with this example prompt: [https://www.perplexity.ai/search/you-are-helping-a-user-create-RNfInjo6TOeOlSaGKNK.FQ](https://www.perplexity.ai/search/you-are-helping-a-user-create-RNfInjo6TOeOlSaGKNK.FQ)

## Function Reference

`call_gemini_api(system_prompt, user_message, message_history=None, output_schema=None, model_name="gemini-2.5-flash-lite-preview-06-17", temperature=0.0, api_key=None)`

-   `system_prompt` (str): The master instruction for the model's behavior.
-   `user_message` (str): The latest user message to be processed.
-   `message_history` (list[dict], optional): A list of previous messages for conversational context.
-   `output_schema` (dict, optional): A dictionary defining the desired JSON output structure.
-   `model_name` (str, optional): The Gemini model to use. This wrapper is optimized for and defaults to `gemini-2.5-flash-lite-preview-06-17`.
-   `temperature` (float, optional): The generation temperature (0.0 for deterministic output).
-   `api_key` (str, optional): Your Gemini API key. If not provided, the function will use the `GEMINI_API_KEY` environment variable.

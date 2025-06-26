# Gemini Structured Output Handler

A robust and reusable Python wrapper for the Google Gemini API that simplifies getting structured JSON output.

This function is built on the `google-genai` client library and provides a clean, reliable interface to leverage the native JSON mode of models like **Gemini 2.5 Pro** and **Gemini 2.5 Flash**. It properly handles system prompts, multi-turn chat history, model selection, and temperature settings, returning a parsed Python dictionary every time.

Say goodbye to unreliable string parsing and prompt-hacking for JSON output!

## Key Features

- **Guaranteed JSON Output:** Uses Gemini's native `response_mime_type="application/json"` for reliable, valid JSON.
- **Structured Schema Definition:** Define your desired output using a simple Python dictionary.
- **Full Chat History Support:** Natively handles multi-turn conversations for contextual responses.
- **Configurable:** Easily change the Gemini model (`gemini-2.5-pro-preview-06-17`, `gemini-2.5-flash-lite-preview-06-17`, etc.) and `temperature`.
- **Error Handling:** Includes checks for API keys and gracefully handles API exceptions.
- **Reusable & Clean:** A single, well-documented function to drop into any project.

## Prerequisites

- Python 3.9+
- A Google Gemini API Key with access to Gemini 2.5 models.

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

3.  **Set your API Key:**
    Create an environment variable for your Gemini API key.
    ```bash
    # On Linux/macOS
    export GEMINI_API_KEY="YOUR_API_KEY"

    # On Windows (Command Prompt)
    set GEMINI_API_KEY="YOUR_API_KEY"
    ```

## Usage

The core of the repository is the `call_gemini_api` function. Here's how to use it:

```python
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

# 2. (Optional) Provide chat history for context
my_message_history = [
    {"role": "user", "text": "The first project is 'Apollo' led by Jane Smith."},
    {"role": "model", "text": '{"project_name": "Apollo", "lead_person": {"name": "Jane Smith", "title": null}, "contact_email": null}'}
]

# 3. Provide the new user message
new_user_input = "The second project is 'Project Phoenix', led by software engineer John Doe. His email is john.doe@example.com."

# 4. Call the function!
try:
    structured_response = call_gemini_api(
        system_prompt=my_system_prompt,
        user_message=new_user_input,
        message_history=my_message_history,
        output_schema=my_output_schema,
        model_name="gemini-2.5-flash-lite-preview-06-17", # Specify a Gemini 2.5 model
        temperature=0.0
    )

    # 5. Use the result as a standard Python dictionary
    print("--- Parsed JSON Response ---")
    print(json.dumps(structured_response, indent=2))

    print("\n--- Accessing Data ---")
    project = structured_response.get("project_name")
    lead_name = structured_response.get("lead_person", {}).get("name")
    print(f"Project: {project}")
    print(f"Lead Name: {lead_name}")

except ValueError as e:
    print(f"\nConfiguration Error: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")

```

## Function Reference

`call_gemini_api(system_prompt, user_message, message_history=None, output_schema=None, model_name="gemini-2.5-flash-lite-preview-06-17", temperature=0.0)`

-   `system_prompt` (str): The master instruction for the model's behavior.
-   `user_message` (str): The latest user message to be processed.
-   `message_history` (list[dict], optional): A list of previous messages for conversational context.
-   `output_schema` (dict, optional): A dictionary defining the desired JSON output structure.
-   `model_name` (str, optional): The Gemini model to use (e.g., `gemini-2.5-pro-preview-06-17`).
-   `temperature` (float, optional): The generation temperature (0.0 for deterministic output).

# gemini_handler.py

import os
import json
from google import genai
from google.genai import types

def _build_client_api_schema(schema_dict: dict) -> types.Schema:
    """
    Recursively builds a genai.types.Schema object from a Python dictionary
    for the genai.Client library.
    """
    type_map = {
        "string": types.Type.STRING, "number": types.Type.NUMBER,
        "integer": types.Type.INTEGER, "boolean": types.Type.BOOLEAN,
        "array": types.Type.ARRAY, "object": types.Type.OBJECT,
    }
    schema_type_str = schema_dict.get("type", "object").lower()
    gemini_type = type_map.get(schema_type_str)
    if not gemini_type:
        raise ValueError(f"Unsupported schema type: {schema_type_str}")

    properties = {k: _build_client_api_schema(v) for k, v in schema_dict.get("properties", {}).items()} or None
    items = _build_client_api_schema(schema_dict["items"]) if "items" in schema_dict else None
    
    return types.Schema(
        type=gemini_type,
        description=schema_dict.get("description"),
        properties=properties,
        items=items,
        required=schema_dict.get("required")
    )

def call_gemini_api(
    system_prompt: str,
    user_message: str,
    message_history: list[dict] | None = None,
    output_schema: dict | None = None,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0.0,
) -> dict:
    """
    Calls the Google Gemini API with structured output support using the genai.Client.

    This function serves as a robust wrapper to simplify interactions with the Gemini
    API, specifically for use cases requiring structured JSON output. It leverages
    Gemini's native JSON mode, ensuring the model's output is a valid, parsable
    JSON object that conforms to a user-defined schema.

    Args:
        system_prompt (str): The main instruction or context for the model's
            behavior throughout the conversation.
        user_message (str): The latest message from the user that the model
            should respond to.
        message_history (list[dict] | None, optional): A list of dictionaries
            representing the prior conversation turns. Each dictionary should have
            "role" ('user' or 'model') and "text" keys. Defaults to None.
        output_schema (dict | None, optional): A Python dictionary that defines the
            expected JSON structure of the model's response. If provided, the
            function will request JSON output. If None, a plain text response
            is requested. Defaults to None.
        model_name (str, optional): The specific Gemini model to be used for the
            API call (e.g., "gemini-2.5-flash").
            Defaults to "gemini-2.5-flash".
        temperature (float, optional): Controls the randomness of the output.
            A value of 0.0 is deterministic, while higher values (e.g., 0.7)
            produce more creative results. Defaults to 0.0.

    Returns:
        dict: A Python dictionary representing the parsed JSON response from the
              model. If `output_schema` is not provided, the dictionary will
              contain a single key, "text", with the model's plain text response.

    Raises:
        ValueError: If the 'GEMINI_API_KEY' environment variable is not set.
        Exception: Propagates any exceptions that occur during the API call,
                   such as authentication or network errors.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    client = genai.Client(api_key=api_key)

    contents = []
    if message_history:
        for msg in message_history:
            contents.append(types.Content(
                role=msg.get("role"),
                parts=[types.Part.from_text(text=msg.get("text"))]
            ))
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)]
    ))

    response_schema = None
    response_mime_type = "text/plain"
    if output_schema:
        response_schema = _build_client_api_schema(output_schema)
        response_mime_type = "application/json"

    generation_config = types.GenerateContentConfig(
        temperature=temperature,
        response_mime_type=response_mime_type,
        response_schema=response_schema,
        system_instruction=[types.Part.from_text(text=system_prompt)],
    )
    
    try:
        response = client.models.generate_content(
            model=f"models/{model_name}",
            contents=contents,
            config=generation_config,
        )
        
        response_text = response.text
        
        if output_schema:
            return json.loads(response_text)
        else:
            return {"text": response_text}

    except Exception as e:
        print(f"An error occurred during the Gemini API call: {e}")
        raise

if __name__ == '__main__':
    # This block demonstrates how to use the call_gemini_api function.
    # It will only run when the script is executed directly.
    
    print("--- Running Gemini API Handler Example ---")
    
    # 1. Define the system prompt, schema, and inputs
    my_system_prompt = "You are a travel agent. Extract the user's travel plan into a structured JSON object. Infer the travel method if not specified."
    new_user_input = "I need to book a trip from Paris to Tokyo for next month, from the 15th to the 22nd. I'll need a hotel."
    my_output_schema = {
        "type": "object",
        "properties": {
            "departure_city": {"type": "string"},
            "destination_city": {"type": "string"},
            "travel_dates": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"}
                }
            },
            "needs_hotel": {"type": "boolean"},
            "inferred_travel_method": {"type": "string"}
        },
        "required": ["departure_city", "destination_city", "travel_dates"]
    }

    try:
        # 2. Call the function
        structured_response = call_gemini_api(
            system_prompt=my_system_prompt,
            user_message=new_user_input,
            output_schema=my_output_schema,
            # The model defaults to a Gemini 2.5 model, but you can override it:
            # model_name="gemini-2.5-flash", 
            temperature=0.0
        )

        # 3. Print the results
        print("\n--- Parsed JSON Response ---")
        print(json.dumps(structured_response, indent=2))

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

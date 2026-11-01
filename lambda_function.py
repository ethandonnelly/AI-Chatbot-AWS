import json
import uuid

from botocore.exceptions import ClientError
from Chatbot import BedrockChatbot
from ConversationStore import DynamoDBConversationStore


# Format a response for API Gateway
def api_response(status, data):
    return {
        "statusCode": status,
        "body": json.dumps(data),
        "headers": {"Content-Type": "application/json"}
    }


def lambda_handler(event, context):

    # Convert the incoming JSON string into a Python dictionary
    try:
        data = json.loads(event.get("body") or "{}")
    except (ValueError, TypeError):
        return api_response(400, {"error": "Invalid JSON"})

    if not isinstance(data, dict):
        return api_response(400, {"error": "Invalid JSON object"})

    # Get and validate the user's prompt
    prompt = data.get("message")

    if not isinstance(prompt, str) or not 1 <= len(prompt.strip()) <= 1000:
        return api_response(400, {"error": "Invalid message"})

    # Get the conversation ID, or create one for a new chat
    chat_id = data.get("conversation_id")

    if chat_id is None:
        chat_id = str(uuid.uuid4())
    elif not isinstance(chat_id, str) or not 1 <= len(chat_id.strip()) <= 128:
        return api_response(400, {"error": "Invalid conversation ID"})

    # Create the database and chatbot objects
    database = DynamoDBConversationStore()
    chatbot = BedrockChatbot()

    # Load previous messages from DynamoDB
    chatbot.messages = database.load_history(chat_id)

    try:
        # Generate the AI response
        reply = chatbot.generate_response(prompt)

        # Save the updated conversation history
        database.save_history(chat_id, chatbot.messages)

    except ClientError as error:
        if error.response["Error"]["Code"] == "ThrottlingException":
            return api_response(429, {"error": "Bedrock limit reached"})
        raise

    # Return the AI reply and conversation ID
    return api_response(200, {
        "conversation_id": chat_id,
        "reply": reply
    })


import boto3


class BedrockChatbot:

    def __init__(self):

        # Connect to Amazon Bedrock in the Stockholm region
        self.bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name="eu-north-1"
        )

        # Choose the AI model
        self.model_id = "eu.amazon.nova-micro-v1:0"

        # Store the conversation history
        self.messages = []

    def generate_response(self, user_prompt):

        # STEP 1: Format the user's message for Bedrock
        user_message = {
            "role": "user",
            "content": [{"text": user_prompt}]
        }

        # STEP 2: Add the new message to the conversation

        # Copy the previous conversation history
        conversation = self.messages.copy()

        # Add the user's new message
        conversation.append(user_message)

        # STEP 3: Send the conversation to Amazon Bedrock and get a response
        response = self.bedrock_client.converse(
            modelId=self.model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 300,
                "temperature": 0.5
            }
        )

        # STEP 4: Extract the AI-generated response
        ai_reply = response["output"]["message"]["content"][0]["text"]

        # STEP 5: Add the AI response to the conversation
        assistant_message = {
            "role": "assistant",
            "content": [{"text": ai_reply}]
        }

        conversation.append(assistant_message)

        # STEP 6: Update the conversation history
        self.messages = conversation

        # Return the AI's response to Lambda
        return ai_reply

    def clear_history(self):

        # Clear the conversation history stored in this object
        self.messages.clear()

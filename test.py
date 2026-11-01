from ChatAPIClient import ChatAPIClient

# Create our API client
client = ChatAPIClient()

# Send a real prompt to our AWS backend
reply = client.send_api_request("Hello!")

# Display the AI's response
print("AI:", reply)

# Display the conversation ID
print("Conversation ID:", client.conversation_id)
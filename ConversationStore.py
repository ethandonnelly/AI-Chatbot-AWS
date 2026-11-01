import boto3

class DynamoDBConversationStore:
    def __init__(self):
        # Connect to DynamoDB
        self.dynamodb = boto3.resource("dynamodb",
                                       region_name="eu-north-1")

        # Connect to database table
        self.table = self.dynamodb.Table("cloudchat-conversations")

    def load_history(self, conversation_id):
        # Search for a conversation using ID
        response = self.table.get_item(Key={"conversation-id": conversation_id},
                                       ConsistentRead=True)

        # Get the conversation data from DynamoDB
        # If no conversation exists, return an empty dictionary
        item = response.get("Item", {})

        # Get the messages stored in the conversation.
        # If there are no messages, return an empty list
        return item.get("messages", [])

    def save_history(self, conversation_id, messages):
        # Keep 20 most recent messages to stop history becoming too large
        messages = messages[-20:]

        # Save the conversation to the DynamoDB table.
        self.table.put_item(Item={
                "conversation-id": conversation_id,
                "messages": messages})


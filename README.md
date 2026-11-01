
# AWS AI Chatbot

An AI chatbot developed in Python using AWS services,
including Amazon Bedrock, AWS Lambda, API Gateway
and DynamoDB.

I chose this project to gain practical experience with
AWS and develop my understanding of cloud infrastructure. Before starting this project, I had no experience with
AWS or building cloud-based applications. Due to this, I used AI-assisted development to help me write and
understand the AWS-related code, allowing me to learn
how the different services work together. The interface was independently coded by me using
CustomTkinter.

## Technologies Used

- **Python**
- **CustomTkinter** - GUI
- **Amazon Bedrock** - Generating AI responses
- **AWS Lambda** - Backend processing
- **Amazon API Gateway** - Receiving API requests
- **Amazon DynamoDB** - Storing conversation data

## How It Works

1. User sends a prompt through the GUI.
2. GUI calls the ChatAPIClient.
3. ChatAPIClient sends the request to API Gateway.
4. API Gateway invokes the AWS Lambda function.
5. Lambda retrieves conversation history from DynamoDB.
6. BedrockChatbot sends the conversation to Amazon Bedrock.
7. Lambda saves the updated conversation history.
8. The response is returned to the GUI.

## What I Learned

- **AWS Fundamentals** - Navigating the AWS Console and configuring services.
- **Boto3** - Using Python to interact with AWS.
- **Amazon Bedrock** - Connecting Python to a hosted AI model.
- **AWS Lambda** - Understanding serverless backend processing.
- **IAM** - Configuring roles and permissions.
- **DynamoDB** - Creating tables and storing conversations.
- **CloudWatch** - Investigating errors and debugging.

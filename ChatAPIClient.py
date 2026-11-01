import json
import boto3
import requests

from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


class ChatAPIClient:

    def __init__(self):

        # Address of API Gateway endpoint
        self.api_url = (
            "https://dg7jmylmk7.execute-api."
            "eu-north-1.amazonaws.com/chat"
        )

        self.region = "eu-north-1"

        # Create session to access AWS login credentials
        self.session = boto3.Session()

        # Store the current conversation ID
        # None means no conversation started
        self.conversation_id = None

    def send_api_request(self, prompt):

        # = STEP 1: Prepare request to send =

        # Store user's prompt in a dictionary
        data = {"message": prompt}

        # Include the conversation ID if one exists
        # Allows Lambda to load previous messages
        if self.conversation_id:
            data["conversation_id"] = self.conversation_id

        # Convert dictionary into JSON bytes
        # So it's in correct format to send to API gateway
        body = json.dumps(data).encode("utf-8")

        # = STEP 2: Get AWS login credentials =

        credentials = self.session.get_credentials()

        # Stop if AWS credentials are unavailable
        if credentials is None:
            raise RuntimeError("AWS credentials not found")

        # = STEP 3: Prepare and sign the HTTP request =

        # Describe the AWS request
        request = AWSRequest(
            method="POST",
            url=self.api_url,
            data=body,
            headers={"Content-Type": "application/json"}
        )

        # Sign the request using AWS credentials
        # API Gateway uses this to verify identity
        signer = SigV4Auth(
            credentials.get_frozen_credentials(),
            "execute-api",
            self.region
        )

        signer.add_auth(request)

        # = STEP 4: Send the request to API Gateway =

        response = requests.post(
            self.api_url,
            data=body,
            headers=dict(request.headers),
            timeout=45)

        # Convert the JSON response into a dictionary
        result = response.json()

        # = STEP 5: Check whether the request was successful =

        # Status 200 means the request succeeded
        if response.status_code != 200:
            # Get the error message returned by AWS
            error_message = result.get("error") or result.get("message") or "Unknown error"

            # Show both the HTTP status code and error message
            raise RuntimeError(
                f"HTTP {response.status_code}: {error_message}"
            )

        # = STEP 6: Store the conversation ID and return the reply =

        # Remember the ID so future messages use the same conversation
        self.conversation_id = result["conversation_id"]

        # Return the AI-generated response to GUI
        return result["reply"]

    def clear_history(self):
        # Forget current conversation ID
        # Lambda will create a new conversation on the next message
        self.conversation_id = None

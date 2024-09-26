import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextGenerationV1  # Replace with the actual service class if different
import config

class WatsonXClient:
    """
    A client to interact with the Allam model on IBM WatsonX.
    Handles IAM authentication and sending requests to the model.
    """
    def __init__(self, api_key, service_url):
        """
        Initialize the WatsonXClient with the provided API key and service URL.

        :param api_key: Your IBM WatsonX IAM API key.
        :param service_url: The endpoint URL of the Allam model on WatsonX.
        """
        # Initialize the authenticator
        self.authenticator = IAMAuthenticator(api_key)
        
        # Initialize the service client
        self.service = TextGenerationV1(authenticator=self.authenticator)
        self.service.set_service_url(service_url)
    
    def send_prompt(self, prompt, parameters=None):
        """
        Send a prompt to the Allam model and retrieve the generated response.

        :param prompt: The input text prompt for the model.
        :param parameters: (Optional) Dictionary of additional parameters for the model.
        :return: The generated text response from the model.
        """
        # Default parameters if none are provided
        if parameters is None:
            parameters = {
                "decoding_method": "greedy",
                "max_new_tokens": 1500,
                "repetition_penalty": 1
            }

        try:
            # Send the prompt to the model
            response = self.service.generate(
                prompt=prompt,
                decoding_method=parameters.get("decoding_method", "greedy"),
                max_new_tokens=parameters.get("max_new_tokens", 1500),
                repetition_penalty=parameters.get("repetition_penalty", 1)
            ).get_result()
            
            # Extract the generated text
            generated_text = response.get('generated_text', '').strip()
            return generated_text

        except Exception as e:
            # Handle exceptions (you might want to log these in a real application)
            raise Exception(f"Error while communicating with the Allam model: {str(e)}")

# Initialize the WatsonXClient with API key and service URL from config
watson_client = WatsonXClient(
    api_key=config.WATSON_API_KEY,
    service_url=config.WATSON_API_URL
)

def get_model_response(prompt, decoding_method="greedy", max_new_tokens=1500, repetition_penalty=1):
    """
    Convenience function to get a response from the Allam model.

    :param prompt: The input text prompt for the model.
    :param decoding_method: Decoding method to use (e.g., 'greedy').
    :param max_new_tokens: Maximum number of tokens to generate.
    :param repetition_penalty: Penalty for repetition.
    :return: The generated text response from the model.
    """
    parameters = {
        "decoding_method": decoding_method,
        "max_new_tokens": max_new_tokens,
        "repetition_penalty": repetition_penalty
    }

    try:
        response = watson_client.send_prompt(prompt, parameters)
        return response
    except Exception as e:
        # Handle exceptions as needed (logging, re-raising, etc.)
        raise e

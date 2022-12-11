import openai

import openai
import textwrap

# Set the API key
openai.api_key = "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"

# Define a function to generate responses using ChatGPT
def generate_response(prompt, n=1, max_tokens=540, temperature=0.5):
    # Use the `Completion` API to generate responses
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=textwrap.wrap(prompt, width=1024),
        max_tokens=max_tokens,
        temperature=temperature,
        n=n,
        stop=None,
    )

    # Return the generated response
    return response["choices"][0]["text"]

# Define a function to run a conversation using ChatGPT
def run_conversation():
    # Initialize the conversation
    conversation = []

    # Run the conversation loop
    while True:
        # Prompt the user for the next message
        user_message = input("User: ")

        # Break the loop if the user inputs "goodbye"
        if user_message.lower() == "goodbye":
            break

        # Add the user's message to the conversation
        conversation.append(user_message)

        # Use ChatGPT to generate a response
        gpt_response = generate_response(prompt="\n".join(conversation))

        # Print the response
        print(f"Bot: {gpt_response}")

# Run the conversation
run_conversation()

from openai import OpenAI
import os
import base64

class OpenAIChat:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not self.client.api_key:
            raise ValueError("OpenAI API key is not set. Please set the 'OPENAI_API_KEY' environment variable.")
        self.model = model
        self.conversation_history = []

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def chat(self, text_input, image_path=None):
        if image_path:
            # For vision queries, convert the new message to vision format
            base64_image = self.encode_image(image_path)
            new_message = {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_input},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
            # Convert previous messages to vision format if they exist
            formatted_history = [
                {"role": msg["role"], 
                 "content": [{"type": "text", "text": msg["content"]}]}
                for msg in self.conversation_history
            ]
            messages = formatted_history + [new_message]
            model = "gpt-4o"
        else:
            # For text-only queries, use the standard format
            messages = self.conversation_history + [{"role": "user", "content": text_input}]
            model = self.model

        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=2048
        )

        assistant_message = response.choices[0].message.content
        # Update conversation history for both vision and text queries
        self.conversation_history.append({"role": "user", "content": text_input})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

if __name__ == "__main__":
    chat_instance = OpenAIChat(model="gpt-4")
    response = chat_instance.chat("Hello, how are you?")
    print(response + '\n\n\n')
    response = chat_instance.chat("what do you see?", image_path="/Users/ribhavkapur/Desktop/everything/omega_labs/agents/claude-computer-use-macos/temp_ss.png")
    print(response + '\n\n\n')
    response = chat_instance.chat("what was my previous message?", image_path="/Users/ribhavkapur/Desktop/everything/omega_labs/agents/claude-computer-use-macos/temp_ss.png")
    print(response + '\n\n\n')
    response = chat_instance.chat("do you have context of our previous messages? if so, what was my first question and what was my second question?")
    print(response + '\n\n\n')
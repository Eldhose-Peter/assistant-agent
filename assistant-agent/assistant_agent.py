from intent_classifier.intent_classifier import IntentClassifier
from task_manager import create_task, remove_task, list_tasks
import subprocess

class AssistantAgent:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.classifier.load_model()

    def generate_response(self, prompt):
        """Generates response using the Mistral model from Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "run", "mistral"],
                input=prompt,
                capture_output=True,
                text=True
            )

            # Print errors if the command fails
            if result.returncode != 0:
                return f"Error: {result.stderr.strip()}"

            return result.stdout.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def handle_input(self, user_input):
        intent = self.classifier.predict_intent(user_input)

        if intent == "summarization":
            prompt = f"""
                    You are an intelligent AI assistant specializing in text summarization. 
                    Your task is to read and analyze the given content and provide a **concise, accurate, and coherent summary**. 
                    Ensure that you retain the key information while making it **brief and readable**.
                    
                    ### Guidelines:
                    - Extract the **most important points**.
                    - Keep the summary **clear and structured**.
                    - If applicable, format key points into **bullet points**.
                    - Preserve the **original intent and tone**.
                    - Avoid unnecessary details or repetition.
                    
                    ### Input Text:
                    user_input : {user_input}
                    task_list : {list_tasks()}
                    
                    ### Expected Output:
                    Provide a structured and concise summary of the above text.
                    """

            return self.generate_response(prompt)

        elif intent == "task_creation":
            task_id = str(hash(user_input))
            return create_task(task_id, user_input)
        elif intent == "task_removal":
            words = user_input.split()
            task_id = words[-1]
            if task_id in list_tasks():
                return remove_task(task_id)
            else:
                return "Please specify task name or task Id for me to delete"
        else:
            return self.generate_response(user_input)


if __name__ == "__main__":
    agent = AssistantAgent()
    print("Welcome to the AI Assistant. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = agent.handle_input(user_input)
        print(response)

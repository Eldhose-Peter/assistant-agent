from db_manager import read_db_schema, read_previous_queries, execute_query
import subprocess

class AssistantAgent:
    def __init__(self):
        pass

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
        prompt = f"""
                You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. 
                Unless otherwise specified, do not return more than 10 rows.

                The user provides a question and you provide SQL. You will only respond with SQL code and not with any explanations.

                Here is the relevant table information:
                {read_db_schema()}
               
                Below are some example questions and the expected SQL query output:
                {read_previous_queries()}

                ### Input Question:
                user_input : {user_input}
                
                ### Expected Output:
                Provide a structured and concise summary of the above text.
                """

        return self.generate_response(prompt)

if __name__ == "__main__":
    agent = AssistantAgent()
    print("Welcome to the AI Assistant. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = agent.handle_input(user_input)
        print("Agent response:", response)

        query_response = execute_query(response)
        print("Query response:", query_response)

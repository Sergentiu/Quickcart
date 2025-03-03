from openai import OpenAI

client = OpenAI()

# Create an Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

# Function to create a new thread
def create_thread():
    thread = client.beta.threads.create()
    return thread.id

# Function to add a message to the thread
def add_message(thread_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message.id

# Function to run the assistant on the thread
def run_assistant(thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Assist the user with their query."
    )
    return run
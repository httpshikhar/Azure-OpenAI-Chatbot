import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import streamlit as st

# Load environment variables
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-02-15-preview"
)

# Read subject and question from files



# Function to generate the detailed response
def generate_response(subject, question):
    prompt = f"""You are an expert tutor specializing in {subject}. Provide a detailed, clear, and comprehensive response to the question: {question}. 
    Ensure the content is:
    1. Complete: Cover all aspects of the question without skipping details.
    2. Structured: Use bullet points, numbered lists, or headings where appropriate for easy readability.
    3. Simple and Direct: Explain concepts in straightforward terms, avoiding unnecessary complexity.
    Focus exclusively on answering the question. Avoid introductions, conclusions, or repeating parts of the prompt. Ensure the response is logically coherent and finishes fully, without cutting off mid-sentence."""

    with open("prompt.txt", "w") as f:
        f.write(prompt)
    # Generate response using Azure OpenAI
    response = client.chat.completions.create(
        model=azure_oai_deployment,
        max_tokens=500,
        messages=[
            {"role": "system", "content": "You are a prominent teacher and an educator."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return the generated response content
    return response.choices[0].message.content.strip()


# Function to generate the title based on the response
def generate_title(response_content):
    title_prompt = f"""Based on the content: {response_content}, generate two vertically aligned, simple images in a clear and organized layout. 
    The images should visually represent the concept with basic elements, avoiding unnecessary detail or complexity. Ensure both images are easy to understand and educational, with no controversial or sensitive content."""

    # Generate title using Azure OpenAI
    title_response = client.chat.completions.create(
        model=azure_oai_deployment,
        max_tokens=100,
        messages=[
            {"role": "user", "content": title_prompt}
        ]
    )

    return title_response.choices[0].message.content.strip()


# Main function to handle generation and display
def generation():
    subject = st.sidebar.selectbox("Select Subject : ", ["Biology", "History", "Coding", "Physics"])
    question = st.sidebar.text_input("Enter your question : ")
    # Generate detailed response
    if st.sidebar.button("Submit"):
        response = generate_response(subject, question)

        # Write detailed response to Streamlit and file
        st.write(response)
        with open("generated_text.txt", "w") as file:
            file.write(response)

        # Generate and save the title
        title = generate_title(response)
        with open("title.txt", "w") as file:
            file.write(title)

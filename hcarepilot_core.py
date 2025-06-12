from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import retrieval_qa
from langchain.prompts import PromptTemplate
import gradio as gr
from gradio.themes.base import Base
from textblob import TextBlob 
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('mongo_url'))
dbName = "medical"
collectionName = "medicineBook"
collection = client[dbName][collectionName]
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

vectorStore = MongoDBAtlasVectorSearch(collection, embeddings)

def query_data(query):
    corrected_query = str(TextBlob(query).correct())
    print(f"Corrected Query: {corrected_query}")

    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

    # Step 1: Generate initial answer directly using LLM
    initial_answer = llm.generate([corrected_query]).generations[0][0].text
    print(f"\nInitial AI Response:\n{initial_answer}")

    start_time = time.time()

    # Step 2: Post-hoc Retrieval
    post_hoc_docs = vectorStore.similarity_search(initial_answer, k=3)

    if post_hoc_docs:
        combined_docs = " ".join([doc.page_content for doc in post_hoc_docs])

        refinement_prompt = PromptTemplate(
            template=(
                "Refine the answer based on the given data\n\n"
                "Initial Answer: {initial_answer}\n\n"
                "Retrieved Evidence: {evidence}\n\n"
                "Refined Answer:"
            ),
            input_variables=["initial_answer", "evidence"],
        )

        refinement_input = refinement_prompt.format(
            initial_answer=initial_answer,
            evidence=combined_docs
        )

        # Refine the initial answer with supporting evidence
        refined_answer = retrieval_qa(llm, chain_type="stuff").run(
            input_documents=post_hoc_docs,
            question=refinement_input
        )

        end_time = time.time()
        print(f"\nRefined Answer:\n{refined_answer}")
        print(f"Query Response Time: {end_time - start_time:.2f} seconds")
        return refined_answer
    else:
        print("No supporting evidence found for refinement.")
        return initial_answer


with gr.Blocks(theme=Base(), title="MEDICAL LLM") as demo:
    gr.Markdown("Medical LLM")
    textbox = gr.Textbox(label="Enter your Question:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        output2 = gr.Textbox(lines=1, max_lines=10, label="Output Results")
    button.click(query_data, textbox, outputs=[output2])    

demo.launch()

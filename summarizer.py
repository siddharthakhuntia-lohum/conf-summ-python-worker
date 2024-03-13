from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv
import logging

load_dotenv()
log_format = "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.DEBUG,filename='data.log', filemode='w', format=log_format, datefmt=date_format)

from utils.helper import num_tokens_from_string

MODEL_NAME = "gpt-3.5-turbo"
MODEL_MAX_TOKENS = 10000  # 16K tokens is the max for GPT-3.5-turbo
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0,
                 openai_api_key=OPENAI_API_KEY, model_name=MODEL_NAME)


def summarize(text: str) -> str:
    """
    Summarize the given transcript using the language model chain.

    Args:
        text (str): The transcript to summarize.

    Returns:
        str: The summarized text.
    """
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    
    

    CURRENT_TOKENS = num_tokens_from_string(text, MODEL_NAME)
    
    logging.info(f"Current tokens: {CURRENT_TOKENS}")


    if CURRENT_TOKENS < MODEL_MAX_TOKENS:
        logging.info("Summarizing using the 'stuff' chain")
        return stuff_summarize(docs)

    prompt_template = """Write a concise summary of the following extracting the key information:


    {text}


    CONCISE SUMMARY:"""

    question_prompt = PromptTemplate(template=prompt_template,
                                     input_variables=["text"])

    refine_template = (
        "Your job is to produce a final summary\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original summary"
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )
    chain = load_summarize_chain(llm,
                                 chain_type="refine",
                                 question_prompt=question_prompt,
                                 refine_prompt=refine_prompt)

    output_summary = chain.invoke({"input_documents": docs})

    return output_summary['output_text']


def stuff_summarize(docs: list) -> str:
    # prompt_template = """Write a concise bullet point summary of the following:

    # {text}

    # CONSCISE SUMMARY IN BULLET POINTS:"""

    prompt_template = """Write a concise summary with minimum 500 wrords of the following extracting the key information :


    {text}


    CONCISE SUMMARY:"""

    PROMPT = PromptTemplate(template=prompt_template,
                                         input_variables=["text"])
    chain = load_summarize_chain(llm,
                                 chain_type="stuff",
                                 prompt=PROMPT)

    output_summary = chain.invoke(docs)

    return output_summary['output_text']

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_experiments.services.file_manager import generate_output_file
from langchain_experiments.services.pdf_service import load_file
from langchain_experiments.services.text_splitter import split_document_tokenized
from langchain_experiments.user_input.console import get_rich_console_instance
from utils import timeit

from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
console = get_rich_console_instance()

# TODO: Refactor this file into different classes with appropriate responsabilities.
@timeit
def summary():
    load_dotenv()

    file_documents = load_file()
    documents_splitted = split_document_tokenized(file_documents)

    console.print(f'There are: {len(documents_splitted)} document(s) in your document')

    # TODO: Refactor this
    total_tokens = 0
    file_name  = generate_output_file()
    with open(file_name, "w", encoding='utf-8') as text_file:
        # TODO: I could paralellize this call, for now it works ok.
        text = ""
        for doc in documents_splitted:
            #ns = chat_prompt.format_prompt(text=doc.page_content).to_messages()
            current_page = doc.metadata['page']

            text_file.write(f'\n ----------Start of Page {current_page} --------------- \n')
            summary = summarizer(doc.page_content, max_length=130, min_length=30, do_sample=False)
            for summary_element in summary:
                text_file.write(summary_element["summary_text"])

            text_file.write(f'\n ----------End of Page {current_page} --------------- \n')

    console.print(f'Total tokens used: {total_tokens}, Total spent: {get_usd_from_total_tokens(total_tokens)}')

def get_document_for_selected_pages(document, pages_selected):
    if pages_selected is not None:
        new_doc_splitted = []
        for doc in document:
            if doc.metadata['page'] in pages_selected and len(doc.page_content.split()) > 2: # TODO: Improve this, random number 2, but it is to check if is not an empty page or a page with only 2 words.
                doc.page_content.replace("\n", "")
                new_doc_splitted.append(doc)
        return new_doc_splitted
    else:
        return document

def get_usd_from_total_tokens(total_tokens_used):
    return (total_tokens_used /1000 )* 0.002 #0.002 is current model(gpt-3.5-turbo) price per 1k tokens

@timeit
# Rewrite this function
def sumarize_text(chat, ns, text_file, current_page):

    result = chat.generate([ns])
    text_file.write(f'\n ----------Start of Page {current_page} ---------------')
    text_file.write(f'\n {result.generations[0][0].text}')
    text_file.write(f'\n ----------End of Page {current_page} ---------------')
    
    total_tokens_used = result.llm_output['token_usage']['total_tokens']
    console.print(f"Page {current_page} finished, totak_tokens: {total_tokens_used} in usd {get_usd_from_total_tokens(total_tokens_used)}, 1k tokens = 0.002 USD")
    return total_tokens_used

if __name__ == "__main__":
    summary()

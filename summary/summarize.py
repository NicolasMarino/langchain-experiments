from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from utils import timeit
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import CharacterTextSplitter
from rich.console import Console
import datetime
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
import os

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
console = Console()



# TODO: Refactor this file into different classes with appropriate responsabilities.
@timeit
def summary(pages_selected, file_path, model_name):
    load_dotenv()

    chat = ChatOpenAI(model_name=model_name, temperature=0) 

    loader = PyPDFLoader(file_path)
    document = loader.load_and_split()

    document = get_document_for_selected_pages(document, pages_selected)

    console.print(f'There are: {len(document)} document(s) in your document')

    text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(tokenizer, chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(document)

    console.print(f'Texts slpitted {len(docs)} pages')

    template="Ignore all prior instructions. Act as an expert on summarization, outlining and structuring. Your style of writing should be informative and logical. Provide me with a summary of a text.The summary should include as much content as possible while keeping it lucid and easy to understand.If the text has multiple parts with multiple chapters, format the bigger sections as a big heading, then the chapters in sub-headings, and in another section then the bullet points of the chapters in normal font. The structure should be the name of a chapter of the text, then Bulletpoints of the contents of said chapter. The bulletpoints must be included, as they provide the most information. Generate the output in markdown format. Do not remind me what I asked you for. Do not apologize. Do not self-reference. I would give you the text i want you to summarize, do not use another data to enhance it, just resume the best ideas for this text, please. Give me the summary in Spanish, the text is: "
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # TODO: Change this.
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_dir = "./summary/outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{output_dir}/output_{current_time}.txt"

    total_tokens = 0

    with open(filename, "w", encoding='utf-8') as file:
        # TODO: I could paralellize this call, for now it works ok.
        for doc in docs:
            ns = chat_prompt.format_prompt(text=doc.page_content).to_messages()
            current_page = doc.metadata['page']
            total_tokens += sumarize_text(chat, ns,file, current_page)
    
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
    # WISHLIST: I could get some directory and load all the pdfs from there. 
    file_path = console.input("Input file path: ")
    
    page_index_option = console.input("What pages do you want to summarize? A) All pages B) Only some pages. ")

    pages = None
    if page_index_option.lower() == "a":
        pages = None
    elif page_index_option.lower() == "b":
        indexStart = int(console.input("Start page (0-indexed): "))
        indexEnd = int(console.input("End page (inclusive): "))
        pages = (indexStart,indexEnd)

    # TODO: Be able to change this.
    model_name = "gpt-3.5-turbo"

    summary(pages,file_path,model_name)

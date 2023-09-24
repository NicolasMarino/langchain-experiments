from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_experiments.services.file_manager import generate_output_file
from langchain_experiments.services.text_splitter import split_document_tokenized
from langchain_experiments.services.pdf_service import load_file
from utils import timeit
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_experiments.user_input.console import get_rich_console_instance


console = get_rich_console_instance()

# TODO: Refactor this file into different classes with appropriate responsabilities.
@timeit
def summary(model_name):
    load_dotenv()

    chat = ChatOpenAI(model_name=model_name, temperature=0) 

    file_documents = load_file()
    documents_splitted = split_document_tokenized(file_documents)

    console.print(f'Texts slpitted {len(documents_splitted)} pages')

    # Prompt to summarize
    template="Ignore all prior instructions. Act as an expert on summarization, outlining and structuring. Your style of writing should be informative and logical. Provide me with a summary of a text.The summary should include as much content as possible while keeping it lucid and easy to understand.If the text has multiple parts with multiple chapters, format the bigger sections as a big heading, then the chapters in sub-headings, and in another section then the bullet points of the chapters in normal font. The structure should be the name of a chapter of the text, then Bulletpoints of the contents of said chapter. The bulletpoints must be included, as they provide the most information. Generate the output in markdown format. Do not remind me what I asked you for. Do not apologize. Do not self-reference. I would give you the text i want you to summarize, do not use another data to enhance it, just resume the best ideas for this text, please. Give me the summary in Spanish, the text is: "
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # FIXME: Saving file
    total_tokens = 0
    file_name  = generate_output_file()
    with open(file_name, "w", encoding='utf-8') as file:
        # TODO: I could paralellize this call, for now it works ok.
        for doc in documents_splitted:
            chat_prompt_formatted = chat_prompt.format_prompt(text=doc.page_content).to_messages()
            current_page = doc.metadata['page']
            total_tokens += sumarize_text(chat, chat_prompt_formatted, file, current_page)

    console.print(f'Result in: {file_name}. Total tokens used: {total_tokens}, Total spent: {get_usd_from_total_tokens(total_tokens)}')


def get_usd_from_total_tokens(total_tokens_used):
    return (total_tokens_used /1000 )* 0.002 #0.002 is current model(gpt-3.5-turbo) price per 1k tokens

@timeit
# Rewrite this function
def sumarize_text(chat, chat_prompt_formatted, file, current_page):

    result = chat.generate([chat_prompt_formatted])
    file.write(f'\n ----------Start of Page {current_page} ---------------')
    file.write(f'\n {result.generations[0][0].text}')
    file.write(f'\n ----------End of Page {current_page} ---------------')
    
    total_tokens_used = result.llm_output['token_usage']['total_tokens']
    console.print(f"Page {current_page} finished, total_tokens: {total_tokens_used} in usd {get_usd_from_total_tokens(total_tokens_used)}")
    return total_tokens_used

if __name__ == "__main__":
    # WISHLIST: I could get some directory and load all the pdfs from there. 
    
    # TODO: Be able to change this.
    model_name = "gpt-3.5-turbo"

    summary(model_name)

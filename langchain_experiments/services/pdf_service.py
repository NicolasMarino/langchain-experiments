from typing import List
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document

from langchain_experiments.user_input.console import get_rich_console_instance

console = get_rich_console_instance()


def get_document_for_selected_pages(documents: List[Document], pages_selected):
    if pages_selected is not None:
        new_doc_splitted = []
        for document in documents:
            if document.metadata['page'] in pages_selected and len(document.page_content.split()) > 2: # TODO: Improve this, random number 2, but it is to check if is not an empty page or a page with only 2 words.
                document.page_content.replace("\n", "")
                new_doc_splitted.append(document)
        return new_doc_splitted
    return documents

# WISHLIST: I could get some directory and load all the pdfs from there. 
def load_file()->List[Document]:

    # This could be in another file
    file_path = console.input("Input file path: ")

    page_index_option = console.input("What pages do you want to summarize? A) All pages B) Only some pages. ")

    pages = None
    if page_index_option.lower() == "b":
        indexStart = int(console.input("Start page (0-indexed): "))
        indexEnd = int(console.input("End page (inclusive): "))
        pages = (indexStart,indexEnd)

    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split()

    return get_document_for_selected_pages(documents, pages)

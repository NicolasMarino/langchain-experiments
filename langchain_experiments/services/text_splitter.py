    
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from transformers import GPT2TokenizerFast
from langchain.docstore.document import Document

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def split_document_tokenized(documents:  List[Document])-> List[Document]:
    text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(tokenizer, chunk_size=500, chunk_overlap=0)
    return text_splitter.split_documents(documents)

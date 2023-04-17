from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from utils import timeit

def main():
    load_dotenv()
    llm = OpenAI(temperature=0,model_name="text-davinci-002")

    loader = UnstructuredPDFLoader("./textbooks/-.pdf")
    data = loader.load()

    print (f'{len(data)} document(s) in your data')
    print (f'There are {len(data[0].page_content)} characters in your document')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(data)

    print (f'Texts slpitted {len(docs)} documents')
        ## Stuff chain.
    #prompt_template = """Replace with a real prompt: {text}"""
    #PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    #chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
    ## Map reduce chain.
    #chain = load_summarize_chain(llm, chain_type="map_reduce")
    #sumarize_text(chain, texts)

@timeit
def sumarize_text(chain, docs):

    with get_openai_callback() as cb:
        text_file = open("results/resume_map_reduce.txt", "w")
        text_file.write(chain.run(docs))
        text_file.close()
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

if __name__ == "__main__":
    main()

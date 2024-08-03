import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.schema.runnable import RunnablePassthrough

# LLM Model 정의 code
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def create_RAG():
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    repo = "kyujinpy/Ko-PlatYi-6B"
    model = AutoModelForCausalLM.from_pretrained(
            repo,
            return_dict=True,
            torch_dtype=torch.float16,
            device_map='auto'
    )
    tokenizer = AutoTokenizer.from_pretrained(repo, quantization_config=bnb_config, device_map="auto")

    # RAG Model 정의 code
    '''
    pip install에서 오류 발생 시 실행
    import locale
    def getpreferredencoding(do_setlocale = True):
        return "UTF-8"
    locale.getpreferredencoding = getpreferredencoding
    '''

    text_generation_pipeline = pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        temperature=0.8,
        return_full_text=True,
        max_new_tokens=1000,
    )

    # RAG에서 사용할 template 정의
    prompt_template = """
    ### [INST]
    지시사항: 주어진 요리를 조리할 때 필요한 재료와 조리 과정을 작성하세요. 재료를 자세하고 정확하게 작성해주세요. 기존의 레시피를 참고하면서 완전 똑같게 작성하지는 말아주세요.
    여기 조리해야 할 요리 이름이 있습니다. 요리 이름 :

    {question}

    ###
    참고 레시피 :
    {context}

    ### 재료 및 레시피 :
    [/INST]
    """

    basic_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

    # Create prompt from prompt template
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    # llm chain 생성
    llm_chain = LLMChain(llm=basic_llm, prompt=prompt)

    # Retriever config 정의
    loader = PyPDFLoader("/content/drive/MyDrive/recipe_book.pdf")
    pages = loader.load_and_split()

    # 레시피 평균 길이가 400~500 자 인 것을 감안 하여 청크 사이즈 설정
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 250, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)

    # ko-sbert로 임베딩
    model_name = "jhgan/ko-sbert-nli"
    encode_kwargs = {'normalize_embeddings': True}

    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs
    )

    # cos sim 기준으로 3개의 chunk retrieve
    db = FAISS.from_documents(texts, hf)
    retriever = db.as_retriever(
                                search_type="similarity",
                                search_kwargs={'k': 3}
                            )

    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
        | llm_chain
    )

def main():

    create_RAG()

    st.title("FOM Recipe Generator with RAG")

    user_food = st.text_area("검색하고 싶은 요리를 적어주세요 :")

    if 'generated_recipe' not in st.session_state:
        if st.button('Generate', key = 'generated_recipe'):
            result = rag_chain.invoke(user_food)
            st.session_state['generated_recipe'] = result
            st.markdown('### 재료 및 레시피')
            st.markdown(result, unsafe_allow_html=True)
        else :
            st.warning("검색을 원하는 요리를 먼저 입력해주세요.")

    else :
        st.markdown('### 재료 및 레시피')
        st.markdown(st.session_state['generated_recipe'], unsafe_allow_html = True)

    if 'generated_recipe' in st.session_state and st.button('참고 레시피 보기'):
        st.markdown('### 참고 레시피')
        references = ""
        for i in result['context']:
            references += f"참고한 레시피: {i['page_content']} / 출처 페이지: {i['metadata']['page']}\n\n"
        st.markdown(references, unsafe_allow_html = True)
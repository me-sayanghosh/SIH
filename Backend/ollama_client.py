from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langdetect import detect

# Initialize Ollama LLM
llm = ChatOllama(
    model="llama3:8b",   # replace with your installed model
    temperature=0.7,
    max_tokens=50
)

parser = StrOutputParser()

def build_chain(language: str):
    """
    Build a chain with dynamic language response.
    """
    prompt_template = PromptTemplate(
        template=f"Give a short summary in {language} for: {{user_input}}",
        input_variables=["user_input"]
    )
    return RunnableSequence(prompt_template, llm, parser)

def build_chain(lang_code: str):
    """
    Build a chain with dynamic language response.
    """
    if lang_code == "en":
        template = "Answer briefly in English: {user_input}"
    else:
        template = "निम्नलिखित प्रश्न का उत्तर हिंदी में दीजिए: {user_input}"

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["user_input"]
    )
    return RunnableSequence(prompt_template, llm, parser)


from langdetect import detect

def query_ollama(user_text):
    """
    Sends user_text to the local Ollama LLM via LangChain and returns the response
    in the same language as input.
    """
    if not user_text:
        return "⚠️ No input provided.", "en"

    # Detect input language
    lang_code = detect(user_text)   # e.g., 'hi' or 'en'

    # Build chain dynamically
    chain = build_chain(lang_code)

    # Run chain
    output = chain.invoke({"user_input": user_text})

    return output.strip(), lang_code


from langdetect import detect

def detect_language(text):
    try:
        lang_code = detect(text)
    except:
        return "en"  # fallback to English if detection fails

    # Normalize: only allow 'hi' or 'en'
    if lang_code == "hi":
        return "hi"
    elif lang_code == "en":
        return "en"
    elif lang_code == "sw":  # Romanized Hindi sometimes shows as Swahili
        return "hi"
    else:
        return "en"  # default to English
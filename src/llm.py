
from src.prompt import prompt_template

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


chat_model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0,
)

def llm_call(text):

    prompt = prompt_template.format(text=text)

    response = chat_model(
        [
            SystemMessage(content="You are an expert in clinical research documentation."),
            HumanMessage(content=prompt)
                           ]
                           )

    return response.content

import logging

from src.prompt import prompt_template

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


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

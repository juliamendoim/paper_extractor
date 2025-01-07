
from src.data_models import LLMOutput

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


parser = JsonOutputParser(pydantic_object=LLMOutput)

prompt_template = PromptTemplate(
    input_variables=["text"],
    template=("""
        Extract each objective and endpoint from the following text as individual statements. For each statement:
        1. Assign a class for the category `section_level_1` (choices: primary-objective, secondary-objective, exploratory-objective).
        2. Assign a class for the category `section_level_2` (choices: efficacy-objective, safety-and-tolerability-objective, pharmacokinetic-objective).
        3. Assign an outcome measure (e.g., PFS, DCR, OS, Quality of Life, Safety and tolerability, Pharmacokinetics, ORR).
        {format_instructions}
        
        Text: 
        {text}
    """),
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

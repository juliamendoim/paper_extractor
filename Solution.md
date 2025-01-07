# Thought process

Create an endpoint that takes a folder with pdf papers and returns a structured file with objectives and endpoints of each paper.

## PDF Processing
1. Use a PDF python library that can handle the table of content. 
2. Use regex to extract the pages corresponding to titles that contain the keywords "objectives" and "endpoints"
3. Extract the content of these pages only, keeping in mind that original structure is key to solve the extraction, so consecutive pages should be kept in a continuous text.

## LLM call
4. Build a prompt that explains the task, adds the provided examples as few shot examples, and sends consecutively the pages.
5. Query an LLM service such as OpenAI or Anthropic
6. For better results, send three consecutive queries:
    - one for extracting the text of each statement
    - one for assigning labels (section levels) for each statement extracted
    - one for extracting the outcome meassure for each statement extracted

## DF and saving to file
7. Structure results in a pandas DF
8. Save DF to a file

## Alternative Paths and Possible Issues


### 1. PDF is corrupt and the library can not parse de TOC
#### Solution: 

- Use an OCR and parse the TOC using regex

    #### Caveats: 

    - OCRs like Tesseract use a dpi parameter that is strongly dependant on each image, resulting in poor generalization. 
    - OCRs are slow
    - Poor general result that can lead to poor extraction with regex


### 2. The words "objectives" and "endpoints" appear in unexpected contexts leading to wrong results. 

#### Solution:

- Use an LLM to make sure the pieces of information are correct.

#### Solution 2: 

- Improve the regex

### 3. Limitations in LLM calls because of privacy or budget:

#### Solution: 
- Run a local LLM

    #### Caveats: 

    - Local LLMs are slow and take up much space

    - Faster local LLMs have poor results

#### Solution 2: 
- Use a classification model to assign levels and a NER model to extract the outcome meassue

    #### Caveats: 
    - Annotated Data is needed

#### Solution 3: 

- Extract information purely based on regex

    #### Caveats: 

    - Insanely specific for each case

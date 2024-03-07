# ICD11-demo
Experiment with ICD11 classification for texts

# Scripts
## _01_load_icd.ipynb
This script loads the ICD11 classification from the csv file and saves only 
necessary columns to the new csv file.

## _02_construct_chroma_idx.ipynb
This script constructs the chroma index for the ICD11 classification. Should be
run after the _01_load_icd.ipynb script.

## _03_parse_doc.ipynb
This document shows main steps of the parsing the document and extracting the
ICD11 codes from the text in non-interactive mode.

## st_app.py
The interactive streamlit app. To run the app, execute the following command:
```bash
streamlit run st_app.py
```

# Docker
## Build the image
```bash
docker build -t atepeq/icd11-demo .
```

## Run the container
```bash
docker run -p 8501:8501 atepeq/icd11-demo
```
After that, open the app in the browser: http://localhost:8501

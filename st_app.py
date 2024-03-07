from pathlib import Path

import numpy as np
import pandas as pd
import chromadb
from transformers import pipeline
import streamlit as st

st.set_page_config(page_title="ICD-11 Code Prediction", layout="wide")


@st.cache_resource
def get_index() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path="idx/icd11")


def get_collection(client: chromadb.ClientAPI) -> chromadb.Collection:
    return client.get_collection(
        name="icd11_titles",
        # metadata={"hnsw:space": "cosine"},
    )


@st.cache_resource
def read_classifier() -> pd.DataFrame:
    return pd.read_csv("data/ICD-11-MMS-en-cleaned.csv.zip").fillna('')


@st.cache_resource
def get_model():
    return pipeline(model="AkshatSurolia/ICD-10-Code-Prediction", task="feature-extraction",
                    max_tokens=64)


client = get_index()
collection = get_collection(client)
classifier = read_classifier()
vectorizer = get_model()

st.title("ICD-11 Code Prediction Demo")
filenames = (Path("data") / "policies").glob("*.txt")
filenames = sorted([Path(f).name for f in filenames])

with st.sidebar:
    st.subheader("Policy Documents")
    fn_to_num = {f: i for i, f in enumerate(filenames)}
    fn_to_size = {f: (Path("data") / "policies" / f).stat().st_size for f in filenames}
    filename = st.radio(
        "Select a policy document", list(filenames),
        format_func=lambda x: f"{fn_to_num[x]}: {x} ({fn_to_size[x] / 1024:.2f} KB)")


@st.cache_data(max_entries=10_000)
def vectorize(text: str) -> np.ndarray:
    return vectorizer(text.strip(), return_tensors=True)[0].mean(dim=0).numpy()


def get_categories(text: str, threshold: float) -> list[str]:
    embedding = vectorize(text).tolist()
    results = collection.query(query_embeddings=embedding, n_results=5)
    codes = [c for c, d in zip(results["ids"][0], results["distances"][0]) if d < threshold]
    return codes


def render_doc(filename: str):
    txt = (Path("data") / "policies" / filename).read_text(encoding="utf-8").strip()
    # replace nspb with space
    txt.replace("\xa0", " ")
    paragraphs = txt.splitlines()
    st.subheader(filename)
    threshold = st.slider("Threshold", min_value=400, max_value=2000, value=1000, step=5)

    pb_txt = f"Processing {len(paragraphs)} paragraphs..."
    pb = st.progress(0, text=pb_txt)
    categories = []
    for n, p in enumerate(paragraphs):
        pb.progress(n / len(paragraphs), text=pb_txt)
        categories.append(get_categories(p, threshold))
    pb.progress(1, text="Processing has done!")

    df = pd.DataFrame.from_dict({
        "Paragraph": paragraphs,
        "Category": [", ".join(c) for c in categories],
    })
    st.table(df)


if filename:
    render_doc(filename)

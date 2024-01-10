from typing import Any, Dict, List, Optional

import argparse

from llama_index.schema import Document, NodeWithScore, TextNode
from llama_index.retrievers import BaseRetriever
from llama_index.indices.query.schema import QueryBundle
from llama_index import SimpleDirectoryReader
from llama_index.schema import TransformComponent
from llama_index.ingestion import IngestionPipeline

import re
import unicodedata


# def parsing_args():
#     parser = argparse.ArgumentParser()


class TextCleaner(TransformComponent):
    def __call__(self, nodes, **kwargs):
        for node in nodes:
            lowercase = node.text
            remove_link = re.sub(
                r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)",
                "",
                lowercase,
            ).replace("&amp;", "&")
            remove_bullet = "\n".join(
                [
                    T
                    for T in remove_link.split("\n")
                    if "•" not in T and "baca juga:" not in T
                ]
            )
            remove_accented = (
                unicodedata.normalize("NFKD", remove_bullet)
                .encode("ascii", "ignore")
                .decode("utf-8", "ignore")
            )
            remove_parentheses = re.sub(
                "([\(\|]).*?([\)\|])", "\g<1>\g<2>", remove_accented
            )
            remove_punc = re.sub(r"[^\w\d.\s]+", " ", remove_parentheses)
            remove_num_dot = re.sub(r"(?<=\d)\.|\.(?=\d)|(?<=#)\.", "", remove_punc)
            remove_extra_whitespace = re.sub(r"^\s*|\s\s*", " ", remove_num_dot)
            node.text = ".".join(
                [
                    s
                    for s in remove_extra_whitespace.strip().split(".")
                    if len(s.strip()) > 10
                ]
            ).replace("_", "")

        return nodes


class ColBERTRetriever(BaseRetriever):
    """Custom retriever."""

    def __init__(
        self, rag_obj: Any, index_name: str, top_k: int = 10, **kwargs: Any
    ) -> None:
        """Init params."""
        try:
            import ragatouille  # noqa
        except ImportError:
            raise ValueError(
                "RAGatouille is not installed. Please install it with `pip install ragatouille`."
            )
        self.rag_obj = rag_obj
        self.index_name = index_name
        self.top_k = top_k

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve."""
        results = self.rag_obj.search(query_bundle.query_str, k=self.top_k)
        result_nodes = []
        for result in results:
            result_nodes.append(
                NodeWithScore(
                    node=TextNode(text=result["content"]), score=result["score"]
                )
            )
        return result_nodes


if __name__ == "__main__":
    reader = SimpleDirectoryReader(input_dir="./html2pdf/")
    index_name = "resume"
    index_path = None

    nodes = reader.load_data()
    pipeline = IngestionPipeline(
        transformations=[
            TextCleaner(),
        ],
    )
    nodes = pipeline.run(documents=nodes)
    nodes_txt = [node.get_content() for node in nodes]

    try:
        from ragatouille import RAGPretrainedModel
    except ImportError:
        raise ValueError(
            "RAGatouille is not installed. Please install it with `pip install ragatouille`."
        )
    
    if index_path is None:
        RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
        index_path = RAG.index(index_name=index_name, collection=nodes_txt)
    else:
        RAG = RAGPretrainedModel.from_index(index_path)

    while True:
        query = input("Query: ")
        top_k = int(input("Top k: "))
        results = RAG.search(query, k=top_k)
        for result in results:
            print(result["content"])
            print("Score: ", result["score"])
            print("====================================")

    

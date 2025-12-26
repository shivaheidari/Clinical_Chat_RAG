"""Embedding utilities.

Small helpers to convert embedding vectors to the expected numeric
format and to format responses for a Web API skill.
"""

from typing import List

import numpy as np


def convert_to_float32(embeddings: List[float]) -> List[float]:
    """Convert OpenAI float64 embeddings to float32 for Azure AI Search."""
    return np.array(embeddings, dtype=np.float32).tolist()


def process_webapi_response(values: List[dict]) -> List[dict]:
    """Format a list of records into a WebApiSkill-like response.

    Each input record may provide the embedding under `data.embedding`
    or directly under `embedding`.
    """
    results = []
    for record in values:
        record_id = record.get("recordId")
        embedding = record.get("data", {}).get("embedding") or record.get("embedding")

        if embedding:
            emb_f32 = convert_to_float32(embedding)
            results.append({
                "recordId": record_id,
                "data": {"embedding": emb_f32},
                "errors": None,
                "warnings": None,
            })
        else:
            results.append({
                "recordId": record_id,
                "data": {"embedding": None},
                "errors": [{"message": "No embedding"}],
            })

    return [{"values": results}]

import numpy as np
from typing import List, Any

def convert_to_float32(embeddings: List[float]) -> List[float]:
    """Convert OpenAI float64 embeddings → float32 for Azure AI Search"""
    return np.array(embeddings, dtype=np.float32).tolist()

def process_webapi_response(values: List[dict]) -> List[dict]:
    """Simulate WebApiSkill response format"""
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
                "warnings": None
            })
        else:
            results.append({
                "recordId": record_id,
                "data": {"embedding": None},
                "errors": [{"message": "No embedding"}]
            })
    return [{"values": results}]

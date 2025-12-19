"""
Simple HTTP endpoint to convert embeddings from float64 to float32.
Deploy to Azure Functions or run locally for testing.
"""
import json
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/convert_embedding', methods=['POST'])
def convert_embedding():
    """
    Expects JSON body matching Azure Cognitive Search Web API skill format:
    {
      "values": [
         {"recordId": "1", "data": {"embedding": [0.1, 0.2, ...] }},
         ...
      ]
    }

    Returns same shape with converted embeddings under `data.embedding`.
    """
    try:
        payload = request.get_json(force=True)
        results = []
        for record in payload.get("values", []):
            record_id = record.get("recordId")
            embedding = None
            # input may be nested under data or directly present depending on skill
            if isinstance(record.get("data"), dict):
                embedding = record.get("data").get("embedding")
            else:
                embedding = record.get("embedding")

            if embedding is None:
                results.append({
                    "recordId": record_id,
                    "errors": [],
                    "data": {"embedding": None}
                })
                continue

            # convert to float32 and back to list
            try:
                emb_f32 = np.array(embedding, dtype=np.float32).tolist()
            except Exception as e:
                results.append({
                    "recordId": record_id,
                    "errors": [{"message": f"conversion error: {e}"}],
                    "data": {"embedding": None}
                })
                continue

            results.append({
                "recordId": record_id,
                "errors": [],
                "data": {"embedding": emb_f32}
            })

        return jsonify({"values": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=5000, debug=True)

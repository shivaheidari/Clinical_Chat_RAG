from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexer

import json
with open("confings/azure_keys.json") as f:
    keys = json.load(f)

SEARCH_ENDPOINT = keys["SEARCH_ENDPOINT"]
SEARCH_ADMIN_KEY = keys["SEARCH_ADMIN_KEY"]
INDEX_NAME = "mimic-rag-index"
DATASOURCE_NAME = "mimic-notes-datasource2025nov"
SKILLSET_NAME = "clinical-chunk-embed-skillset"

client = SearchIndexerClient(
    endpoint=SEARCH_ENDPOINT,
    credential=AzureKeyCredential(SEARCH_ADMIN_KEY)
)

#created indexer- connects DataSource -> SkillSet -> Index
indexer = SearchIndexer(

    name="mimic-clinical-indexer",
    data_source_name=DATASOURCE_NAME,
    target_index_name=INDEX_NAME,
    skillset_name=SKILLSET_NAME,

 field_mappings=[],  
    output_field_mappings=[
        # SplitSkill output "chunks" → chunk_text
        {
            "sourceFieldName": "/document/chunks/*",
            "targetFieldName": "chunk_text",
        },
        # EmbeddingSkill output → embedding_vector
        {
            "sourceFieldName": "/document/chunks/*/embedding_vector",
            "targetFieldName": "embedding_vector",
        },
    ],
)


result = client.create_or_update_indexer(indexer)
client.run_indexer("mimic-clinical-indexer")

print("🚀 Indexer created and running!")
print("⏳ Check progress in Azure Portal → your Search service → Indexers")
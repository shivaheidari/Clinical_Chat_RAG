from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
SearchIndex, 
SimpleField, 
SearchField,
SearchFieldDataType,
SearchableField, 
VectorSearch,
HnswAlgorithmConfiguration, 
HnswParameters,
VectorSearchProfile
)

import os
import json

with open("confings/azure_keys.json") as f:
    keys = json.load(f)

SEARCH_ENDPOINT = keys["SEARCH_ENDPOINT"]
SEARCH_ADMIN_KEY = keys["SEARCH_ADMIN_KEY"]
INDEX_NAME = "mimic-rag-index-dec"

#creating index client
index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, 
                                 credential=AzureKeyCredential(SEARCH_ADMIN_KEY))

#configure vector search (HNSW)

vector_search = VectorSearch(

    algorithms=[HnswAlgorithmConfiguration(

        name="cl-hnsw",
        parameters=HnswParameters(
            m=4,
            ef_construction=200,
            ef_search=100,
            metric="cosine"
        )
    )] , profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="cl-hnsw")]
)
# define fields (shcema)

fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SimpleField(
        name="patient_id",
        type=SearchFieldDataType.String,
        filterable=True,
        facetable=True,
    ),
    SimpleField(
        name="section",
        type=SearchFieldDataType.String,
        filterable=True,
        facetable=True,
    ),
    SearchableField(
        name="chunk_text",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchField(
        name="embedding_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="hnsw-profile",
    ),
]

index = SearchIndex(

    name=INDEX_NAME,
    fields=fields,
    vector_search=vector_search
)


result = index_client.create_or_update_index(index)
print(f"index '{result.name}' created/updated")
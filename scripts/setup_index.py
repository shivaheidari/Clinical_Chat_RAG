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

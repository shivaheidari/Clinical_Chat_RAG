from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import(

    SearchIndexerDataSourceConnection,
    SearchIndexerSkillset,
    SplitSkill,
    AzureOpenAIEmbeddingSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SplitSkillLanguage,
    SearchIndexerDataContainer,
    CognitiveServicesByKey
)

import os 
import json

with open("confings/azure_keys.json") as f:
    keys = json.load(f)

SEARCH_ENDPOINT = keys["SEARCH_ENDPOINT"]
SEARCH_ADMIN_KEY = keys["SEARCH_ADMIN_KEY"]
STORAGE_CONNECTION_STRING = keys["STORAGE_CONNECTION_STRING"]
AZURE_OPENAI_ENDPOINT = keys["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_KEY = keys["AZURE_OPENAI_KEY"]

CONTAINER_NAME = "notes"
BLOB_FOLDER_PATH = ""
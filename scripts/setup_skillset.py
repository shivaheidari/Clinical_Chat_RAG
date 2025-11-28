from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import(

    SearchIndexerDataSourceConnection,
    SearchIndexerDataSourceType,
    SearchIndexerSkillset,
    SplitSkill,
    AzureOpenAIEmbeddingSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SplitSkillLanguage,
    SearchIndexerDataContainer,
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
SKILLSET_NAME = "clinical-chunk-embed-skillset"
DATASOURCE_NAME = "mimic-notes-datasource2025nov"

indexer_client = SearchIndexerClient(
    endpoint=SEARCH_ENDPOINT,
    credential=AzureKeyCredential(SEARCH_ADMIN_KEY)

)

data_source = SearchIndexerDataSourceConnection(name=DATASOURCE_NAME,
                                                type=SearchIndexerDataSourceType.AZURE_BLOB,
                                                description="MIMIC clinical notes in blob storage",
                                                connection_string=STORAGE_CONNECTION_STRING,
                                                container=SearchIndexerDataContainer(
                                                    name="notes"))


indexer_client.create_or_update_data_source_connection(data_source)
print(f"✅ Data source '{DATASOURCE_NAME}' created")

skillset = SearchIndexerSkillset(

    name=SKILLSET_NAME,
    description="Split discharge summaries into 250-word chunks",
    #skill1 chunking 
    skills=[
        SplitSkill(
        name="split-clinical-notes",
        description="split disharge summries into 250-word chunks",
        context="/document",
        default_language_code=SplitSkillLanguage.EN,
        text_split_mode="sentences",
        maximum_page_length=250,
        inputs=[InputFieldMappingEntry(name="text", source="/document/content")], 
        outputs=[OutputFieldMappingEntry(name="textItems", target_name="chunks")]
    ),
    #skill2 generate embedding
    AzureOpenAIEmbeddingSkill(
        name="clinical-embeddings",
        description="embed clinical chunks",
        context="/document/chunks/*",
        resource_url=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        deployment_name="text-embedding-3-small",
        model_name="text-embedding-3-small",
        inputs=[InputFieldMappingEntry(name="text", source="/document/chunks/*")],
        outputs=[OutputFieldMappingEntry(name="embedding", target_name="embedding_vector")]
        )]

)

indexer_client.create_or_update_skillset(skillset)
print(f"✅ Skillset '{SKILLSET_NAME}' created")
print("📋 Skills: Text splitting + Azure OpenAI embeddings")
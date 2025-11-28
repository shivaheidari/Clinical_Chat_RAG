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
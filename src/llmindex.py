from llama_index.core import VectorStoreIndex, SummaryIndex
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import QueryEngineTool

# Create different query engines
vector_query_engine = vector_index.as_query_engine()
sql_query_engine = sql_database.as_query_engine()

# Define tools with descriptions
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for answering questions about company policies, documentation, and internal knowledge"
)

sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description="Useful for queries requiring structured data like sales figures, customer counts, or financial metrics"
)

# Create router
router_query_engine = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(),
    query_engine_tools=[vector_tool, sql_tool]
)

# Query automatically routes to the right engine
response = router_query_engine.query("What were our Q3 sales numbers?")
# Automatically routes to SQL engine

response = router_query_engine.query("What's our refund policy?")
# Automatically routes to vector store

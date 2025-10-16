from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal

# Define routing schema
class RouteQuery(BaseModel):
    """Route query to appropriate datasource."""
    datasource: Literal["vectorstore", "web_search", "direct_response"] = Field(
        description="Choose vectorstore for company docs, web_search for current events, or direct_response for general knowledge"
    )
    reasoning: str = Field(description="Brief explanation for routing decision")

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create router prompt
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at routing user queries to the appropriate data source.
    
    Choose where to route based on query type:
    - vectorstore: Company-specific information, internal docs, policies
    - web_search: Current events, real-time data, recent news
    - direct_response: General knowledge, definitions, explanations
    
    Analyze the query and make the best routing decision."""),
    ("human", "{query}")
])

# Create router chain
router_chain = router_prompt | llm.with_structured_output(RouteQuery)

# Route a query
def route_query(query: str):
    result = router_chain.invoke({"query": query})
    print(f"Route: {result.datasource}")
    print(f"Reasoning: {result.reasoning}")
    return result.datasource

# Example usage
route_query("What is our company's remote work policy?")
# Output: vectorstore - Query asks about internal company policy

route_query("Who won the Super Bowl last night?")
# Output: web_search - Query requires current event information

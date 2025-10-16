from semantic_router import Route
from semantic_router.encoders import OpenAIEncoder
from semantic_router.routers import SemanticRouter

# Define routes with example utterances
vectorstore_route = Route(
    name="vectorstore",
    utterances=[
        "What are our company policies on remote work?",
        "Tell me about our product features",
        "What's in the documentation about API limits?",
        "Explain our refund policy"
    ]
)

web_search_route = Route(
    name="web_search",
    utterances=[
        "What are the latest news about AI?",
        "Who won the game yesterday?",
        "What's the current stock price?",
        "Latest developments in quantum computing"
    ]
)

direct_response_route = Route(
    name="direct_response",
    utterances=[
        "What is machine learning?",
        "Explain Python decorators",
        "How does photosynthesis work?",
        "What's the capital of France?"
    ]
)

# Initialize encoder and router
encoder = OpenAIEncoder()
router = SemanticRouter(
    encoder=encoder, 
    routes=[vectorstore_route, web_search_route, direct_response_route],
    auto_sync="local"
)

# Route queries
query = "What's our vacation policy?"
route_choice = router(query)
print(f"Routing to: {route_choice.name}")  # Output: vectorstore

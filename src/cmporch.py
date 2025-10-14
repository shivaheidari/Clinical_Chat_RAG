
from langgraph import Graph, Node, Edge

# Define nodes with logic
def start_node(state):
    state['message'] = "Hello! How can I assist you?"
    return state

def process_query_node(state):
    query = state.get('user_input')
    # Imagine calling an LLM or tool here
    state['response'] = f"Processed query: {query}"
    return state

def human_review_node(state):
    # Route to human if query is complex
    if 'complex' in state.get('response', ''):
        state['needs_human'] = True
    else:
        state['needs_human'] = False
    return state

def end_node(state):
    state['message'] = "Thank you for using the service."
    return state

# Define edges with conditional logic
def edge_start_to_process(state):
    return 'process_query'  # Always go to process_query after start

def edge_process_to_review(state):
    if state.get('needs_human'):
        return 'human_review'
    else:
        return 'end'

def edge_review_to_end(state):
    return 'end'

# Create nodes
nodes = {
    'start': Node(start_node),
    'process_query': Node(process_query_node),
    'human_review': Node(human_review_node),
    'end': Node(end_node),
}

# Create edges
edges = {
    ('start', 'process_query'): Edge(edge_start_to_process),
    ('process_query', 'human_review'): Edge(edge_process_to_review),
    ('human_review', 'end'): Edge(edge_review_to_end),
}

# Create graph
graph = Graph(nodes=nodes, edges=edges, start_node='start')

# Run graph with initial state
state = {'user_input': "Tell me a complex question"}
final_state = graph.run(state)
print(final_state['message']) 

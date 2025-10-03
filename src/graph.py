import networkx as nx

G = nx.DiGraph()

# Example: create nodes for topics and docs
G.add_node("Cloud Computing", type="topic")
G.add_node("doc1.pdf", type="document")
G.add_edge("Cloud Computing", "doc1.pdf", relation="covers")

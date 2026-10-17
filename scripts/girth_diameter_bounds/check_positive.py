"""One graph property predicate, copied exactly from the accepted reference."""
import networkx as nx

def require(condition, message):
    if not condition:
        raise ValueError(message)

def graph_properties(raw):
    raw = raw.strip()
    graph = nx.from_graph6_bytes(raw)
    require(nx.is_connected(graph), 'disconnected first witness')
    return graph, [len(graph), min(dict(graph.degree()).values()),
                   max(dict(graph.degree()).values()), nx.girth(graph),
                   nx.diameter(graph), int(nx.is_bipartite(graph))]

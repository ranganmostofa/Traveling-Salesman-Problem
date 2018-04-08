from UndirectedGraph import UndirectedGraph
from Node import Node
from Edge import Edge


v1 = Node("v1", dict(), set())
v2 = Node("v2", dict(), set())

g = UndirectedGraph({v1, v2})

print(g.add_edge(0.10, dict(), v1, v2))
print(set(g.get_edges()))


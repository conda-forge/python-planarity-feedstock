from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory

import planarity


assert planarity.__version__ == "1.0.0"
assert planarity.gp_GetProjectVersionFull() == "5.0.0.0"

path = [(0, 1), (1, 2), (2, 3)]
assert planarity.is_planar(path)
assert planarity.is_planar({0: [1], 1: [0, 2], 2: [1]})

k5 = list(combinations(range(5), 2))
assert not planarity.is_planar(k5)
assert sorted(planarity.kuratowski_edges(k5)) == k5

k33 = [(u, v) for u in range(3) for v in range(3, 6)]
assert not planarity.is_planar(k33)
assert planarity.kuratowski_edges(path) == []

graph = planarity.PGraph([(1, 2)])
assert graph.ascii() == "1\n|\n2\n \n"
assert set(graph.nodes()) == {1, 2}
assert graph.edges() == [(1, 2)]
for _, data in graph.nodes(include_drawplanar_vertex_info=True):
    assert set(data) == {"vertex_position", "vertex_start", "vertex_end"}
for _, _, data in graph.edges(include_drawplanar_edge_info=True):
    assert set(data) == {"edge_position", "edge_start", "edge_end"}

with TemporaryDirectory() as directory:
    filename = Path(directory) / "graph.txt"
    planarity.PGraph([(1, 2)]).write(str(filename))
    assert filename.read_text() == "N=2\n1: 2 0\n2: 1 0\n"

# Exercise the new graph and graph6 extension modules as well as the classic API.
for order, expected in [(4, planarity.OK), (5, planarity.NONEMBEDDABLE)]:
    full_graph = planarity.Graph()
    full_graph.gp_EnsureVertexCapacity(order)
    full_graph.gp_EnsureEdgeCapacity(order * (order - 1))
    for u, v in combinations(range(1, order + 1), 2):
        assert full_graph.gp_AddEdge(u, 0, v, 0) == planarity.OK
    assert full_graph.gp_GetN() == order
    assert full_graph.gp_GetM() == order * (order - 1) // 2

    writer = planarity.G6WriteIterator(full_graph)
    writer.g6_InitWriterWithString()
    writer.g6_WriteGraph()
    encoded = writer.g6_FreeWriter()

    restored = planarity.Graph()
    reader = planarity.G6ReadIterator(restored)
    reader.g6_InitReaderWithString(encoded)
    reader.g6_ReadGraph()
    assert restored.gp_GetN() == order
    assert restored.gp_GetM() == order * (order - 1) // 2
    reader.g6_FreeReader()

    full_graph.gp_ExtendWith_Planarity()
    assert full_graph.gp_Embed(planarity.EMBEDFLAGS_PLANAR) == expected

from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory

import planarity


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
for _, data in graph.nodes(data=True):
    assert set(data) == {"pos", "start", "end"}
for _, _, data in graph.edges(data=True):
    assert set(data) == {"pos", "start", "end"}

with TemporaryDirectory() as directory:
    filename = Path(directory) / "graph.txt"
    planarity.PGraph([(1, 2)]).write(str(filename))
    assert filename.read_text() == "N=2\n1: 2 0\n2: 1 0\n"

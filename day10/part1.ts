const input = `89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732`;

type MapNode = {
  value: number;
  neighbors: MapNode[];
  summits: Set<MapNode> | null;
};

const trailheads: MapNode[] = [];
// Convert the input into a 2D array of nodes.
const map: MapNode[][] = input.split("\n").map((line, i) =>
  line.split("").map((val, j) => {
    const node: MapNode = {
      value: Number(val),
      neighbors: [],
      summits: null,
    };
    if (node.value === 0) {
      trailheads.push(node);
    }
    return node;
  })
);
// link the nodes
map.forEach((line, i) => {
  line.forEach((node, j) => {
    if (i > 0) {
      node.neighbors.push(map[i - 1][j]);
    }
    if (i < map.length - 1) {
      node.neighbors.push(map[i + 1][j]);
    }
    if (j > 0) {
      node.neighbors.push(map[i][j - 1]);
    }
    if (j < line.length - 1) {
      node.neighbors.push(map[i][j + 1]);
    }
  });
});

// Compute how many 9 height nodes are reachable from each trailhead
const explore = (node: MapNode): Set<MapNode> => {
  if (node.summits !== null) {
    // Already computed
    return node.summits;
  }
  if (node.value === 9) {
    // End of trail
    node.summits = new Set([node]);
    return node.summits;
  }

  node.summits = new Set();
  for (const neighbor of node.neighbors) {
    if (neighbor.value === node.value + 1) {
      for (const summit of explore(neighbor)) {
        node.summits!.add(summit);
      }
    }
  }
  return node.summits;
};

let sum = 0;
for (const trailhead of [trailheads[0]]) {
  const set = explore(trailhead);
  sum += set.size;
}
console.log(sum);

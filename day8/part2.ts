const input = `............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............`;

const map = input.split("\n").map((line) => line.split(""));
const antinodeMap = map.map((line) => line.map(() => "."));

type Coordinate = [number, number];

const isOutOfBounds = (position: Coordinate) =>
  position[0] < 0 ||
  position[0] >= map.length ||
  position[1] < 0 ||
  position[1] >= map[0].length;

const antennasByName: { [key: string]: Coordinate[] } = {};
for (let i = 0; i < map.length; i++) {
  for (let j = 0; j < map[i].length; j++) {
    const value = map[i][j];
    if (value == "." || value == "#") {
      continue;
    }
    if (!antennasByName[value]) {
      antennasByName[value] = [];
    }
    antennasByName[value].push([i, j]);
  }
}

const createPairs = (antennas: Coordinate[]) => {
  const pairs: Coordinate[][] = [];
  for (let i = 0; i < antennas.length - 1; i++) {
    for (let j = i + 1; j < antennas.length; j++) {
      pairs.push([antennas[i], antennas[j]]);
    }
  }
  return pairs;
};

Object.values(antennasByName).forEach((antennas) => {
  const pairs = createPairs(antennas);
  pairs.forEach((pair) => {
    let leftmost = pair[0][0] < pair[1][0] ? pair[0] : pair[1];
    let rightmost = pair[0][0] >= pair[1][0] ? pair[0] : pair[1];
    const dx = Math.abs(pair[1][0] - pair[0][0]);
    const dy = pair[1][1] - pair[0][1];
    while (!isOutOfBounds(leftmost)) {
      antinodeMap[leftmost[0]][leftmost[1]] = "#";
      leftmost = [leftmost[0] - dx, leftmost[1] - dy];
    }
    while (!isOutOfBounds(rightmost)) {
      antinodeMap[rightmost[0]][rightmost[1]] = "#";
      rightmost = [rightmost[0] + dx, rightmost[1] + dy];
    }
  });
});

console.log(antinodeMap);

let sum = 0;
for (let i = 0; i < antinodeMap.length; i++) {
  for (let j = 0; j < antinodeMap[i].length; j++) {
    if (antinodeMap[i][j] === "#") {
      sum++;
    }
  }
}

console.log(sum);

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
    if (value == ".") {
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
    const leftmost = pair[0][0] < pair[1][0] ? pair[0] : pair[1];
    const rightmost = pair[0][0] >= pair[1][0] ? pair[0] : pair[1];
    const dx = pair[1][0] - pair[0][0];
    const dy = pair[1][1] - pair[0][1];
    const antinode1: Coordinate = [
      leftmost[0] - Math.abs(dx),
      leftmost[1] - dy,
    ];
    const antinode2: Coordinate = [
      rightmost[0] + Math.abs(dx),
      rightmost[1] + dy,
    ];
    if (!isOutOfBounds(antinode1)) {
      antinodeMap[antinode1[0]][antinode1[1]] = "#";
    }
    if (!isOutOfBounds(antinode2)) {
      antinodeMap[antinode2[0]][antinode2[1]] = "#";
    }
  });
});

let sum = 0;
for (let i = 0; i < antinodeMap.length; i++) {
  for (let j = 0; j < antinodeMap[i].length; j++) {
    if (antinodeMap[i][j] === "#") {
      sum++;
    }
  }
}

console.log(sum);

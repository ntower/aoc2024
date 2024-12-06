const input = `....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...`;

const map = input.split("\n").map((row) => row.split(""));

type Coordinate = [number, number];

const up: Coordinate = [-1, 0];
const down: Coordinate = [1, 0];
const left: Coordinate = [0, -1];
const right: Coordinate = [0, 1];

let direction: Coordinate = up;
let position: Coordinate = [0, 0];

for (let i = 0; i < map.length; i++) {
  for (let j = 0; j < map[i].length; j++) {
    if (map[i][j] === "^") {
      position = [i, j];
      break;
    }
  }
}

const move = (position: Coordinate, direction: Coordinate): Coordinate => [
  position[0] + direction[0],
  position[1] + direction[1],
];
const isOutOfBounds = (position: Coordinate) =>
  position[0] < 0 ||
  position[0] >= map.length ||
  position[1] < 0 ||
  position[1] >= map[0].length;
const isWall = (position: Coordinate) => map[position[0]][position[1]] === "#";
const turn = (direction: Coordinate) => {
  if (direction === up) {
    return right;
  } else if (direction === right) {
    return down;
  } else if (direction === down) {
    return left;
  } else {
    return up;
  }
};

while (true) {
  map[position[0]][position[1]] = "X";
  const nextPosition = move(position, direction);
  if (isOutOfBounds(nextPosition)) {
    break;
  } else if (isWall(nextPosition)) {
    direction = turn(direction);
  } else {
    position = nextPosition;
  }
}

let sum = 0;
for (const row of map) {
  for (const cell of row) {
    if (cell === "X") {
      sum++;
    }
  }
}

console.log(sum);

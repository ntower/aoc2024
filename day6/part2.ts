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

let startingPosition: Coordinate = [0, 0];

for (let i = 0; i < map.length; i++) {
  for (let j = 0; j < map[i].length; j++) {
    if (map[i][j] === "^") {
      startingPosition = [i, j];
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

let sum = 0;

const getKey = (position: Coordinate, direction: Coordinate) =>
  `${position[0]},${position[1]},${direction[0]},${direction[1]}`;

const causesLoop = () => {
  let position = startingPosition;
  let direction = up;
  const visited: { [key: string]: boolean } = {};

  while (true) {
    const nextPosition = move(position, direction);
    if (isOutOfBounds(nextPosition)) {
      return false;
    } else if (isWall(nextPosition)) {
      const key = getKey(position, direction);
      if (visited[key]) {
        // Loop!
        return true;
      }
      visited[key] = true;
      direction = turn(direction);
    } else {
      position = nextPosition;
    }
  }
};

for (let i = 0; i < map.length; i++) {
  for (let j = 0; j < map[i].length; j++) {
    let oldSymbol = map[i][j];
    if (oldSymbol === "#") {
      // Already a wall
      continue;
    }

    map[i][j] = "#";

    if (causesLoop()) {
      sum++;
    }

    map[i][j] = oldSymbol;
  }
}

console.log(sum);

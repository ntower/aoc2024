const input = `
....#.....
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
const canMakeLoop = (
  last3TurningPoints: Coordinate[],
  position: Coordinate
) => {
  // BUG: 3 is not enough. Some loops are bigger than a square
  const loopStart = last3TurningPoints[0];
  if (!loopStart) {
    return false;
  }
  const returnedToSameRow = position[0] === loopStart[0];
  const returnedToSameColumn = position[1] === loopStart[1];
  if (returnedToSameRow || returnedToSameColumn) {
    // A loop can be created by putting an obstacle directly in front
    console.log(position);
    return true;
  }
};

let sum = 0;
const last3TurningPoints: Coordinate[] = [];

while (true) {
  map[position[0]][position[1]] = "X";
  const nextPosition = move(position, direction);
  if (isOutOfBounds(nextPosition)) {
    break;
  } else if (isWall(nextPosition)) {
    if (last3TurningPoints.length === 3) {
      last3TurningPoints.shift();
    }
    last3TurningPoints.push(position);
    direction = turn(direction);
  } else {
    if (canMakeLoop(last3TurningPoints, position)) {
      sum++;
    }
    position = nextPosition;
  }
}

console.log(sum);

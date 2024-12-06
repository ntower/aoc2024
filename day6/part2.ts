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
const canMakeLoop = (
  previousTurns: {
    position: Coordinate;
    direction: Coordinate;
  }[],
  position: Coordinate,
  direction: Coordinate
) => {
  // Pretend we turn right now. Will we revisit a turning point?
  const newDirection = turn(direction);
  while (true) {
    const nextPosition = move(position, newDirection);
    if (isOutOfBounds(nextPosition)) {
      return false;
    }
    if (isWall(nextPosition)) {
      if (
        previousTurns.find(
          (turn) =>
            turn.position[0] === position[0] &&
            turn.position[1] == position[1] &&
            turn.direction === newDirection
        )
      ) {
        return true;
      }
    }
    position = nextPosition;
  }
};

let sum = 0;
const previousTurns: {
  position: Coordinate;
  direction: Coordinate;
}[] = [];

while (true) {
  map[position[0]][position[1]] = "X";
  const nextPosition = move(position, direction);
  if (isOutOfBounds(nextPosition)) {
    break;
  } else if (isWall(nextPosition)) {
    previousTurns.push({ position, direction });
    direction = turn(direction);
  } else {
    if (canMakeLoop(previousTurns, position, direction)) {
      sum++;
    }
    position = nextPosition;
  }
}

// Tried submitting 829, too low
console.log(sum);

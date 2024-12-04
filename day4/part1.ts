const input = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX`;

const inputArray: string[][] = input.split("\n").map((line) => line.split(""));

const directions: [xIncrement: number, yIncrement: number][] = [
  [1, 0],
  [0, 1],
  [1, 1],
  [1, -1],
];

let sum = 0;

for (let startingX = 0; startingX < inputArray.length; startingX++) {
  for (let startingY = 0; startingY < inputArray[0].length; startingY++) {
    for (const [xIncrement, yIncrement] of directions) {
      let word = "";
      for (let i = 0; i < 4; i++) {
        const char =
          inputArray[startingX + xIncrement * i]?.[startingY + yIncrement * i];
        if (typeof char === "undefined") {
          break;
        }
        word += char;
      }
      if (word === "XMAS" || word === "SAMX") {
        sum++;
      }
    }
  }
}

console.log(sum);

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

const getWord = ({
  x,
  y,
  xIncrement,
  yIncrement,
}: {
  x: number;
  y: number;
  xIncrement: number;
  yIncrement: number;
}) => {
  let word = "";
  for (let i = 0; i < 3; i++) {
    const char = inputArray[x + xIncrement * i]?.[y + yIncrement * i];
    if (typeof char === "undefined") {
      break;
    }
    word += char;
  }
  return word;
};

let sum = 0;

for (let x = 0; x < inputArray.length; x++) {
  for (let y = 0; y < inputArray[0].length; y++) {
    const word1 = getWord({ x, y, xIncrement: 1, yIncrement: 1 });
    const word2 = getWord({ x, y: y + 2, xIncrement: 1, yIncrement: -1 });
    if (
      (word1 === "MAS" || word1 === "SAM") &&
      (word2 === "MAS" || word2 === "SAM")
    ) {
      sum++;
    }
  }
}

console.log(sum);

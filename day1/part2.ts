const data = `3   4
4   3
2   5
1   3
3   9
3   3`; // insert data here

const lines = data.split("\n");

const left = new Array(lines.length);
const right = new Array(lines.length);
lines.forEach((line, i) => {
  const [a, b] = line.split("   ");
  left[i] = Number(a);
  right[i] = Number(b);
});

const index = {};
right.forEach((value) => {
  index[value] = (index[value] ?? 0) + 1;
});

let similarity = 0;
left.forEach((value) => {
  similarity += value * (index[value] ?? 0);
});

console.log(similarity);

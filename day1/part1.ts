const data = ``; // insert data here

const lines = data.split("\n");

const left = new Array(lines.length);
const right = new Array(lines.length);

lines.forEach((line, i) => {
  const [a, b] = line.split("   ");
  left[i] = Number(a);
  right[i] = Number(b);
});

left.sort((a, b) => a - b);
right.sort((a, b) => a - b);

let sum = 0;
left.forEach((a, i) => {
  const difference = right[i] - a;
  sum += Math.abs(difference);
});
console.log(sum);

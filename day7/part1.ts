const input = `190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20`;

const equations: {
  target: number;
  values: number[];
}[] = input.split("\n").map((line) => {
  const [target, values] = line.split(": ");
  return {
    target: parseInt(target),
    values: values.split(" ").map((n) => parseInt(n)),
  };
});

const operators = [
  (a: number, b: number) => a + b,
  (a: number, b: number) => a * b,
  // concatenate
  (a: number, b: number) => parseInt(`${a}${b}`),
];

const evaluateEquation = (values: number[]): number[] => {
  const [a, b, ...rest] = values;
  if (b === undefined) {
    return [a];
  }

  const results = operators.map((operator) => operator(a, b));
  return results.flatMap((result) => evaluateEquation([result, ...rest]));
};

let sum = 0;

for (const equation of equations) {
  const candidates = evaluateEquation(equation.values);
  if (candidates.includes(equation.target)) {
    sum += equation.target;
  }
}

console.log(sum);

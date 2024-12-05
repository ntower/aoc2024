const input = `47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47`;

const lines = input.split("\n");
// Keep track of the rules. If we see the number on the left hand side, then
//    all the numbers on the right hand side become banned, because they would
//    violate a rule.
const rules: { [key: number]: Set<number> } = {};
let seperatorIndex = -1;
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line === "") {
    // end of rules
    seperatorIndex = i;
    break;
  }
  const [before, after] = line.split("|").map((x) => parseInt(x));
  if (!rules[after]) {
    rules[after] = new Set<number>();
  }
  rules[after].add(before);
}

const updates = lines
  .slice(seperatorIndex + 1)
  .map((line) => line.split(",").map((x) => parseInt(x)));

const isValid = (update: number[]) => {
  let bannedDigits: Set<number>[] = [];
  for (const num of update) {
    if (bannedDigits.some((set) => set.has(num))) {
      return false;
    }

    const newBans = rules[num];
    if (newBans) {
      bannedDigits.push(newBans);
    }
  }
  return true;
};

let sum = 0;
for (const update of updates) {
  if (!isValid(update)) {
    update.sort((a, b) => {
      let aMustComeLast = rules[a]?.has(b);
      let bMustComeLast = rules[b]?.has(a);
      if (aMustComeLast && bMustComeLast) {
        throw new Error(`Mutually exclusive rules ${a} ${b}`);
      } else if (aMustComeLast) {
        return 1;
      } else if (bMustComeLast) {
        return -1;
      } else {
        return 0;
      }
    });
    const midpoint = Math.floor((update.length - 1) / 2);
    sum += update[midpoint];
    continue;
  }
}

console.log(sum);

const input = ``; // insert data here
const reports = input
  .split("\n")
  .map((row) => row.trim().split(" ").map(Number));

const safeReports = reports.filter((report) => {
  const isAscending = report.every((value, i) => {
    const nextValue = report[i + 1];
    if (!nextValue) return true;
    const difference = nextValue - value;
    return difference > 0 && difference <= 3;
  });
  const isDescending = report.every((value, i) => {
    const nextValue = report[i + 1];
    if (!nextValue) return true;
    const difference = value - nextValue;
    return difference > 0 && difference <= 3;
  });
  return isAscending || isDescending;
});

console.log(safeReports.length);

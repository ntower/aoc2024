const input = ``; // insert data here
const reports = input
  .split("\n")
  .map((row) => row.trim().split(" ").map(Number));

const isValidReport = (report, omit: number | null = null) => {
  const isAscending = report.every((value, i) => {
    if (i === omit) return true;

    let nextI = i + 1;
    if (nextI === omit) nextI++;

    const nextValue = report[i + 1];
    if (!nextValue) return true;

    const difference = nextValue - value;
    return difference > 0 && difference <= 3;
  });
  const isDescending = report.every((value, i) => {
    if (i === omit) return true;

    let nextI = i + 1;
    if (nextI === omit) nextI++;

    const nextValue = report[i + 1];
    if (!nextValue) return true;

    const difference = value - nextValue;
    return difference > 0 && difference <= 3;
  });
  return isAscending || isDescending;
};

const safeReports = reports.filter((report) => {
  return (
    isValidReport(report) || report.some((_, i) => isValidReport(report, i))
  );
});

console.log(safeReports.length);

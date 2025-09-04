export const getTotalVotes = (votes) =>
  Object.values(votes).reduce((sum, count) => sum + count, 0);

export const getPercentage = (votes, candidateVotes) => {
  const total = getTotalVotes(votes);
  return total > 0 ? ((candidateVotes / total) * 100).toFixed(1) : 0;
};

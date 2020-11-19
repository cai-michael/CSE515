# return the option that occurs most, or the earlier one if there's a tie
def majority_vote(votes):
	counts = {}
	for k in votes:
		if(not k in counts):
			counts[k] = 0
		counts[k] += 1
	cvalues = list(counts.values())
	return list(counts.keys())[cvalues.index(max(cvalues))]

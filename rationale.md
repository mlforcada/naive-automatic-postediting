
# Learning to postedit: RATIONALE 

These notes show that one can indeed learn post-editing operators from post-edit jobs. The strategy may be applied to any MT system as it uses it as a black box.

## LEARNING 
Learning amounts to harvesting post-editing operators to be applied later.
### Definitions:
 * S : source sentence
 * MT: machine translation system
 * MT(S): machine translation of S
 * PE(MT(S)): post-editing of the machine translation of S, assumed available
 * substr(X) : set of all whole-word substrings of a segment X.

### Process: (can be streamlined) 
 * Compute P(S,MT)={s in substr(S) : MT(s) in substr(MT(S))}, the subset of whole-word substrings of s such that their translation is a whole-word substring of the translation of S. (a length limitation can be applied here)
 * Align MT(S) and PE(MT(S)) (for instance, using edit distance)
 * build the set of all t' in substr(PE(MT(S)) such that t covers a mismatch between MT(S) and PE(MT(S)) (a length limitation can be applied here)
 * for each t' get the corresponding t in MT(S) that are aligned to it (that is, compatible with the word-alignment given by edit distance). There may be more than one.
 * Select those that are in the set MT(P), that is, those that are MT(s) for some s in substr(S).
 * (Of those, one can select operators with have some minimum overlap or some minimum length)
 * Build the set O of postediting operators (s,t') that will be used to post-edit a sentence


## APPLYING 
### Definitions: 
 * S' : new source sentence

### Process (can surely be streamlined) 
 * Build the explanation set P(S',MT)
 * For all s in P(S',MT) such that (s,t') is in O (the last two steps could be streamlined), build the set of target-side operators O' (t,t') to be applied (with t in subset(MT(S')))
 * Apply operators in O' in all possible (compatible, careful with illegal overlaps) ways to MT(S') to get all possible postediting hypotheses T' (this could be done on the fly perhaps)
 * Estimate the quality of each hypothesis T'
 * Produce the best one 

### On quality estimation:
 * Features of post-editing operators or features collected for each T' could be used to build a quality estimator that could then be trained.




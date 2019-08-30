# IdentifyingCodesApproximation

I view the Minimum Identifying Code Set (MICS) problem as a novel variation of the Minimum Hitting Set (MHS) problem. As such, I can utilize the well developed algorithms for the MHS problem, to solve the MICS problem. 

In this repository, I present an approximation algorithm for the MICS problem. This algorithm is based on the well known greedy HS approximation algorithm and has a performance bound of O(log n). 

I have tested my approach on various anonymous undirected Facebook social networks. Even with the O(log n) performance bound, on this dataset, the approximation algorithm performed pretty well. It provided near optimal solution cardinalities in a fraction of the computation time (when compared with an Integer Linear Program).  

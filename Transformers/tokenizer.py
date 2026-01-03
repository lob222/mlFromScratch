# My implementation of BPE (Byte-Pair Encoding) as detailed in original Paper
# Resource used to learn about BPE: https://www.youtube.com/watch?v=tOMjTCO0htA
import heapq

class BPEtokenizer:
    def __init__(self, max_tokens = 37000):
        self.max_tokens = max_tokens

    def encode(self, corpus):
        token_list = list("".join(corpus))
        vocab = list(set(token_list))

        pq = []

        pair_count = dict()

        # 1. Intial pairs count
        for i in range(len(token_list) - 1):
            tk_l = token_list[i]
            tk_r = token_list[i + 1]

            pair = tuple([tk_l, tk_r])
            if pair in pair_count:
                pair_count[pair] = pair_count[pair] - 1
            else:
                pair_count[pair] = -1
        
        for p in pair_count:
            heapq.heappush(pq, (-pair_count[p], p)) # (-ve count, pair_tuple)


        
        while len(vocab) < 3.7e4:
            
            neg_count, most_pair = heapq.heappop(pq) # takes most negative element ("lowest prioirty" & highest pair count)
            most_l, most_r = most_pair
            vocab.append("".join(most_pair))

            new_pair_idxs = []

            j = 0
            while j < len(token_list) - 1:
                tk_l = token_list[j]
                tk_r = token_list[j + 1]
                if tk_l == most_l and tk_r == most_r:
                    # replace all instances of tk_l and tk_r by concat(tk_l, tk_r), ie. concatenate and remove
                    token_list[j] = token_list[j] + token_list[j + 1]
                    token_list.pop(j+1)
                    new_pair_idxs.append(j)
                j += 1
                
            new_pair_count = dict()

            # Add the new pairs to the pair list
            for idx in new_pair_idxs:
                if idx == 0:
                    pairs = [tuple([token_list[idx], token_list[idx + 1]])]
                elif idx == len(token_list) - 1:
                    pairs = [tuple([token_list[idx - 1], token_list[idx]])]
                else:
                    pairs = [tuple([token_list[idx - 1], token_list[idx]]), tuple([token_list[idx], token_list[idx + 1]])]

                for pair in pairs:
                    if pair in new_pair_count:
                        new_pair_count[pair] = new_pair_count[pair] - 1
                    else:
                        new_pair_count[pair] = -1

            for p in new_pair_count:
                heapq.heappush(pq, (-new_pair_count[p], p)) # (-ve count, pair_tuple)
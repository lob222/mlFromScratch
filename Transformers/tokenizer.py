# My implementation of BPE (Byte-Pair Encoding) as detailed in original Paper
# Resource used to learn about BPE: https://www.youtube.com/watch?v=tOMjTCO0htA

class Node: 
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None



class BPEtokenizer:
    def __init__(self, max_tokens = 37000):
        self.max_tokens = max_tokens

    def create_llist(self, sentence):

        nodes = []
        for tk in sentence:
            nodes.append(Node(data = tk))

        for i in range(len(nodes)):
            node_curr = nodes[i]
            if i > 0 :
                node_curr.prev = nodes[i - 1]
            if i < len(nodes) - 1:
                node_curr.next = nodes[i + 1]

        return nodes[0]


    def encode(self, corpus):
        vocab = list(set(''.join(corpus)))

        llist_corpus = [self.create_llist(s) for s in corpus]

        pair_count = dict()

        for ll_sentence in llist_corpus:
            curr_node = ll_sentence
            while curr_node is not None and curr_node.next is not None:

                next_node = curr_node.next

                tk_l = curr_node.data
                tk_r = next_node.data

                tk_pair = tuple([tk_l, tk_r])
                if tk_pair in pair_count:
                    pair_count[tk_pair] = pair_count[tk_pair] + 1
                else:
                    pair_count[tk_pair] = 1
                curr_node = curr_node.next


        while len(vocab) < 3.7e4:
            max_tk_l, max_tk_r = max(pair_count.items(), key=lambda item: item[1])[0]
            tk_new = max_tk_l + max_tk_r
            vocab.append(tk_new)
            del pair_count[(max_tk_l, max_tk_r)]

            for ll_sentence in llist_corpus:
                curr_node = ll_sentence
                while curr_node is not None and curr_node.next is not None:
                    left_node = curr_node
                    right_node = curr_node.next

                    tk_l = left_node.data
                    tk_r = right_node.data

                    if tk_l == max_tk_l and tk_r == max_tk_r:
                        new_node = Node(tk_l + tk_r)
                        new_node.prev = left_node.prev
                        new_node.next = right_node.next

                        left_node.prev.next = new_node
                        right_node.next.prev = new_node

                    # TODO: finish implementation


                    tk_pair = tuple([tk_l, tk_r])
                    if tk_pair in pair_count:
                        pair_count[tk_pair] = pair_count[tk_pair] + 1
                    else:
                        pair_count[tk_pair] = 1
                    curr_node = curr_node.next


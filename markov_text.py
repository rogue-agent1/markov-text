#!/usr/bin/env python3
"""markov_text - Markov chain text generator with configurable n-gram order."""
import sys, random
from collections import defaultdict

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.chain = defaultdict(list)
        self.starts = []
    def train(self, text):
        words = text.split()
        if len(words) <= self.order: return
        self.starts.append(tuple(words[:self.order]))
        for i in range(len(words) - self.order):
            key = tuple(words[i:i+self.order])
            self.chain[key].append(words[i+self.order])
    def generate(self, max_words=50, seed=None):
        if seed is not None: random.seed(seed)
        if not self.starts: return ""
        state = random.choice(self.starts)
        result = list(state)
        for _ in range(max_words - self.order):
            if state not in self.chain: break
            nxt = random.choice(self.chain[state])
            result.append(nxt)
            state = tuple(result[-self.order:])
        return " ".join(result)

def test():
    mc = MarkovChain(order=1)
    mc.train("the cat sat on the mat the cat ate the rat")
    random.seed(42)
    text = mc.generate(20, seed=42)
    assert len(text.split()) >= 2
    assert text.split()[0] in ["the", "cat", "sat", "on", "mat", "ate", "rat"]
    mc2 = MarkovChain(order=2)
    mc2.train("a b c d e a b c d e a b c f g")
    assert ("a", "b") in mc2.chain
    nexts = mc2.chain[("a", "b")]
    assert "c" in nexts
    print("markov_text: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: markov_text.py --test")

import torch
import torch.nn as nn
import torch.nn.functional as F

class Embedding(nn.Module):
    def __init__(self, max_len, vocab_size, d_model)-> None:
        super().__init__()
        self.max_len = max_len # context size
        self.d_model = d_model # embedding size
        self.pos = self._positional()

        self.embeddings = nn.Linear(vocab_size, d_model, bias=False)

    def forward(self, x):
        # Learn embeddings from one-hot representation to latent space of size d_model        
        y = self.embeddings(x)
        # Incorporate positional embeddings for information about position of token in sequence
        y = y + self.pos
        return y

    def _positional(self):

        # positional embedding of shape [max_len, d_model]
        feature_idx = torch.arange(self.d_model).repeat(self.max_len).view(self.max_len, self.d_model)
        freq_idx = torch.arange(int(self.d_model / 2)).repeat_interleave(2).repeat(self.max_len).view(self.max_len, self.d_model) * 2
        pos_idx = torch.arange(self.max_len).repeat_interleave(self.d_model).view(self.max_len, self.d_model)

        inner = pos_idx/ 1e4 ** (freq_idx / self.d_model)

        enc = torch.where(feature_idx % 2 == 0, 
                            torch.sin(inner),
                            torch.cos(inner) 
                          )
        return enc

if __name__ == "__main__":
    e = Embedding(5, 100, 8)
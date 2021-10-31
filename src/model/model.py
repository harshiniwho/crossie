import torch
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel

from config import *

tokenizer = GPT2Tokenizer.from_pretrained(MODEL_TYPE)
model = GPT2LMHeadModel.from_pretrained(MODEL_TYPE)


def fetch_next_words(text, k):
    tokens = tokenizer.encode(text)
    tokens_tensor = torch.tensor([tokens])
    model.eval()

    tokens_tensor = tokens_tensor.to(DEVICE)
    model.to(DEVICE)

    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    probs = predictions[0, -1, :]

    first_next_word = []
    for i in probs.topk(k)[1]:
        tokenizer.decode(i.item()).strip()
        first_next_word.append(tokenizer.decode(i.item()).strip())
    return first_next_word

import torch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_TYPE = "gpt2"

END_PUNCTUATION = { 0, 13, 11, 26, 30 }
NUMBER_OF_CLUES = 10

DATA_DIR = "data/"

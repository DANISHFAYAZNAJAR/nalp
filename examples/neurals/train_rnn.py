import nalp.stream.loader as l
import nalp.stream.preprocess as p
from nalp.datasets.one_hot import OneHot
from nalp.neurals.rnn import RNN

# Loading a text
sentences = l.load_txt('data/text/chapter1_harry.txt')

# Defining a predition input
start_text = 'Mr. Dursley'

# Creates a pre-processing pipeline
pipe = p.pipeline(
    p.tokenize_to_char
)

# Applying pre-processing pipeline to sentences and start token
tokens = pipe(sentences)
start_token = pipe(start_text)

# Creating a OneHot dataset
d = OneHot(tokens, max_length=10)

# Defining a neural network based on vanilla RNN
rnn = RNN(vocab_size=d.vocab_size, hidden_size=64, learning_rate=0.001)

# Training the network
rnn.train(dataset=d, batch_size=128, epochs=100)

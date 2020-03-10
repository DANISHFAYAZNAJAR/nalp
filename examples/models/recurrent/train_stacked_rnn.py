import tensorflow as tf

from nalp.corpus.text import TextCorpus
from nalp.datasets.language_modelling import LanguageModellingDataset
from nalp.encoders.integer import IntegerEncoder
from nalp.models.recurrent.stacked_rnn import StackedRNN

# Creating a character TextCorpus from file
corpus = TextCorpus(from_file='data/text/chapter1_harry.txt', type='char')

# Creating an IntegerEncoder
encoder = IntegerEncoder()

# Learns the encoding based on the TextCorpus dictionary and reverse dictionary
encoder.learn(corpus.vocab_index, corpus.index_vocab)

# Applies the encoding on new data
encoded_tokens = encoder.encode(corpus.tokens)

# Creating Language Modelling Dataset
dataset = LanguageModellingDataset(encoded_tokens, max_length=10, batch_size=64)

# Creating the StackedRNN
rnn = StackedRNN(vocab_size=corpus.vocab_size,
                 embedding_size=256, hidden_size=[128, 256, 512])

# As NALP's StackedRNNs are stateful, we need to build it with a fixed batch size
rnn.build((64, None))

# Compiling the StackedRNN
rnn.compile(optimizer=tf.optimizers.Adam(learning_rate=0.001),
            loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=[tf.metrics.SparseCategoricalAccuracy(name='accuracy')])

# Fitting the StackedRNN
rnn.fit(dataset.batches, epochs=100)

# Evaluating the StackedRNN
# rnn.evaluate(dataset.batches)

# Saving StackedRNN weights
rnn.save_weights('trained/stacked_rnn', save_format='tf')

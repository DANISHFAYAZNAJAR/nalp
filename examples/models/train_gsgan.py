import tensorflow as tf

from nalp.corpus.text import TextCorpus
from nalp.datasets.language_modeling import LanguageModelingDataset
from nalp.encoders.integer import IntegerEncoder
from nalp.models.gsgan import GSGAN

# Creating a character TextCorpus from file
corpus = TextCorpus(from_file='data/text/chapter1_harry.txt', type='char')

# Creating an IntegerEncoder
encoder = IntegerEncoder()

# Learns the encoding based on the TextCorpus dictionary and reverse dictionary
encoder.learn(corpus.vocab_index, corpus.index_vocab)

# Applies the encoding on new data
encoded_tokens = encoder.encode(corpus.tokens)

# Creating Language Modeling Dataset
dataset = LanguageModelingDataset(encoded_tokens, max_length=10, batch_size=64)

# Creating the GSGAN
gsgan = GSGAN(encoder=encoder, vocab_size=corpus.vocab_size,
              max_length=10, embedding_size=256, hidden_size=512, tau=5)

# Compiling the GSGAN
gsgan.compile(pre_optimizer=tf.optimizers.Adam(learning_rate=0.01),
              g_optimizer=tf.optimizers.Adam(learning_rate=0.001),
              d_optimizer=tf.optimizers.Adam(learning_rate=0.001))

# Pre-fitting the GSGAN
gsgan.pre_fit(dataset.batches, epochs=100)

# Fitting the GSGAN
gsgan.fit(dataset.batches, epochs=100)

# Saving GSGAN weights
gsgan.save_weights('trained/gsgan', save_format='tf')
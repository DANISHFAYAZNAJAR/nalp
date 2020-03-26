from tensorflow.keras import layers

import nalp.utils.logging as l
from nalp.core.model import Discriminator

logger = l.get_logger(__name__)


class LSTMDiscriminator(Discriminator):
    """A LSTMDiscriminator class is the one in charge of a discriminative Long Short-Term Memory implementation.

    References:
        S. Hochreiter, Jürgen Schmidhuber. Long short-term memory. Neural computation 9.8 (1997).

    """

    def __init__(self, encoder=None, vocab_size=1, embedding_size=32, hidden_size=64):
        """Initialization method.

        Args:
            encoder (IntegerEncoder): An index to vocabulary encoder.
            vocab_size (int): The size of the vocabulary.
            embedding_size (int): The size of the embedding layer.
            hidden_size (int): The amount of hidden neurons.

        """

        logger.info('Overriding class: Discriminator -> LSTMDiscriminator.')

        # Overrides its parent class with any custom arguments if needed
        super(LSTMDiscriminator, self).__init__(name='D_lstm')

        # Creates a property for holding the used encoder
        self.encoder = encoder

        # Creates an embedding layer
        self.embedding = layers.Dense(embedding_size, name='embedding')

        # Creates a LSTM cell
        self.cell = layers.LSTMCell(hidden_size, name='lstm_cell')

        # Creates the RNN loop itself
        self.rnn = layers.RNN(self.cell, name='rnn_layer',
                              stateful=True)

        # And finally, defining the output layer
        self.out = layers.Dense(1, name='out')

    def call(self, x):
        """Method that holds vital information whenever this class is called.

        Args:
            x (tf.Tensor): A tensorflow's tensor holding input data.

        Returns:
            The same tensor after passing through each defined layer.

        """

        # Firstly, we apply the embedding layer
        x = self.embedding(x)

        # We need to apply the input into the first recurrent layer
        x = self.rnn(x)

        # The input also suffers a linear combination to output correct shape
        x = self.out(x)

        return x

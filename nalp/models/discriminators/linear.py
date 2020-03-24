import tensorflow as tf
from tensorflow.keras import layers

import nalp.utils.logging as l
from nalp.core.model import Discriminator

logger = l.get_logger(__name__)


class LinearDiscriminator(Discriminator):
    """A LinearDiscriminator class stands for the linear discriminative part of a Generative Adversarial Network.

    """

    def __init__(self, n_samplings, alpha):
        """Initialization method.

        Args:
            n_samplings (int): Number of downsamplings to perform.
            alpha (float): LeakyReLU activation threshold.

        """

        logger.info('Overriding class: Discriminator -> LinearDiscriminator.')

        # Overrides its parent class with any custom arguments if needed
        super(LinearDiscriminator, self).__init__(name='D_linear')

        # Defining a property for the LeakyReLU activation
        self.alpha = alpha

        # Defining a list for holding the linear layers
        self.linear = [layers.Dense(
            128 * i, name=f'linear_{i}') for i in range(n_samplings, 0, -1)]

        # Defining the output as a logit unit that decides whether input is real or fake
        self.out = layers.Dense(1, name='out')

    def call(self, x, training=True):
        """Method that holds vital information whenever this class is called.

        Args:
            x (tf.Tensor): A tensorflow's tensor holding input data.
            training (bool): Whether architecture is under training or not.

        Returns:
            The same tensor after passing through each defined layer.

        """

        # For every possible linear layer
        for l in self.linear:
            # Applies the layer with a LeakyReLU activation
            x = tf.nn.leaky_relu(l(x), self.alpha)

        # Passing down the output layer
        x = self.out(x)

        return x
# class for forming input images 

# imports required libraries
import tensorflow as tf

# defines the Forming class for the forming of input images
class Tailing:

    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, size: int):
        self.size = size

    # module for the forming of input images
    def tailing(self, image: tf.Tensor)-> tf.Tensor:
        '''forms an image into a specified size by extracting patches from the image and returns the formed image
        Args:
            image: the image to be formed
        Returns:
            the formed image
        '''

        # extracts patches from the image
        tiles=tf.image.extract_patches(
            images=tf.expand_dims(image, axis=0),
            sizes=[1, self.size, self.size, 1],
            strides=[1, self.size, self.size, 1],
            rates=[1, 1, 1, 1],
            padding='VALID'
        )

        # squeezes the patches to remove the extra dimension
        tiles=tf.squeeze(tiles, axis=0)

        # reshapes the patches to the specified size
        tiles=tf.reshape(tiles, [-1, self.size, self.size, 3])

        # returns the formed image
        return tiles
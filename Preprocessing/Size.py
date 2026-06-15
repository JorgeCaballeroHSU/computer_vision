# class for resizing images to a specified size

# imports required libraries
import tensorflow as tf

# defines the Size class
class Size:
    def __init__(self, size: int):
        self.size = size

    # module for resizing images to a specified size
    def resize(self, image: tf.Tensor)-> tf.Tensor:
        '''resizes an image to a specified size and returns the resized image
        Args:
            image: the image to be resized
        Returns:
            the resized image
        '''
        return tf.image.resize(image, [self.size, self.size])
    

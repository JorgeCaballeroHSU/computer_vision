# classes for the generation of augmented data for the training of the model

# imports required libraries
import tensorflow as tf

# defines the flipping class for the flipping of images
class Flipping:

    #space for the properties of the class

    # module for the initialization of the class
    def __init__(self, flipType: str):
        self.flipType = flipType

    # module for the flipping of images
    def flip(self, image: tf.Tensor)-> tf.Tensor:
        '''flips an image according to the specified flip type and returns the flipped image
        Args:
            image: the image to be flipped
        Returns:
            the flipped image
        '''
        if self.flipType == 'horizontal':
            return tf.image.flip_left_right(image)
        elif self.flipType == 'vertical':
            return tf.image.flip_up_down(image)
        else:
            raise ValueError('Invalid flip type. Must be "horizontal" or "vertical".')
        
# defines the ColorDistortion class for the distortion of the colors of images
class ColorDistortion:

    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, brightness: float, contrast: float, saturation: float, hue: float):
        self.brightness = brightness
        self.contrast = contrast
        self.saturation = saturation
        self.hue = hue

    # module for the distortion of the colors of images
    def distortColors(self, image: tf.Tensor)-> tf.Tensor:
        '''distorts the colors of an image according to the specified brightness, contrast, saturation, and hue and returns the distorted image
        Args:
            image: the image to be distorted
        Returns:
            the distorted image
        '''
        image = tf.image.random_brightness(image, max_delta=self.brightness)
        image = tf.image.random_contrast(image, lower=1-self.contrast, upper=1+self.contrast)
        image = tf.image.random_saturation(image, lower=1-self.saturation, upper=1+self.saturation)
        image = tf.image.random_hue(image, max_delta=self.hue)
        return image
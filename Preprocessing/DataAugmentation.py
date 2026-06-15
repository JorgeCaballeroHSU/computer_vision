# classes for the generation of augmented data for the training of the model

# imports required libraries
import tensorflow as tf
import random

# defines the flipping class for the flipping of images
class Flipping:

    #space for the properties of the class

    # module for the initialization of the class
    def __init__(self, flipType: str | None=None) ->None:

        # defines the content of the property flipType, None by default
        self.flipType = flipType

        # returns None
        return None

    # module for the flipping of images
    def flip(self, image: tf.Tensor)-> tf.Tensor:
        '''flips an image according to the specified flip type and returns the flipped image
        Args:
            image: the image to be flipped
        Returns:
            the flipped image
        '''
        # applies horizontal flip
        if self.flipType == 'horizontal':

            # changes flipType back to None
            self.flipType=None

            # returns results
            return tf.image.flip_left_right(image)
        
        # applies vertical flip
        elif self.flipType == 'vertical':

            # changes flipType back to None
            self.flipType=None

            # returns results
            return tf.image.flip_up_down(image)
        
        # applies a random flip
        else:

            # choises randonly the type of flip
            self.flipType=random.choice(['horizontal','vertical'])

            # calls itself again and return results
            return self.flip(image=image)
        
# defines the ColorDistortion class for the distortion of the colors of images
class ColorDistortion:

    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, brightness: float |None=0.1, contrast: float|None=0.5, 
                 saturation: float|None=0.25, hue: float|None=0.1)->None:
        
        # defines the value of the properties of this class
        self.brightness = brightness
        self.contrast = contrast
        self.saturation = saturation
        self.hue = hue

        # returns None
        return None

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

        # returns results
        return image
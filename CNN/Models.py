# this files contains the models for the CNN

# imports required libraries
import tensorflow as tf
import keras

# defines the convolutional neural network AlexNet model
class AlexNet(keras.Model):
    
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(AlexNet, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.conv1 = keras.layers.Conv2D(filters=96, kernel_size=(11, 11), strides=4, activation='relu')
        self.pool1 = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2)
        self.conv2 = keras.layers.Conv2D(filters=256, kernel_size=(5, 5), strides=1, activation='relu', padding='same')
        self.pool2 = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2)
        self.conv3 = keras.layers.Conv2D(filters=384, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv4 = keras.layers.Conv2D(filters=384, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv5 = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.pool5 = keras.layers.MaxPooling2D(pool_size=(3, 3), strides=2)
        self.flatten = keras.layers.Flatten()
        self.fc6 = keras.layers.Dense(units=4096, activation='relu')
        self.dropout6 = keras.layers.Dropout(rate=0.5)
        self.fc7 = keras.layers.Dense(units=4096, activation='relu')
        self.dropout7 = keras.layers.Dropout(rate=0.5)
        self.fc8 = keras.layers.Dense(units=self.numClasses, activation='softmax')


    #module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        ''' 
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])   

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.conv1(inputs)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.pool5(x)
        x = self.flatten(x)
        x = self.fc6(x)
        x = self.dropout6(x)
        x = self.fc7(x)
        x = self.dropout7(x)
        x = self.fc8(x)
        return x   

# defines the convolutional neural network VGG19 model
class VGG19(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(VGG19, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.conv1_1 = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv1_2 = keras.layers.Conv2D(filters=64, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.pool1 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)
        self.conv2_1 = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv2_2 = keras.layers.Conv2D(filters=128, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.pool2 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)
        self.conv3_1 = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv3_2 = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv3_3 = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv3_4 = keras.layers.Conv2D(filters=256, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.pool3 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)
        self.conv4_1 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv4_2 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv4_3 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv4_4 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.pool4 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)
        self.conv5_1 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv5_2 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv5_3 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.conv5_4 = keras.layers.Conv2D(filters=512, kernel_size=(3, 3), strides=1, activation='relu', padding='same')
        self.pool5 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)
        self.flatten = keras.layers.Flatten()
        self.fc6 = keras.layers.Dense(units=4096, activation='relu')
        self.dropout6 = keras.layers.Dropout(rate=0.5)
        self.fc7 = keras.layers.Dense(units=4096, activation='relu')
        self.dropout7 = keras.layers.Dropout(rate=0.5)
        self.fc8 = keras.layers.Dense(units=self.numClasses, activation='softmax')  

    #module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:  
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.conv1_1(inputs)
        x = self.conv1_2(x)
        x = self.pool1(x)
        x = self.conv2_1(x)
        x = self.conv2_2(x)
        x = self.pool2(x)
        x = self.conv3_1(x)
        x = self.conv3_2(x)
        x = self.conv3_3(x)
        x = self.conv3_4(x)
        x = self.pool3(x)
        x = self.conv4_1(x)
        x = self.conv4_2(x)
        x = self.conv4_3(x)
        x = self.conv4_4(x)
        x = self.pool4(x)
        x = self.conv5_1(x)
        x = self.conv5_2(x)
        x = self.conv5_3(x)
        x = self.conv5_4(x)
        x = self.pool5(x)
        x = self.flatten(x)
        x = self.fc6(x)
        x = self.dropout6(x)
        x = self.fc7(x)
        x = self.dropout7(x)
        x = self.fc8(x)
        return x
    
# defines the convolutional neural network InceptionV3 model
class InceptionV3(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(InceptionV3, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.inceptionV3 = keras.applications.InceptionV3(include_top=False, weights='imagenet', input_shape=(299, 299, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.inceptionV3(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# defines the convolutional neural network squeeznet model
class SqueezeNet(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(SqueezeNet, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.squeezeNet = keras.applications.SqueezeNet(include_top=False, weights='imagenet', input_shape=(227, 227, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.squeezeNet(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x
    
# defines the convolutional neural network ResNet50 model
class ResNet50(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(ResNet50, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.resNet50 = keras.applications.ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.resNet50(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x
    
# defines the convolutional neural network DenseNet121 model
class DenseNet121(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(DenseNet121, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.denseNet121 = keras.applications.DenseNet121(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.denseNet121(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# defines the convolutional neural network Xception model  
class Xception(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(Xception, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.xception = keras.applications.Xception(include_top=False, weights='imagenet', input_shape=(299, 299, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.xception(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# defines the convolutional neural network NASNEet model
class NASNet(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(NASNet, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.nasNet = keras.applications.NASNetMobile(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.nasNet(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x
    
# defines the convolutional neural network MobileNetV2 model
class MobileNetV2(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(MobileNetV2, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.mobileNetV2 = keras.applications.MobileNetV2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.mobileNetV2(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x
    
# defines the convolutional neural network EfficientNetB0 model
class EfficientNetB0(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(EfficientNetB0, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.efficientNetB0 = keras.applications.EfficientNetB0(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.efficientNetB0(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# defines the convolutional neural network YoloV3 model
class YoloV3(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(YoloV3, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.yoloV3 = keras.applications.YOLOV3(include_top=False, weights='imagenet', input_shape=(416, 416, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.yoloV3(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# defines the convolutional neural network RetinaNet model
class RetinaNet(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(RetinaNet, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.retinaNet = keras.applications.RetinaNet(include_top=False, weights='imagenet', input_shape=(512, 512, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.retinaNet(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# defines the convolutional neural network Unet model
class Unet(keras.Model):
    # space for the properties of the class

    # module for the initialization of the class
    def __init__(self, numClasses: int):
        super(Unet, self).__init__()

        # initializes the properties of the class
        self.numClasses = numClasses

        # defines the layers of the model
        self.unet = keras.applications.Unet(include_top=False, weights='imagenet', input_shape=(256, 256, 3))
        self.flatten = keras.layers.Flatten()
        self.fc = keras.layers.Dense(units=self.numClasses, activation='softmax')

    # module for training the model
    def trainModel(self, trainDataset: tf.data.Dataset, valDataset: tf.data.Dataset, epochs: int, checkpoint: tf.keras.callbacks.ModelCheckpoint)-> None:
        '''trains the model on the training dataset and validates it on the validation dataset for a specified number of epochs and saves the best model using the specified checkpoint
        Args:
            trainDataset: the training dataset to be used for training the model
            valDataset: the validation dataset to be used for validating the model during training
            epochs: the number of epochs to train the model for
            checkpoint: the checkpoint to be used for saving the best model during training
        Returns:
            None
        '''
        # compiles the model with the Adam optimizer, categorical cross-entropy loss, and accuracy metric
        self.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # trains the model on the training dataset and validates it on the validation dataset for the specified number of epochs and saves the best model using the specified checkpoint
        self.fit(trainDataset, validation_data=valDataset, epochs=epochs, callbacks=[checkpoint])

    # module for the forward pass of the model
    def call(self, inputs: tf.Tensor)-> tf.Tensor:
        '''performs a forward pass through the model and returns the output tensor
        Args:
            inputs: the input tensor to be passed through the model
        Returns:
            the output tensor of the model after performing a forward pass
        '''
        x = self.unet(inputs)
        x = self.flatten(x)
        x = self.fc(x)
        return x
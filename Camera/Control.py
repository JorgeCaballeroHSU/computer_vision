# this file contains the class Control, which is used to have a list of commands that can be sent trough the socket to control the camera

# defines the class Control, which is used to have a list of commands that can be sent to the camera to control it
class Control:

    # properties of the class Control
    _commands = ['focus', 'zoom', 'aperture', 'shutter_speed', 'iso', 'white_balance', 'exposure_compensation', 'flash_mode', 'drive_mode', 'metering_mode', 'picture_style']

    # constructor of the class Control, it initializes the list of commands
    def __init__(self)->None:

        pass

    # method to get the list of commands
    def getCommands(self)->list:
        '''returns the list of commands that can be sent to the camera to control it

        Returns:
            list: the list of commands that can be sent to the camera to control it
        '''

        # returns the list of commands
        return self._commands
    

    # method to define the focus position of the camera
    def focus(self, position: int)->tuple:
        '''defines the focus position of the camera
        Args:
            position (int): the focus position to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the position to set the camera to
        '''

        # returns None
        return self._commands[0], position
    
    # method to define the zoom level of the camera
    def zoom(self, level: int)->tuple:
        '''defines the zoom level of the camera
        Args:
            level (int): the zoom level to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the zoom level to set the camera to
        '''

        # returns None
        return self._commands[1], level
    
    # method to define the aperture of the camera
    def aperture(self, value: float)->tuple:    
        '''defines the aperture of the camera
        Args:
            value (float): the aperture value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the aperture value to set the camera to
        '''

        # returns None
        return self._commands[2], value
    
    # method to define the shutter speed of the camera
    def shutter_speed(self, value: float)->tuple:
        '''defines the shutter speed of the camera
        Args:
            value (float): the shutter speed value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the shutter speed value to set the camera to
        '''

        # returns None
        return self._commands[3], value
    
    # method to define the ISO of the camera
    def iso(self, value: int)->tuple:
        '''defines the ISO of the camera
        Args:
            value (int): the ISO value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the ISO value to set the camera to
        '''

        # returns None
        return self._commands[4], value
    
    # method to define the white balance of the camera
    def white_balance(self, value: str)->tuple:
        '''defines the white balance of the camera
        Args:
            value (str): the white balance value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the white balance value to set the camera to
        '''

        # returns None
        return self._commands[5], value
    
    # method to define the exposure compensation of the camera
    def exposure_compensation(self, value: float)->tuple:
        '''defines the exposure compensation of the camera
        Args:
            value (float): the exposure compensation value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the exposure compensation value to set the camera to
        '''

        # returns None
        return self._commands[6], value
    
    # method to define the flash mode of the camera
    def flash_mode(self, value: str)->tuple:
        '''defines the flash mode of the camera
        Args:
            value (str): the flash mode value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the flash mode value to set the camera to
        '''

        # returns None
        return self._commands[7], value
    
    # method to define the drive mode of the camera
    def drive_mode(self, value: str)->tuple:
        '''defines the drive mode of the camera
        Args:
            value (str): the drive mode value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the drive mode value to set the camera to
        '''

        # returns None
        return self._commands[8], value
    
    # method to define the metering mode of the camera
    def metering_mode(self, value: str)->tuple:
        '''defines the metering mode of the camera
        Args:
            value (str): the metering mode value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the metering mode value to set the camera to
        '''

        # returns None
        return self._commands[9], value
    
    # method to define the picture style of the camera
    def picture_style(self, value: str)->tuple:
        '''defines the picture style of the camera
        Args:
            value (str): the picture style value to set the camera to
        
        Returns:
            tuple: the command to send to the camera and the picture style value to set the camera to
        '''

        # returns None
        return self._commands[10], value
    
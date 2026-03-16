# this class is used to change the type of path from windows to wsl and vice versa

# import required libraries
import subprocess

class ChangePath:

    '''This class is used to change the type of path from windows to wsl and vice versa. It is used to change the type of path from windows to wsl and vice versa.'''

    # changes the type of path from windows to wsl
    def changePathWindowsToWsl(self, path: str) ->str:

        '''This method changes the type of path from windows to wsl. It is used to change the type of path from windows to wsl and vice versa.'''

        # code to change the type of path from windows to wsl goes here
        result = subprocess.run(["wsl", "wslpath", "-u", path], capture_output=True, text=True)

        # returns the path in wsl format
        return result.stdout.strip()

    # changes the type of path from wsl to windows
    def changePathWslToWindows(self, path: str) ->str:

        '''This method changes the type of path from wsl to windows. It is used to change the type of path from windows to wsl and vice versa.'''

        # code to change the type of path from wsl to windows goes here
        result = subprocess.run(["wsl", "wslpath", "-w", path], capture_output=True, text=True)

        # returns the path in windows format
        return result.stdout.strip()

    # checks if the path is in windows format or wsl format
    def checkPathFormat(self, path: str) ->str:

        '''This method checks if the path is in windows format or wsl format. It is used to check if the path is in windows format or wsl format.'''

        # code to check if the path is in windows format or wsl format goes here
        if path.startswith("/mnt/"):
            return "wsl"
        else:
            return "windows"
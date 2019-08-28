class Error(Exception):
    '''
        Base class for exceptions.
    '''
    pass

class ConnectionError(Error):

    def __init__(self):
        self.message = ": device is not connected to any network"

    def throwError(self):
        return self.__class__.__name__ + self.message


raise ConnectionError
# except Error as inst:
#     print (inst.throwError())
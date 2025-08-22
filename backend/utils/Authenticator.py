class Authenticator:
    _is_authenticated = False
    _key = "default_key"
    _default_key = "default_key"

    def __init__(self):
        if self._key == self._default_key:
            print ("WARNING: default key is used")

    def Authenticate(self, key):
        if (self._key == key):
            self._is_authenticated = True
        else:
            self._is_authenticated = False

    def IsAuthenticated(self):
        return(self._is_authenticated)
    

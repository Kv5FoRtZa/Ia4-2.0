class Level:
    # class variables (static variables in java)
    type = "level" # am scris si eu ceva aici sa fie

    # class constructor (instance variables)
        # self.instance (public -- can be accesed outisde the class)
        # self._instance (private -- cannot be accesed outside the class - unless getter)

    # state : locked / unlocked
    # win_status : 0 (nu a castigat) / 1 (a castigat)
    # map : harta nivelului
    def __init__(self, name, state, win_status, game_map_obj):
        self._name = name
        self._state = state
        self._win_status = win_status
        self._map = game_map_obj

    def getName(self):
        return self._name

    def getState(self):
        return self._state
    
    def setState(self, value):
        self._state = value

    def getWinStatus(self):
        return self._win_status

    def setWinStatus(self, value):
        self._win_status = value

    def getMap(self):
        return self._map
    
    # map will be it's own class
    def setMap(self, value):
        self._map = value
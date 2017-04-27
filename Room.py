class Room:
    # ID counter used to assign IDs automatically
    nextRoomId = 0

    # Initializes room data and assign ID to room
    def __init__(self, name, lab, numberOfSeats):
        global nextRoomId
        self.id = nextRoomId
        self.name = name
        if lab == 'true':
            self.lab = True
        else:
            self.lab = False
        print("laaab: ", name, lab, self.lab, self.id)
        self.numberOfSeats = numberOfSeats
        nextRoomId = nextRoomId + 1

    # Returns room ID
    def GetId(self):
        return self.id

    # Returns room name
    def GetName(self):
        return self.name

    # Returns TRUE if room has computers otherwise it returns FALSE
    def IsLab(self):
        return self.lab

    # Returns number of seats in room
    def GetNumberOfSeats(self):
        return int(self.numberOfSeats)

    # Restarts ID assigments
    @staticmethod
    def RestartIDs():
        global nextRoomId
        nextRoomId = 0

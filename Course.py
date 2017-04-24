class Course:
    # Initializes course
    def __init__(self, id, name):
        self.id = id
        self.name = name

    # Returns course ID
    def GetId(self):
        return self.id

    # Returns course name
    def GetName(self):
        return self.name

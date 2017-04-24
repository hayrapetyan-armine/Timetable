class Professor:
    # Initializes professor data
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.courseClasses = []

    # Returns professor's ID
    def GetId(self):
        return self.id

    # Returns professor's name
    def GetName(self):
        return self.name

    # Bind professor to course
    def AddCourseClass(self, courseClass):
        self.courseClasses.append(courseClass)

    # Returns reference to list of classes that professor teaches
    def GetCourseClasses(self):
        return self.courseClasses
    
    # Compares ID's of two objects which represent professors
    def __eq__(self, rhs):
        return self.id == rhs.id

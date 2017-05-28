class StudentsGroup:

    # Initializes student group data
    def __init__(self, id, name, numberOfStudents):
        self.id = id
        self.name = name
        self.numberOfStudents = numberOfStudents
        self.courseClasses = []
        
    # Bind group to class
    def AddClass(self, courseClass):
        self.courseClasses.append(courseClass)

    # Returns student group ID
    def GetId(self):
        return self.id

    # Returns name of student group
    def GetName(self):
        print(str(self.name))
        return str(self.name)

    # Returns number of students in group
    def GetNumberOfStudents(self):
        return int(self.numberOfStudents)

    # Returns reference to list of classes that group attends
    def GetCourseClasses(self):
        return self.courseClasses

    # Compares ID's of two objects which represent student groups
    def __eq__(self, rhs):
        return self.id == rhs.id

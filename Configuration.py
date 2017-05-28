import Professor
import StudentsGroup
import Course
import Room
import CourseClass

# Reads configration file and stores parsed objects
class Configuration:

    global instance
    
    # Initialize data
    def __init__(self):
        self.isEmpty = True
        self.professors = {}
        self.studentGroups = {}
        self.courses = {}
        self.rooms = {}
        self.courseClasses = []

        Room.Room.RestartIDs()

    # Returns reference to global instance of configuration
    def GetInstance():
        instance = Configuration()
        return instance

    # Parse file and store parsed object
    def Parsefile(self, fileName):
        # clear previously parsed objects
        self.professors = {}
        self.studentGroups = {}
        self.courses = {}
        self.rooms = {}
        self.courseClasses = []

        Room.Room.RestartIDs()

        # open file
        counter = 0
        with open(fileName, "r") as input:
            for line in input:
                counter = counter + 1
                # get type of object, parse obect and store it
                strippedLine = line.strip()
                if strippedLine == '#prof':
                    p = self.__ParseProfessor(input)
                    if p:
                        self.professors[p.GetId()] = p
                elif strippedLine == '#group':
                    g = self.__ParseStudentsGroup(input)
                    if g:
                        self.studentGroups[g.GetId()] = g
                elif strippedLine == '#course':
                    c = self.__ParseCourse(input)
                    if c:
                        self.courses[c.GetId()] = c
                elif strippedLine == '#room':
                    r = self.__ParseRoom(input)
                    if r:
                        self.rooms[r.GetId()] = r
                elif strippedLine == '#class':
                    c = self.__ParseCourseClass(input)
                    if c:
                        self.courseClasses.append(c)
        input.close()
        self.isEmpty = False
        
    # Returns pointer to professor with specified ID
    # If there is no professor with such ID method returns NULL
    def GetProfessorById(self, id):
        if id in self.professors.keys():
            return self.professors[id]
        return None
    
    # Returns number of parsed professors
    def GetNumberOfProfessors(self):
        return len(self.professors.keys())

    # Returns pointer to student group with specified ID
    # If there is no student group with such ID method returns NULL
    def GetStudentsGroupById(self, id):
        if id in self.studentGroups.keys():
            return self.studentGroups[id]
        return None    
        
    # Returns number of parsed student groups
    def GetNumberOfStudentGroups(self):
        return len(self.studentGroups)
    
    # Returns pointer to course with specified ID
    # If there is no course with such ID method returns NULL
    def GetCourseById(self, id):
        if id in self.courses.keys():
            return self.courses[id]
        return None

    # Returns number of parsed courses
    def GetNumberOfCourses(self):
        return len(self.courses)
    
    # Returns pointer to room with specified ID
    # If there is no room with such ID method returns NULL
    def GetRoomById(self, id):
        if id in self.rooms.keys():
            return self.rooms[id]
        return None
    
    # Returns number of parsed rooms
    def GetNumberOfRooms(self):
        return len(self.rooms)
    
    # Returns reference to list of parsed classes
    def GetCourseClasses(self):
        return self.courseClasses
    
    # Returns number of parsed classes
    def GetNumberOfCourseClasses(self):
        return len(self.courseClasses)
    
    # Returns TRUE if configuration is not parsed yet
    def isEmpty(self):
        return self.isEmpty

    # Reads professor's data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseProfessor(self, file):
        newFile = file
        id = 0
        name = ''
        dictConfig  = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == '#end':
                break
            key = ''
            value = ''
            p = line.find('=')
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1:].strip()
            
            for key in dictConfig.keys():
                if key == 'id':
                    id = dictConfig[key]
                elif key == 'name':
                    name = dictConfig[key]

        # make object and return pointer to it
        if id == 0:
            return None
        
        return Professor.Professor(id, name)

     
    # Reads professor's data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseStudentsGroup(self, file):
        newFile = file
        id = 0
        number = 0
        name = ''
        dictConfig  = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == '#end':
                break
            key = ''
            value = ''
            p = line.find('=')
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1:].strip()
            
            for key in dictConfig.keys():
                if key == 'id':
                    id = dictConfig[key]
                elif key == 'name':
                    name = dictConfig[key]
                elif key == 'size':
                    number = dictConfig[key]

        # make object and return pointer to it
        if id == 0:
            return None
        return StudentsGroup.StudentsGroup( id, name, number )

    # Reads course's data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseCourse(self, file):
        print("parse course")
        newFile = file
        id = 0
        name = ''
        dictConfig = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == '#end':
                break
            key = ''
            value = ''
            p = line.find('=')
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1:].strip()
            
            for key in dictConfig.keys():
                if key == 'id':
                    id = dictConfig[key]
                elif key == 'name':
                    name = dictConfig[key]

        # make object and return pointer to it
        if id == 0:
            return None
 
        return Course.Course(id, name)

    # Reads rooms's data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseRoom(self, file):
        newFile = file
        number = 0
        lab = False
        name = ''
        dictConfig = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == '#end':
                break
            key = ''
            value = ''
            p = line.find('=')
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1:].strip()
            
            for key in dictConfig.keys():
                if key == 'name':
                    name = dictConfig[key]
                elif key == 'lab':
                    lab = dictConfig[key]
                elif key == 'size':
                    number = dictConfig[key]

        # make object and return pointer to it
        if number == 0:
            return None

        return Room.Room( name, lab, number )
    
    # Reads class' data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseCourseClass(self, file):
        newFile = file
        pid = 0
        cid = 0
        dur = 1
        lab = False
        groups = []
        dictConfig = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == '#end':
                break
            key = ''
            value = ''
            p = line.find('=')
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1:].strip()
            
            for key in dictConfig.keys():
                if key == 'professor':
                    pid = dictConfig[key]
                elif key == 'course':
                    cid = dictConfig[key]
                elif key == 'lab':
                    lab = dictConfig[key]
                elif key == 'duration':
                    dur = dictConfig[key]
                elif key == 'group':
                    g = self.GetStudentsGroupById(dictConfig[key])
                    if g:
                        groups.append(g)

        # get professor who teaches class and course to which this class belongs
        p = self.GetProfessorById(pid)
        c = self.GetCourseById(cid)

        # does professor and class exists
        if not c or not p:
            return None
        
        # make object and return pointer to it
        return CourseClass.CourseClass( p, c, groups, lab, dur )

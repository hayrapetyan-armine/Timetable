import Professor
import StudentsGroup
import Course

class CourseClass:

    # Initializes class object
    def __init__(self, professor, course, groups, requiresLab, duration):
        self.professor = professor
        self.course = course
        self.numberOfSeats = 0
        self.requiresLab = requiresLab
        self.duration = duration
        self.groups = groups
        
        # bind professor to class
        self.professor.AddCourseClass(self)

        # bind student groups to class
        groupLength = len(self.groups)
        for i in range(groupLength): # self.groups:
            self.groups[i].AddClass(self)
            self.numberOfSeats = self.numberOfSeats + StudentsGroup.StudentsGroup.GetNumberOfStudents(self.groups[i])
            
    # Returns TRUE if another class has one or more overlapping student groups
    def GroupsOverlap(self, c):
        for grKey in self.groups:
            for cKey in c.groups:
                if grKey == cKey:
                  #  print("group_overlap", grKey, cKey)
                    return True
        return False

    # Returns TRUE if another class has same professor
    def ProfessorOverlaps(self, c):
       # print("professor_overlap", self.professor, c.professor)
        return self.professor == c.professor

    # Return pointer to professor who teaches
    def GetProfessor(self):
        return self.professor

    # Return pointer to course to which class belongs
    def GetCourse(self):
        return self.course

    # Returns reference to list of student groups who attend class
    def GetGroups(self): 
        return self.groups

    # Returns number of seats (students) required in room
    def GetNumberOfSeats(self):
        return int(self.numberOfSeats)

    # Returns TRUE if class requires computers in room
    def IsLabRequired(self):
        return self.requiresLab

    # Returns duration of class in hours
    def GetDuration(self):
        return int(self.duration)

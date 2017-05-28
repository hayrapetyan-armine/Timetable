import CourseClass
import Configuration
import copy
from random import randint
import Algorithm

# Number of working hours per day
DAY_HOURS = 12
# Number of days in week
DAYS_NUM = 5

# Schedule chromosome
class Schedule:
        # Initializes chromosomes with configuration block (setup of chromosome)
        def __init__(self, numberOfCrossoverPoints, mutationSize, crossoverProbability, mutationProbability):
                # Number of crossover points of parent's class tables
                self.numberOfCrossoverPoints = numberOfCrossoverPoints
                # Number of classes that is moved randomly by single mutation operation
                self.mutationSize = mutationSize
                # Probability that crossover will occure
                self.crossoverProbability = crossoverProbability
                # Probability that mutation will occure
                self.mutationProbability = mutationProbability
                # Fitness value of chromosome
                self.fitness = 0
                # Time-space slots, one entry represent one hour in one classroom
                self.slots = []
                # Flags of class requirements satisfaction
                self.criteria = []

                self.slots = DAYS_NUM * DAY_HOURS * Algorithm.instance.GetNumberOfRooms() * [None]
                self.criteria = Configuration.instance.GetNumberOfCourseClasses() * 5

        # Imitates copy constructor in C++
        def copy(self):
                return copy.deepcopy(self)

        # Makes new chromosome with same setup but with randomly chosen code
        def MakeNewFromPrototype(self):
                # number of time-space slots
                size = len(self.slots)

                # make new chromosome, copy chromosome setup
                newChromosome = self.copy()
                newChromosome.classes = {}
                # place classes at random position
                c = Configuration.instance.GetCourseClasses()
                for it in c:
                        # determine random position of class
                        nr = Configuration.instance.GetNumberOfRooms()
                        dur = c[it].GetDuration()
                        day = randint(0,32767) % DAYS_NUM
                        room = randint(0, 32767) % nr
                        time = randint(0, 32767) % ( DAY_HOURS + 1 - dur )
                        pos = day * nr * DAY_HOURS + room * DAY_HOURS + time

                        # fill time-space slots, for each hour of class
                        for i in range(dur - 1, -1, -1):
                                newChromosome.slots[pos + i].push(c[it])

                        # insert in class table of chromosome
                        newChromosome.classes[pos] = c[it]

                newChromosome.CalculateFitness()

                # return smart pointer
                return newChromosome

        # Performes crossover operation using two chromosomes and returns pointer to offspring
        def Crossover(self, parent2):
                # check probability of crossover operation
                if randint(0, 32767) % 100 > self.crossoverProbability:
                        # no crossover, just copy first parent
                        return Schedule.Schedule( self, False )

                # new chromosome object, copy chromosome setup
                n = Schedule.Schedule( self, True )

                # number of classes
                size = len(self.classes)
                cp = size * [None]

                # determine crossover point (randomly)
                for i in range(self.numberOfCrossoverPoints, 0, -1):
                        while 1:
                                p = randint(0, 32767) % size
                                if (not cp[p]):
                                        cp[p] = True
                                        break

                j = 0
                it1 = self.classes[j]
                it2 = parent2.classes[j]
                # make new code by combining parent codes
                first = randint(0, 1) == 0
                for i in range(0, size):
                        if first:
                                # insert class from first parent into new chromosome's class table
                                n.classes[j] = it1
                                # all time-space slots of class are copied
                                for k in range(it1.GetDuration() - 1, -1, -1):
                                        n.slots[j + k].push(it1)
                        else:
                                # insert class from second parent into new chromosome's class table
                                n.classes[j] = it2
                                # all time-space slots of class are copied
                                for k in range(it2.GetDuration() - 1, -1, -1):
                                        n.slots[j + k].push(it2)

                        # crossover point
                        if cp[i]:
                                # change source chromosome
                                first = not first

                        j = j + 1

                n.CalculateFitness()

                # return smart pointer to offspring
                return n

        # Performs mutation on chromosome
        def Mutation(self):
                # check probability of mutation operation
                if randint(0, 32767) % 100 > self.mutationProbability:
                        return None

                # number of classes
                numberOfClasses = len(self.classes)
                # number of time-space slots
                size = len(self.slots)

                # move selected number of classes at random position
                for i in range(self.mutationSize, 0, -1):
                        # select random chromosome for movement
                        mpos = randint(0, 32767) % numberOfClasses
                        pos1 = j = mpos

                        cc1 = self.classes[pos1]

                        # determine position of class randomly
                        nr = Schedule.instance.GetNumberOfRooms()
                        dur = cc1.GetDuration()
                        day = randint(0, 32767) % DAYS_NUM
                        room = randint(0, 32767) % nr
                        time = randint(0, 32767) % ( DAY_HOURS + 1 - dur )
                        pos2 = day * nr * DAY_HOURS + room * DAY_HOURS + time

                        # move all time-space slots
                        for j in range(dur - 1, -1, -1):
                                # remove class hour from current time-space slot
                                c1 = self.slots[pos1 + i]
                                for k in range(0, len(self.slots)):
                                        if c1[k] == cc1:
                                                del c1[k]
                                                break

                                # move class hour to new time-space slot
                                self.slots[pos2 + i].push(cc1)

                        # change entry of class table to point to new time-space slots
                        self.classes[ cc1 ] = pos2

                self.CalculateFitness()

        # Calculates fitness value of chromosome
        def CalculateFitness(self):
                # chromosome's score
                score = 0
                numberOfRooms = Configuration.instance.GetNumberOfRooms()
                daySize = DAY_HOURS * numberOfRooms

                ci = 0
		
                # check criterias and calculate scores for each class in schedule
                for i in range(0, len(self.classes)):
                        # coordinate of time-space slot
                        p = i
                        day = p / daySize
                        time = p % daySize
                        room = time / DAY_HOURS
                        time = time % DAY_HOURS

                        dur = classes[i].GetDuration()

                        # check for room overlapping of classes
                        ro = False
                        for j in range(dur - 1, -1, -1):
                                if self.slots[p + j].size() > 1:
                                        ro = True
                                        break

                        # on room overlapping
                        if not ro:
                                score = score + 1

                        self.criteria[ci + 0 ] = not ro
                        
                        cc = classes[i]
                        r = Configuration.instance.GetRoomById( room )
                        # does current room have enough seats
                        self.criteria[ci + 1 ] = r.GetNumberOfSeats() >= cc.GetNumberOfSeats()
                        if self.criteria[ ci + 1 ]:
                                score = score + 1

                        # does current room have computers if they are required
                        self.criteria[ ci + 2 ] = (not cc.IsLabRequired()) or (cc.IsLabRequired() and r.IsLab())
                        if self.criteria[ ci + 2 ]:
                                score = score + 1

                        po = False
                        go = False
                        # check overlapping of classes for professors and student groups
                        t = day * daySize + time
                        breakPoint = False
                        for k in range(numberOfRooms, 0, -1):
                                if breakPoint == True: break
                                # for each hour of class
                                for l in range(dur - 1, -1, -1):
                                        if breakPoint == True: break
                                        # check for overlapping with other classes at same time
                                        cl = self.slots[ t + k ]
                                        for it in range(0, len(cl)):
                                                if cc != cl[it]:
                                                        # professor overlaps?
                                                        if not po and cc.ProfessorOverlaps(cl[it]):
                                                                po = True
                                                        # student group overlaps?
                                                        if not go and cc.GroupsOverlap(cl[it]):
                                                                go = True
                                                        # both type of overlapping? no need to check more
                                                        if po and go:
                                                                breakPoint = True
                                                                
                                t = t + DAY_HOURS
                        # professors have no overlapping classes?
                        if not po:
                                score = score + 1
                        self.criteria[ ci + 3 ] = not po

                        # student groups has no overlapping classes?
                        if not go:
                                score = score + 1
                        self.criteria[ ci + 4 ] = not go

                        ci += 5

                # calculate fitness value based on score
                self.fitness = score / ( Configuration.instance.GetNumberOfCourseClasses() * DAYS_NUM )

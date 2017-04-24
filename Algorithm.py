import CourseClass
import Configuration
#from Configuration import Configuration
import copy
import random
from random import randint

# Genetic algorithm
class Algorithm:

    # Initializes genetic algorithm
    def __init__(self, numberOfChromosomes, replaceByGeneration, trackBest, prototype ):
        self.replaceByGeneration = replaceByGeneration
        self.prototype = prototype
        self.currentBestSize = 0
        self.currentGeneration = 0
	
        # there should be at least 2 chromosomes in population
        if numberOfChromosomes < 2:
            numberOfChromosomes = 2
                
        # and algorithm should track at least one of best chromosomes
        if trackBest < 1:
            trackBest = 1

        if self.replaceByGeneration < 1:
            self.replaceByGeneration = 1
        elif self.replaceByGeneration > numberOfChromosomes - trackBest:
            self.replaceByGeneration = numberOfChromosomes - trackBest
        # reserve space for population
        self.chromosomes = numberOfChromosomes * [None]
        self.bestFlags = numberOfChromosomes * [False]

        # reserve space for best chromosome group
        self.bestChromosomes = trackBest * [None]


    # Returns reference to global instance of algorithm
    def GetInstance():
        # make prototype of chromosomes
        prototype = Schedule(2, 2, 80, 3)
        # make new global instance of algorithm using chromosome prototype
        instance = Algorithm(100, 8, 5, prototype )
        
        return instance

    # Start
    def Start(self):
        # clear best chromosome group from previous execution
        #ClearBest()
        # initialize new population with chromosomes randomly built using prototypes
        for it in range(len(self.chromosomes)):
            # remove chromosomes from previous execution
            if self.chromosomes[ it ]:
                del self.chromosomes[ it ]

            # add new chromosome to population
            self.chromosomes[ it ] = self.prototype.MakeNewFromPrototype()
           # print("self.chromosomes", len(self.chromosomes), len(self.chromosomes[it].classes), it)
          #  print("fff", self.chromosomes[ it ].GetFitness())
            self.AddToBest( it )
           # print("best:", self.GetBestChromosome().GetFitness())
          #  print("ggg", self.chromosomes[ it ].GetFitness())

        self.currentGeneration = 0
        random.seed()
        lengthOfChromosomes = len(self.chromosomes)

        while 1:
            best = self.GetBestChromosome()
          #  print("best", best.GetFitness(), best.score, len(best.classes.keys()))
            # algorithm has reached criteria?
            if best.GetFitness() >= 1:
                print("best", best.GetFitness(), best.score)
                break

            # produce offspring
            offspring = self.replaceByGeneration * [None]
            for j in range(0, self.replaceByGeneration):
                # selects parent randomly
                a = randint(0, 327670) % lengthOfChromosomes
                b = randint(0, 327670) % lengthOfChromosomes
              #  print("a = ", a, b, len(self.chromosomes[ a ].classes), len(self.chromosomes[ b ].classes))
                p1 = self.chromosomes[ a ]
                p2 = self.chromosomes[ b ]
               # print("p1 and p2", len(p1.classes),len(self.chromosomes[ a ].classes), len(p2.classes),len(self.chromosomes[ b ].classes), j)
                offspring[j] = p1.Crossover(p2)
                offspring[j].Mutation()

            # replace chromosomes of current operation with offspring
            for j in range(0, self.replaceByGeneration):
                # select chromosome for replacement randomly
                ci = randint(0, 32767) % len(self.chromosomes)
                # protect best chromosomes from replacement
                while (self.IsInBest( ci )):
                    ci = randint(0, 32767) % len(self.chromosomes)

                # replace chromosome
                # delete self.chromosomes[ci]
                #print("self.chromosomes[ci]", self.chromosomes[ci])
                self.chromosomes[ ci ] = offspring[ j ]

                # try to add new chromosomes in best chromosome group
                self.AddToBest( ci )

            self.currentGeneration = self.currentGeneration + 1
           # print("currentGeneration: ", self.currentGeneration)
            
    # Returns pointer to best chromosomes in population
    def GetBestChromosome(self):
        return self.chromosomes[ self.bestChromosomes[ 0 ] ]

    # Tries to add chromosomes in best chromosome group
    def AddToBest(self, chromosomeIndex):
        # don't add if new chromosome hasn't fitness enough big
        # for best chromosome group or it is already in the group

      # and (not self.chromosomes[self.bestChromosomes[self.currentBestSize - 1]] is None) and
       # print("chromosomeIndex", chromosomeIndex, self.chromosomes[ chromosomeIndex ].GetFitness())
        if ( self.currentBestSize == len(self.bestChromosomes) and self.chromosomes[self.bestChromosomes[self.currentBestSize - 1]].GetFitness() >= \
           self.chromosomes[ chromosomeIndex ].GetFitness() ) or self.bestFlags[ chromosomeIndex ]:
              return

        # find place for new chromosome
        i = self.currentBestSize
        j = 0
       # print("self.currentBestSize", self.currentBestSize)
        for i in range( self.currentBestSize, 0, -1 ):
            # group is not full?
            if i < len( self.bestChromosomes ):
                # position of new chromosome is found?
                # (not self.chromosomes[ self.bestChromosomes[ i - 1 ] ] is None) and
              #  print("fitnessses: ", self.chromosomes[ self.bestChromosomes[ i - 1 ] ].GetFitness(), self.chromosomes[ chromosomeIndex ].GetFitness())
                if  self.chromosomes[ self.bestChromosomes[ i - 1 ] ].GetFitness() > \
                   self.chromosomes[ chromosomeIndex ].GetFitness():
                    j = i
                    break

                # move chromosomes to make room for new
              #  print("move chromosome", self.bestChromosomes[ i ])
                self.bestChromosomes[ i ] = self.bestChromosomes[ i - 1 ]
              #  print("i2 = ", i)
            else:
                # group is full remove worst chromosomes in the group
                self.bestFlags[ self.bestChromosomes[ i - 1 ] ] = False
            j = i - 1

        # store chromosome in best chromosome group
        self.bestChromosomes[ j ] = chromosomeIndex
        self.bestFlags[ chromosomeIndex ] = True
      #  print("aaaa", self.bestChromosomes[ 0 ])
        
        # increase current size if it has not reached the limit yet
        if self.currentBestSize < len(self.bestChromosomes):
            self.currentBestSize = self.currentBestSize + 1

    # Return True if chromosome belongs to best chromosome group
    def IsInBest(self, chromosomeIndex):
        return self.bestFlags[ chromosomeIndex ]

    # Clear best chromosome group
    def ClearBest(self):
        for i in range(len(self.bestFlags), -1, -1):
            self.bestFlags[ i ] = False

        self.currentBestSize = 0


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
            self.score = 0
            self.classes = {}
            self.slots = ( DAYS_NUM * DAY_HOURS * instance.GetNumberOfRooms() ) * [None]
            self.criteria = (instance.GetNumberOfCourseClasses() * 5 )* [None] 

    # Imitates copy constructor in C++
    def copy(self, setupOnly):
        #return copy.deepcopy(self)
        c = Schedule(0,0,0,0)
        
        if not setupOnly:
            # copy code
            c.slots = self.slots
            c.classes = self.classes

            # copy flags of class requirements
            c.criteria = self.criteria

            # copy fitness
            c.fitness = self.fitness
        else:
            # reserve space for time-space slots in chromosomes code
            c.slots = ( DAYS_NUM * DAY_HOURS * instance.GetNumberOfRooms() ) * [None]

            # reserve space for flags of class requirements
            c.criteria = ( instance.GetNumberOfCourseClasses() * 5 ) * [None]

        # copy parameters
        c.numberOfCrossoverPoints = self.numberOfCrossoverPoints
        c.mutationSize = self.mutationSize
        c.crossoverProbability = self.crossoverProbability
        c.mutationProbability = self.mutationProbability

        return c
                

    # Makes new chromosome with same setup but with randomly chosen code
    def MakeNewFromPrototype(self):
            # number of time-space slots
            size = len(self.slots)
            #print("size if slots: ")
            # make new chromosome, copy chromosome setup
            newChromosome = self.copy(True)
           # newChromosome.classes = {}
            # place classes at random position
            c = instance.GetCourseClasses()
            nr = instance.GetNumberOfRooms()
            maxLength = nr * DAY_HOURS * DAYS_NUM
            # newChromosome.slots = [None] * maxLength
         #   print("length of c: ", len(c))
            for it in c:
                # determine random position of class
                dur = it.GetDuration()
                day = randint(0,32767) % DAYS_NUM
                room = randint(0, 32767) % nr
                time = randint(0, 32767) % (DAY_HOURS + 1 - dur)
                pos = day * nr * DAY_HOURS + room * DAY_HOURS + time
                newChromosome.classes[ it ] = pos
                        
              #  print("duration: ", dur)
                #print("it in c: ", dur, day, room, time, pos)
                # fill time-space slots, for each hour of class
                for i in range( dur - 1, -1, -1 ):
                    if newChromosome.slots[ pos + i ] is None:
                        newChromosome.slots[ pos + i ] = [ it ]
                    else:
                        newChromosome.slots[ pos + i ].append( it )

                # insert in class table of chromosome
                newChromosome.classes[ it ] = pos
               # print("slots and class at position: ", pos, newChromosome.slots[ pos ], newChromosome.classes[ pos ])

           # print("lengthofclasses", len(newChromosome.classes))
            newChromosome.CalculateFitness()

            # return smart pointer
            return newChromosome

    # Performes crossover operation using two chromosomes and returns pointer to offspring
    def Crossover(self, parent2):
        # check probability of crossover operation
        if randint(0, 32767) % 100 > self.crossoverProbability:
            # no crossover, just copy first parent
            return self.copy(False)

        # new chromosome object, copy chromosome setup
        n = self.copy(True)

        # number of classes
        size = len(self.classes)
        cp = size * [None]

        # determine crossover point (randomly)
        for i in range( self.numberOfCrossoverPoints, 0, -1 ):
            while 1:
                p = randint( 0, 32767 ) % size
                if (not cp[ p ]):
                    cp[ p ] = True
                    break

        j = 0
        
        # make new code by combining parent codes
        first = randint( 0, 1 ) == 0
        for i in range( 0, size ):
            if first:
                # insert class from first parent into new chromosome's class table
                if j >= len(list(self.classes.keys())):
                        break
                it1 = self.classes[ list(self.classes.keys())[ j ] ]
                n.classes[ list( self.classes.keys() )[ j ] ] = it1
                # all time-space slots of class are copied
                for k in range( list( self.classes.keys() )[ j ].GetDuration() - 1, -1, -1 ):
                    if n.slots[ it1 + k ] is None:
                        n.slots[ it1 + k ] = [ list(self.classes.keys())[ j ] ]
                    else:
                        n.slots[ it1 + k ].append( list(self.classes.keys())[ j ] )
                   # print("k = ", k)
            else:
                # insert class from second parent into new chromosome's class table
                if j >= len(list(parent2.classes.keys())):
                        break
                it2 = parent2.classes[ list(parent2.classes.keys())[ j ] ]
                n.classes[ list(parent2.classes.keys())[ j ] ] = it2
                # all time-space slots of class are copied
                for k in range( list(parent2.classes.keys())[ j ].GetDuration() - 1, -1, -1 ):
                    if n.slots[ it2 + k ] is None:
                        n.slots[ it2 + k ] = [ list(parent2.classes.keys())[ j ] ]
                    else:
                        n.slots[ it2 + k ].append( list(parent2.classes.keys())[ j ] )

            # crossover point
            if cp[ i ]:
                # change source chromosome
                first = not first

            j = j + 1
           # print("j = ", j)
           # if j >= len(list(self.classes.keys())) or j >= len(list(parent2.classes.keys())):
           #     break
           # it1 = self.classes[ list(self.classes.keys())[ j ] ]
          #  it2 = parent2.classes[ list(parent2.classes.keys())[ j ] ]

      #  print("crossover", len(n.classes), n.classes)
       # print("n.slots: ", len(n.slots))
       # print("crossover", len(n.classes))
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
                pos1 = self.classes[ list(self.classes.keys())[ mpos ] ]
                it = list(self.classes.keys())[ mpos ]
               # list1 = list(self.classes)

                cc1 = it

                # determine position of class randomly
                nr = instance.GetNumberOfRooms()
                dur = cc1.GetDuration()
                day = randint(0, 32767) % DAYS_NUM
                room = randint(0, 32767) % nr
                time = randint(0, 32767) % ( DAY_HOURS + 1 - dur )
                pos2 = day * nr * DAY_HOURS + room * DAY_HOURS + time

                # move all time-space slots
                for j in range( dur - 1, -1, -1 ):
                    # remove class hour from current time-space slot
                    c1 = self.slots[ pos1 + j ]
                    for k in range( 0, len( c1 ) ):
                      #  print("c1[k] and cc1: ", c1[ k ], cc1)
                        if c1[ k ] == cc1:
                            del c1[ k ]
                            break

                    # move class hour to new time-space slot
                    if self.slots[ pos2 + j ] is None:
                        self.slots[ pos2 + j ] = [ cc1 ]
                    else:
                        self.slots[ pos2 + j ].append( cc1 )

                # change entry of class table to point to new time-space slots
               # del self.classes[ pos1 ]
                self.classes[ cc1 ] = pos2
            #print("mutation")
         #   print('leng', len(self.classes.keys()))
            self.CalculateFitness()

    # Calculates fitness value of chromosome
    def CalculateFitness(self):
        # chromosome's score
        score = 0
        numberOfRooms = instance.GetNumberOfRooms()
        daySize = DAY_HOURS * numberOfRooms

        ci = 0
       # print("len of self classes: ", len(self.classes))
        #    self.criteria = [None] * len(self.classes.keys())
          #  self.slots = [x for x in self.slots if x is not None]
            # check criterias and calculate scores for each class in schedule
            #print("slots:", len(self.slots))
##            for temp in range(len(self.slots)):
##                try:
##                    if self.slots[temp] == None:
##                        print("temp", temp)
##                        del self.slots[temp]
##                except IndexError:
##                    pass
            #print("slots:", self.slots)
            #print(len(self.criteria))
       # print("len", len(self.classes), len(self.criteria))
       # print("self.classes", self.classes)
      #  print("len of classes", len(self.classes.keys()))
        for i in self.classes.keys():
            #print('ci: ', i)
            # coordinate of time-space slot
            p = self.classes[ i ]
            day = p // daySize
            time = p % daySize
            room = time // DAY_HOURS
           # print("time: ", time, p, daySize)
            time = time % DAY_HOURS

           # print("aaaaaaaaaa", p, day * daySize + time, day, daySize, time) # 66 54 2 24 6

            #print('day', p, day, daySize, time, room, DAY_HOURS)
            #print("classes", i, self.classes[i])
            dur = i.GetDuration()
           # print("self.slots[i] ", i, dur, self.slots[i], self.slots[p])

            # check for room overlapping of classes
            ro = False
            for j in range( dur - 1, -1, -1 ):
               # print("P + J is: ", p + j)
                if len( self.slots[ p + j ] ) > 1: # not self.slots[p + j] is None and
                    ro = True
                    break

            # on room overlapping
            if not ro:
                score = score + 1

            #print(self.criteria[ci + 0])
           # print("ci: ", ci)
            self.criteria[ ci + 0 ] = not ro
                
            cc = i
            r = instance.GetRoomById( room )
            #print("r: ", instance, room)
            # does current room have enough seats
            #print("number of seats: ", r.GetNumberOfSeats())
           # print("ci = ", ci)
            self.criteria[ ci + 1 ] = r.GetNumberOfSeats() >= cc.GetNumberOfSeats()
            if self.criteria[ ci + 1 ]:
                score = score + 1

            # does current room have computers if they are required
            self.criteria[ ci + 2 ] = ( not cc.IsLabRequired() ) or ( cc.IsLabRequired() and r.IsLab() )
            if self.criteria[ ci + 2 ]:
                score = score + 1

            po = False
            go = False
            # check overlapping of classes for professors and student groups
            t = day * daySize + time
           # print('vsyo budet', day, daySize, time, t, len(self.slots))
            breakPoint = False
            for k in range( numberOfRooms, 0, -1 ):
                if breakPoint == True: break
                # for each hour of class
                for l in range( dur - 1, -1, -1 ):
                    if breakPoint == True: break
                    # check for overlapping with other classes at same time
                   # print("slots", len(self.slots), t, k)
                    cl = self.slots[ t + l ]
                    if not cl is None:
                        for it in cl:
                            if breakPoint == True: break
                            if cc != it:
                                # professor overlaps?
                                if not po and cc.ProfessorOverlaps( it ):
                                    po = True
                                # student group overlaps?
                                if not go and cc.GroupsOverlap( it ):
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
        
        self.fitness = score / ( instance.GetNumberOfCourseClasses() * DAYS_NUM )
        self.score = score
        #if self.fitness > 0.95:
       # print(self.fitness, score, instance.GetNumberOfCourseClasses() * DAYS_NUM)
       # print("fitness: ", self.fitness)

    # Returns fitness value of chromosome
    def GetFitness(self):
        return self.fitness
            
##import Configuration
###Configuration.Configuration.GetInstance().Parsefile("Test.cfg")
##instance = Configuration.Configuration()
##instance.Parsefile("ase.cfg")
##Algorithm.GetInstance().Start()

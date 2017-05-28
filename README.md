# Timetable
Creating Timetable automation system using Genetic Algorithms. It is written by Python 3.5 and PyQt5.

## The problem
Making a class schedule is one of those NP hard problems. The problem can be solved using a heuristic search algorithm 
to find the optimal solution, but it only works for simple cases. For more complex inputs and requirements, 
finding a considerably good solution can take a while, or it may be impossible. 
This is where genetic algorithms come in to the game.

## Background
When you make a class schedule, you must take into consideration 
many requirements (number of professors, students, classes and classrooms, size of classroom, 
laboratory equipment in classroom, and many others). 
These requirements can be divided into several groups by their importance. 
Hard requirements (if you break one of these, then the schedule is infeasible):

* A class can be placed only in a spare classroom.
* No professor or student group can have more then one class at a time.
* A classroom must have enough seats to accommodate all students.
* To place a class in a classroom, the classroom must have laboratory equipment (computers, in our case) if the class requires it.

Some soft requirements (can be broken, but the schedule is still feasible):

* Preferred time of class by professors.
* Preferred classroom by professors.
* Preferred time of class by student groups.

Hard and soft requirements, of course, depend on the situation. 
<b>In this example, only hard requirements are implemented!!!</b>

## The solution
The input file is .cfg format which describes initial objects. Let's describe configuration file.

<b>Configuration File</b>

Types of objects:

professor (#prof tag) - describes a professor.<br>
course (#course tag) - describes a course.<br>
room (#room tag) - describes a room.<br>
group (#group tag) - describes a students group.<br>
course class (#class tag) - describes a class, and binds the professor, course, and students group.<br>

Each object begins with its tag and finishes with the #end tag, all tags must be in separate lines. 
In the body of an object, each line contains only one key and value pair (attribute) separated by an = character. 
Each attribute should be specified just one time, except for the group attribute 
in the #group object which can have multiple group attributes. Tag and key names are case sensitive. 
Here is a list of the objects' attributes:<br>

#prof<br>
id (number, required) - ID of the professor.<br>
name (string, required) - name of the professor.<br>
#course<br>
id (number, required) - ID of the course.<br>
name (string, required) - name of the course.<br>
#room<br>
name (string, required) - name of the room.<br>
size (number, required) - number of seats in the room.<br>
lab (boolean, optional) - indicates if the room is a lab (has computers); if not specified, the default value is false.<br>
#group<br>
id (number, required) - ID of the students group.<br>
name (string, required) - name of the students group.<br>
size (number, required) - number of students in the group.<br>
#class<br>
professor (number, required) - ID of a professor; binds a professor to a class.<br>
course (number, required) - ID of a course; binds a course to a class.<br>
group (number, required) - ID of a students group; binds the students group to a class; each class can be bound to multiple students groups.<br>
duration (number, optional) - duration of class (in hours); if not specified, the default value is 1.<br>
lab (boolean, optional) - if the class requires computers in a room; if not specified, the default value is false.<br>

<b>Example of a Configuration File</b>
<pre>#prof
    id = 1
    name = Sahakyan George
#end

#course
    id = 1
    name = Functional programming (Lisp)
#end

#room
    name = R50
    lab = true
    size = 24
#end

#group
    id = 1
    name = KM3
    size = 19
#end

#class
    professor = 1
    course = 1
    duration = 2
    group = 1
    group = 2
#end

#class
    professor = 1
    course = 1
    duration = 3
    group = 1
    lab = true
#end

#class
    professor = 1
    course = 1
    duration = 3
    group = 2
    lab = true
#end</pre>

## Steps to implement application
1. Execute gui.py file
2. In the File dropdown, click on Open button to import .cfg file (example is described above)
3. After click on Start Solving 
4. After waiting sometimes timetable will appear in your desktop.

## Example of implemented Timetable.

![22](https://cloud.githubusercontent.com/assets/11331810/26530141/9fcde062-43d7-11e7-910b-a1d65d73fe7b.png)

from itertools import groupby

print("Hello world")

# define Student class
class Student:
  def __init__(self, lastname, firstname, grade, classroom, bus, gpa,
      tlastname, tfirstname):
    self.lastname = lastname
    self.firstname = firstname
    self.grade = grade
    self.bus = bus
    self.classroom = classroom
    self.gpa = gpa
    self.tlastname = tlastname
    self.tfirstname = tfirstname

  def __repr__(self):
    return "(" + ", ".join([self.lastname, self.firstname, str(self.grade), 
                            str(self.classroom), str(self.bus), str(self.gpa), 
                            self.tlastname, self.tfirstname]) + ")"

# parse students.txt into a list of Student objects
try:
  file = open("students.txt")
  # TODO: check if line is in the correct format
  students = [Student(*line.rstrip().split(",")) for line in file]
  file.close()
except FileNotFoundError:
  print("students.txt does not exist")
  exit(1)

# define getters
get_lastname = lambda s: s.lastname
get_tlastname = lambda s: s.tlastname
get_bus = lambda s: s.bus
get_grade = lambda s: s.grade

# sort list of students by last name
sorted_by_lastname = sorted(students, key=get_lastname)

# group sorted list by last name and store as dictionary
grouped_by_lastname = \
  dict((k, list(v)) for k, v in groupby(sorted_by_lastname, key=get_lastname))

print(grouped_by_lastname)

# sort list of students by their teacher's last name
# group sorted list by teacher's last name and store as dictionary

# sort list of students by bus route
# groupd sorted list by bus route and store as dictionary

# sort list of students by grade level
# sort list of student by grade level and store as dictionary



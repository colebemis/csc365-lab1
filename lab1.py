from itertools import groupby

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

# groups by given key
def group(lst, keyfunc):
  sorted_lst = sorted(lst, key=keyfunc)
  return dict((k, list(v)) for k, v in groupby(sorted_lst, key=keyfunc))

# parses a file into a list of Student objects
def parse_file(filename):
  try:
    file = open(filename)
    # TODO: check if line is in the correct format. exit program if incorrect
    students = [Student(*line.rstrip().split(",")) for line in file]
    file.close()
    return students 

  except FileNotFoundError:
    print("students.txt does not exist")
    exit(1)

def find_by_lastname(lastname, grouped_by_lastname):
  students = grouped_by_lastname[lastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.grade),
                     str(student.classroom), student.tlastname, student.tfirstname]))

def find_by_lastname_bus(lastname, grouped_by_lastname):
  students = grouped_by_lastname[lastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.bus)]))

def find_by_tlastname(tlastname, grouped_by_tlastname):
  students = grouped_by_tlastname[tlastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname]))

def find_by_bus(bus, grouped_by_bus):
  students = grouped_by_bus[bus]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.grade),
                     str(student.classroom)]))

def main():
  students = parse_file("students.txt")

  grouped_by_lastname = group(students, lambda s: s.lastname)
  grouped_by_tlastname = group(students, lambda s: s.tlastname)
  grouped_by_bus = group(students, lambda s: s.bus)
  grouped_by_grade = group(students, lambda s: s.grade)

  find_by_lastname("NOVICK", grouped_by_lastname)
  find_by_lastname_bus("NOVICK", grouped_by_lastname)
  find_by_tlastname("BODZIONY", grouped_by_tlastname)
  find_by_bus("51", grouped_by_bus)

  while True:
    query = input("Enter query: ")

    if query == "q":
      break

if __name__ == "__main__":
  main()

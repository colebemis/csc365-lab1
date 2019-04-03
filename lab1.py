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

def main():
  students = parse_file("students.txt")
  grouped_by_lastname = group(students, lambda s: s.lastname)
  grouped_by_tlastname = group(students, lambda s: s.tlastname)
  grouped_by_bus = group(students, lambda s: s.bus)
  grouped_by_grade = group(students, lambda s: s.grade)
  print(grouped_by_lastname)

if __name__ == "__main__":
  main()

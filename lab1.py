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

# parses the command and calls the appropriate function
# note: quitting out of the program is handled in the main loop
# TODO: add more comprehensive error menu messages
def parse_cmd(cmd, data):
  cmd_words = cmd.split()

  query_length = len(cmd_words)
  first_word = cmd_words[0].lower().rstrip(":")
  if query_length > 2:
    third_word = cmd_words[2].lower()

  if (first_word == "student" or first_word == "s") and len(cmd):
    if query_length == 2:
      print("Querying student with last name {}".format(cmd_words[1]))
      find_by_lastname(cmd_words[1], data["lastname"])
    elif query_length == 3 and (third_word == "b" or third_word == "bus"):
      print("Querying student {} with bus info".format(cmd_words[1]))
      find_by_lastname_bus(cmd_words[1], data["lastname"])
    else:
      print("Malformatted student query")

  elif first_word == "teacher" or first_word == "t":
    print("Querying teacher {}".format(cmd_words[1]))
    find_by_tlastname(cmd_words[1], data["tlastname"])

  elif first_word == "bus" or first_word == "b":
    print("Querying bus {}".format(cmd_words[1]))
    find_by_bus(cmd_words[1], data["bus"])

  elif first_word == "grade" or first_word == "g":
    if query_length == 2:
        print("Querying grade {}".format(cmd_words[1]))
        return find_by_grade(cmd_words[1], data["grade"])
    elif query_length == 3:
        if third_word == "high" or third_word == "h":
            print("Querying highest GPA in grade {}".format(cmd_words[1]))
            return find_by_grade_high(cmd_words[1], data["grade"])
        elif third_word == "low" or third_word == "l":
            print("Querying lowest GPA in grade {}".format(cmd_words[1]))
            find_by_grade_low(cmd_words[1], data["grade"])

  elif first_word == "average" or first_word == "a":
      print("Querying the average GPA for grade {}".format(cmd_words[1]))
      find_by_grade_gpa_avg(cmd_words[1], data["grade"])

  elif first_word == "info" or first_word == "i":
    print("Querying info summary")
    summarize_by_grade(data["grade"])

  else:
    print("Unrecognized query format")


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

def find_by_grade(grd, grouped_by_grade):
  return grouped_by_grade.get(grd)

def find_by_grade_high(grd, grouped_by_grade):
  merged = []
  for i in range(int(grd) + 1):
    temp = grouped_by_grade.get(str(i))
    if temp != None:
      merged += temp
  return merged

def find_by_grade_low(grd, grouped_by_grade):
  return

def find_by_grade_gpa_avg(grd, grouped_by_grade):
  return

def summarize_by_grade(grouped_by_grade):
  return

def info():
  return

def main():
  students = parse_file("students.txt")

  grouped_by_lastname = group(students, lambda s: s.lastname)
  grouped_by_tlastname = group(students, lambda s: s.tlastname)
  grouped_by_bus = group(students, lambda s: s.bus)
  grouped_by_grade = group(students, lambda s: s.grade)

  data = {"lastname": grouped_by_lastname,
          "tlastname": grouped_by_tlastname,
          "bus": grouped_by_bus,
          "grade": grouped_by_grade}

  while True:
    query = input("Enter query: ")

    query_lower = query.lower()
    if query_lower == "q" or query_lower == "quit":
      break
    else:
      print(parse_cmd(query, data))


if __name__ == "__main__":
  main()

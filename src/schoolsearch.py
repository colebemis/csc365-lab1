from itertools import groupby
import os

class Student:
  def __init__(self, lastname, firstname, grade, classroom, bus, gpa):
    self.lastname = lastname.strip()
    self.firstname = firstname.strip()
    self.grade = grade.strip()
    self.bus = bus.strip()
    self.classroom = classroom.strip()
    self.gpa = gpa.strip()

  def __repr__(self):
    return "(" + \
      ", ".join([self.lastname, self.firstname, str(self.grade), 
                 str(self.classroom), str(self.bus), str(self.gpa)]) + ")"

class Teacher:
  def __init__(self, lastname, firstname, classroom):
    self.lastname = lastname.strip()
    self.firstname = firstname.strip()
    self.classroom = classroom.strip()

  def __repr__(self):
    return "(" + \
      ", ".join([self.lastname, self.firstname, str(self.classroom)]) + ")"

# groups by given key
def group(lst, keyfunc):
  sorted_lst = sorted(lst, key=keyfunc)
  return dict((k, list(v)) for k, v in groupby(sorted_lst, key=keyfunc))

# parses a file into a list of Student objects
def parse_students(filename):
  try:
    file = open(filename)
    students = [Student(*line.rstrip().split(",")) for line in file]
    file.close()
    return students 

  except FileNotFoundError:
    print(filename + " does not exist")
    exit(1)

# parses a file into a list of Teacher objects
def parse_teachers(filename):
  try:
    file = open(filename)
    teachers = [Teacher(*line.rstrip().split(",")) for line in file]
    file.close()
    return teachers 

  except FileNotFoundError:
    print(filename + " does not exist")
    exit(1)

# parses the command and calls the appropriate function
# note: quitting out of the program is handled in the main loop
def parse_cmd(cmd, data):
  err_msg = "Unrecognized command. Possible commands:\n" \
            "- S[tudent]: <lastname> [B[us]]\n" \
            "- T[eacher]: <lastname>\n" \
            "- B[us]: <number>\n" \
            "- G[rade]: <number> [H[igh]|L[ow]]\n" \
            "- A[verage]: <number>\n" \
            "- I[nfo]\n" \
            "- Q[uit]"
  cmd_words = cmd.split()

  query_length = len(cmd_words)
  first_word = cmd_words[0].lower().rstrip(":")
  if query_length > 2:
    third_word = cmd_words[2].lower()

  if first_word == "student" or first_word == "s":
    if query_length == 2:
      # "S[tudent]: <lastname>"
      find_by_lastname(cmd_words[1], data)
    elif query_length == 3 and (third_word == "b" or third_word == "bus"):
      # S[tudent]: <lastname> B[us]
      find_by_lastname_bus(cmd_words[1], data)
    else:
      print(err_msg)

  elif (first_word == "teacher" or first_word == "t") and query_length == 2:
    # T[eacher]: <lastname>
    find_by_tlastname(cmd_words[1], data)

  elif (first_word == "bus" or first_word == "b") and query_length == 2:
    # B[us]: <number>
    find_by_bus(cmd_words[1], data)

  elif first_word == "grade" or first_word == "g":
    if query_length == 2:
        # G[rade]: <number>
        find_by_grade(cmd_words[1], data)
    elif query_length == 3:
        if third_word == "high" or third_word == "h":
            # G[rade]: <number> H[igh]
            find_by_grade_gpa_high(cmd_words[1], data)
        elif third_word == "low" or third_word == "l":
            # G[rade]: <number> L[ow]
            find_by_grade_gpa_low(cmd_words[1], data)
        else:
          print(err_msg)
    else:
      print(err_msg)

  elif (first_word == "average" or first_word == "a") and query_length == 2:
      # A[verage]: <number>
      find_by_grade_gpa_avg(cmd_words[1], data)

  elif (first_word == "info" or first_word == "i") and query_length == 1:
    # I[nfo]
    summarize_by_grade(data)

  else:
    print(err_msg)


def find_by_lastname(lastname, data):
  if not lastname in data["students_by_lastname"]:
    return

  students = data["students_by_lastname"][lastname]

  for student in students:
    teacher = data["teachers_by_classroom"][student.classroom][0]
    print(", ".join([student.lastname, student.firstname, str(student.grade),
                     str(student.classroom), teacher.lastname, teacher.firstname]))

def find_by_lastname_bus(lastname, data):
  if not lastname in data["students_by_lastname"]:
    return

  students = data["students_by_lastname"][lastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname, student.bus]))

def find_by_tlastname(tlastname, data):
  if not tlastname in data["teachers_by_lastname"]:
    return

  teacher = data["teachers_by_lastname"][tlastname][0]
  students = data["students_by_classroom"][teacher.classroom]
  for student in students:
    print(", ".join([student.lastname, student.firstname]))

def find_by_bus(bus, data):
  if not bus in data["students_by_bus"]:
    return

  students = data["students_by_bus"][bus]
  for student in students:
    print(", ".join([student.lastname, student.firstname, student.grade,
                     student.classroom]))

def find_by_grade(grade, data):
  if not grade in data["students_by_grade"]:
    return

  students = data["students_by_grade"][grade]
  for student in students:
    print(", ".join([student.lastname, student.firstname]))

def find_by_grade_gpa_high(grade, data):
  if not grade in data["students_by_grade"]:
    return

  students = data["students_by_grade"][grade]
  best_student = students[0]
  for student in students:
    if student.gpa > best_student.gpa:
      best_student = student

  teacher = data["teachers_by_classroom"][best_student.classroom][0]
  print(", ".join([best_student.lastname, best_student.firstname, best_student.gpa,
                   teacher.lastname, teacher.firstname, student.bus]))

def find_by_grade_gpa_low(grade, data):
  if not grade in data["students_by_grade"]:
    return

  students = data["students_by_grade"][grade]
  worst_student = students[0]
  for student in students:
    if student.gpa < worst_student.gpa:
      worst_student = student
    
  teacher = data["teachers_by_classroom"][worst_student.classroom][0]
  print(", ".join([worst_student.lastname, worst_student.firstname, worst_student.gpa,
                  teacher.lastname, teacher.firstname, worst_student.bus]))

def find_by_grade_gpa_avg(grade, data):
  if not grade in data["students_by_grade"]:
    return

  students = data["students_by_grade"][grade]
  sum_gpa = 0
  for student in students:
    sum_gpa += float(student.gpa)

  print(sum_gpa/len(students))

def find_by_classroom(grade, data):
  if not grade in data["students_by_classroom"]:
    return

  students = data["students_by_classroom"][grade]
  for student in students:
    print(", ".join([student.lastname, student.firstname]))

def find_by_classroom_teacher(grade, data):
  if not grade in data["teachers_by_classroom"]:
    return

  teachers = data["teachers_by_classroom"]["grade"]
  for teacher in teachers:
    print(", ".join([teacher.lastname, teacher.firstname]))

def summarize_by_grade(data):
  for i in range(7):
    if str(i) in data["students_by_grade"]:
      students = data["students_by_grade"][str(i)]
      print("%d: %d" % (i, len(students)))
    else:
      print("%d: 0" % (i))

def main():
  students = parse_students("../list.txt")
  teachers = parse_teachers("../teachers.txt")

  data = {
    "students_by_lastname": group(students, lambda s: s.lastname),
    "students_by_bus": group(students, lambda s: s.bus),
    "students_by_grade": group(students, lambda s: s.grade),
    "students_by_classroom": group(students, lambda s: s.classroom),
    "teachers_by_lastname": group(teachers, lambda t: t.lastname), 
    "teachers_by_classroom": group(teachers, lambda t: t.classroom) 
  }

  while True:
    query = input("Enter query: ")

    query_lower = query.lower()
    if query_lower == "q" or query_lower == "quit":
      break
    else:
      parse_cmd(query, data)


if __name__ == "__main__":
  main()

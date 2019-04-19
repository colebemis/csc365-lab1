# Kellie Banzon, Cole Bemis, Tanner Larson

from itertools import groupby
from hashlib import blake2s

class Student:
  def __init__(self, lastname, firstname, grade, classroom, bus, gpa):
    self.id = generateId(lastname, firstname, grade, classroom, bus, gpa)
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

# create unique id consistent between runs
def generateId(lastname, firstname, grade, classroom, bus, gpa):
    items = [lastname.encode('utf-8'), firstname.encode('utf-8'), grade.encode('utf-8'),
             classroom.encode('utf-8'), bus.encode('utf-8'), gpa.encode('utf-8')]
    h = blake2s(digest_size=10)
    [h.update(item) for item in items]
    return h.hexdigest()

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
def parse_cmd(cmd, data, students):
  err_msg = "Unrecognized command. Possible commands:\n" \
            "- S[tudent]: <lastname> [B[us]]\n" \
            "- T[eacher]: <lastname>\n" \
            "- B[us]: <number>\n" \
            "- G[rade]: <number> [H[igh]|L[ow]|T[eacher]]\n" \
            "- C[lassroom]: <number> [T[eacher]]\n" \
            "- A[verage]: <number>\n" \
            "- I[nfo]\n" \
            "- E[nrollment]\n" \
            "- R[aw]: [grade=<number>] [bus=<number>] [teacher=<lastname>]\n" \
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
      elif third_word == "teacher" or third_word == "t":
        # G[rade]: <number> T[eacher]
        find_by_grade_teachers(cmd_words[1], data)
      else:
        print(err_msg)
    else:
      print(err_msg)

  elif first_word == "classroom" or first_word == "c":
    if query_length == 2:
      # C[lassroom]: <number>
      find_by_classroom(cmd_words[1], data)
    elif query_length == 3 and (third_word == "teacher" or third_word == "t"):
      # C[lassroom]: <number> T[eacher]
      find_by_classroom_teacher(cmd_words[1], data)

  elif (first_word == "average" or first_word == "a") and query_length == 2:
      # A[verage]: <number>
      find_by_grade_gpa_avg(cmd_words[1], data)

  elif (first_word == "info" or first_word == "i") and query_length == 1:
    # I[nfo]
    summarize_by_grade(data)

  elif (first_word == "enrollment" or first_word == "e") and query_length == 1:
    # E[nrollment]
    enrollment(data)

  elif (first_word == "raw" or first_word == "r") and 1 <= query_length <= 4 :
    try:
      filters = dict(map(lambda x: map(lambda s: s.lower(), x.split("=")), cmd_words[1:]))
      for key in filters.keys():
        if key.lower() not in ["grade", "bus", "teacher"]:
          raise Exception()
      # R[aw]: [grade=<number>] [bus=<number>] [teacher=<lastname>]
      raw(filters, data, students)
    except:
      print(err_msg) 

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

def find_by_grade_teachers(grade, data):
  if not grade in data["students_by_grade"]:
    return

  studentsInGrade = data["students_by_grade"][grade]
  studentsInGradeByClassroom = group(studentsInGrade, lambda s: s.classroom)

  for classroom in studentsInGradeByClassroom:
    teachers = data["teachers_by_classroom"][classroom]
    for teacher in teachers:
      print(", ".join([teacher.lastname, teacher.firstname]))

def find_by_classroom(classroom, data):
  if not classroom in data["students_by_classroom"]:
    return

  students = data["students_by_classroom"][classroom]
  for student in students:
    print(", ".join([student.lastname, student.firstname]))

def find_by_classroom_teacher(classroom, data):
  if not classroom in data["teachers_by_classroom"]:
    return

  teachers = data["teachers_by_classroom"][classroom]
  for teacher in teachers:
    print(", ".join([teacher.lastname, teacher.firstname]))

def summarize_by_grade(data):
  for i in range(7):
    if str(i) in data["students_by_grade"]:
      students = data["students_by_grade"][str(i)]
      print("%d: %d" % (i, len(students)))
    else:
      print("%d: 0" % (i))

def enrollment(data):
  students = data["students_by_classroom"]
  for classroom in students:
    print("%s: %d" % (classroom, len(students[classroom])))

def raw(filters, data, students):
  result = students

  for key in filters:
    if key == "grade":
      students_by_grade = group(result, lambda s: s.grade)
      try:
        result = students_by_grade[filters[key]]
      except KeyError:
        return

    elif key == "bus":
      students_by_bus = group(result, lambda s: s.bus)
      try:
        result = students_by_bus[filters[key]]
      except KeyError:
        return

    elif key == "teacher":
      teachers_by_lastname = data["teachers_by_lastname"]
      try:
        teachers = teachers_by_lastname[filters[key].upper()]
      except KeyError:
        return
      temp = []
      for teacher in teachers:
        students_by_classroom = group(result, lambda s: s.classroom)
        try:
            temp.extend(students_by_classroom[teacher.classroom])
        except KeyError:
            continue
      result = temp

    else:
      raise KeyError('Invalid filter')

  for student in result:
    # NOTE: this lookup is expensive
    teachers = data["teachers_by_classroom"][student.classroom]
    teacher_names = ""
    for i in range(len(teachers)):
      if i > 0:
        teacher_names += "& "
      teacher_names += "{}, {}".format(teachers[i].lastname, teachers[i].firstname)
    print(", ".join([student.id, student.gpa, student.grade, teacher_names, student.bus]))



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
      parse_cmd(query, data, students)


if __name__ == "__main__":
  main()

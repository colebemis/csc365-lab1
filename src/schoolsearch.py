from itertools import groupby
import os

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
    students = [Student(*line.rstrip().split(",")) for line in file]
    file.close()
    return students 

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
      # print("Querying student with last name {}".format(cmd_words[1]))
      find_by_lastname(cmd_words[1], data["lastname"])
    elif query_length == 3 and (third_word == "b" or third_word == "bus"):
      # print("Querying student {} with bus info".format(cmd_words[1]))
      find_by_lastname_bus(cmd_words[1], data["lastname"])
    else:
      print(err_msg)

  elif (first_word == "teacher" or first_word == "t") and query_length == 2:
    # print("Querying teacher {}".format(cmd_words[1]))
    find_by_tlastname(cmd_words[1], data["tlastname"])

  elif (first_word == "bus" or first_word == "b") and query_length == 2:
    # print("Querying bus {}".format(cmd_words[1]))
    find_by_bus(cmd_words[1], data["bus"])

  elif first_word == "grade" or first_word == "g":
    if query_length == 2:
        # print("Querying grade {}".format(cmd_words[1]))
        find_by_grade(cmd_words[1], data["grade"])
    elif query_length == 3:
        if third_word == "high" or third_word == "h":
            # print("Querying highest GPA in grade {}".format(cmd_words[1]))
            find_by_grade_gpa_high(cmd_words[1], data["grade"])
        elif third_word == "low" or third_word == "l":
            # print("Querying lowest GPA in grade {}".format(cmd_words[1]))
            find_by_grade_gpa_low(cmd_words[1], data["grade"])
        else:
          print(err_msg)
    else:
      print(err_msg)

  elif (first_word == "average" or first_word == "a") and query_length == 2:
      # print("Querying the average GPA for grade {}".format(cmd_words[1]))
      find_by_grade_gpa_avg(cmd_words[1], data["grade"])

  elif (first_word == "info" or first_word == "i") and query_length == 1:
    # print("Querying info summary")
    summarize_by_grade(data["grade"])

  else:
    print(err_msg)


def find_by_lastname(lastname, grouped_by_lastname):
  if not lastname in grouped_by_lastname:
    return

  students = grouped_by_lastname[lastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.grade),
                     str(student.classroom), student.tlastname, student.tfirstname]))

def find_by_lastname_bus(lastname, grouped_by_lastname):
  if not lastname in grouped_by_lastname:
    return

  students = grouped_by_lastname[lastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.bus)]))

def find_by_tlastname(tlastname, grouped_by_tlastname):
  if not tlastname in grouped_by_tlastname:
    return

  students = grouped_by_tlastname[tlastname]
  for student in students:
    print(", ".join([student.lastname, student.firstname]))

def find_by_bus(bus, grouped_by_bus):
  if not bus in grouped_by_bus:
    return

  students = grouped_by_bus[bus]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.grade),
                     str(student.classroom)]))

def find_by_grade(grd, grouped_by_grade):
  if not grd in grouped_by_grade:
    return

  students = grouped_by_grade[grd]
  for student in students:
    print(", ".join([student.lastname, student.firstname, str(student.gpa),
                     str(student.tlastname), str(student.tfirstname), str(student.bus)]))

def find_by_grade_gpa_high(grd, grouped_by_grade):
  if not grd in grouped_by_grade:
    return

  students = grouped_by_grade[grd]
  best_student = students[0]
  for student in students:
    if student.gpa > best_student.gpa:
      best_student = student
  print(", ".join([best_student.lastname, best_student.firstname, str(best_student.gpa),
                  str(best_student.tlastname), str(student.tfirstname), str(student.bus)]))

def find_by_grade_gpa_low(grd, grouped_by_grade):
  if not grd in grouped_by_grade:
    return

  students = grouped_by_grade[grd]
  worst_student = students[0]
  for student in students:
    if student.gpa < worst_student.gpa:
      worst_student = student
  print(", ".join([worst_student.lastname, worst_student.firstname, str(worst_student.gpa),
                  str(worst_student.tlastname), str(worst_student.tfirstname), str(worst_student.bus)]))

def find_by_grade_gpa_avg(grd, grouped_by_grade):
  if not grd in grouped_by_grade:
    return

  students = grouped_by_grade[grd]
  sum_gpa = 0
  for student in students:
    sum_gpa += float(student.gpa)
  print(sum_gpa/len(students))

def summarize_by_grade(grouped_by_grade):
  for i in range(7):
    if str(i) in grouped_by_grade:
      students = grouped_by_grade[str(i)]
      print(i, ": ", len(students))
    else:
      print(i, ": ", 0)

def main():
  students = parse_file("../students.txt")

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
      parse_cmd(query, data)


if __name__ == "__main__":
  main()

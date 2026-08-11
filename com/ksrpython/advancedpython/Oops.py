# student tracker:
# I want to find average marks of the students, grade and display all of them
s1 = {"roll": 102, "name": "Ankit", "marks": [82,68,91], "college": "ssn"} # initialisation of dict
s2 = {"roll": 101, "name": "Varshith", "marks": [72,68,81], "email": "anki@gmail.com", "college": "ssn", "password": "Test@123"}

s1.keys()

def average(student):
    marks = student["marks"]
    return sum(marks) / len(marks) # average formula

def grade(student):
    avg = average(student)
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "Fail"

def is_pass(student):
    if grade(student) == "Fail":
        return False
    else:
        return True


def display(student):
    print(student["roll"], ": ", student["name"], " - ", grade(student))

if __name__ == "__main__":
    display(s1)
    display(s2)
    s1["marks"] = -10 #  nonsense value, no guard
    del s2["name"]    #  KeyError waiting to happen in future operations
    # display(s1)
    # display(s2)

# i want to add two properties ie. email and college, one behaviour is_pass()


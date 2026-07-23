# Activity: College Fest Registration System
#
# Problem Statement
#
# A college is organizing two events:
#
# • 🎯 Technical Event
# • 🎭 Cultural Event
#
# The coordinator wants a program that allows users to:
#
# 1.Register students for Technical Event.
# 2.Register students for Cultural Event.
# 3.Show all participants.
# 4.Show students participating in both events.
# 5.Show students only in Technical Event.
# 6.Show students only in Cultural Event.
# 7.Show students participating in exactly one event.
# 8.Check whether a student is registered.
# 9.Remove a student from an event.
# 10.Add more students later.
# 11.Exit.

technical = set()
cultural = set()

while True:
    print("1.Register students for Technical Event.")
    print("2.Register students for Cultural Event.")
    print("3.Show all participants.")
    print("4.Show students participating in both events.")
    print("5.Show students only in Technical Event.")
    print("6.Show students only in Cultural Event.")
    print("7.Show students participating in exactly one event.")
    print("8.Check whether a student is registered.")
    print("9.Remove a student from an event.")
    print("10.Add more students later.")
    print("11.Exit.")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        name = input("Enter student's name: ")
        technical.add(name)
        print(name, "is registered for Technical Event.")
    elif choice == 2:
        name = input("Enter student's name: ")
        cultural.add(name)
        print(name, "is registered for Cultural Event.")
    elif choice == 3:
        print("All participants!!")
        # print(technical | cultural)
        print(technical.union(cultural))
    elif choice == 4:
        print("Students participating in both events.")
        print(technical.intersection(cultural))
    elif choice == 5:
        print("Students only in Technical Event.")
        print(technical)
    elif choice == 6:
        print("Students only in Cultural Event.")
        print(cultural)
    elif choice == 7:
        print("Students participating in exactly one event.")
        print(technical.symmetric_difference(cultural))
        # print(technical ^ cultural)
    elif choice == 8:
        name = input("Enter student's name: ")
        if name in technical or name in cultural:
            if name in technical:
                print(name, "is registered for Technical Event.")
            else:
                print(name, "is registered for Cultural Event.")
        else:
            print("Student",name, "is not registered ")
    elif choice == 9:
        name = input("Enter student's name: ")
        event = input("Enter event: technical or cultural: ")
        if event == "technical":
            technical.discard(name)
            print(name, "is removed from Technical Event.")
        elif event == "cultural":
            cultural.discard(name)
            print(name, "is removed from Cultural Event.")
        else:
            print("Invalid event")
    elif choice == 10:
        event = input("Enter event: technical or cultural: ")
        names = eval(input("Enter names comma saperated:"))
        print(names)
        if event == "technical":
            technical.update(names)
        elif event == "cultural":
            cultural.update(names)
        else:
            print("Invalid event")

        print("Students",names,"are registered successfully.")
    elif choice == 11:
        print("Thank you for using this program!")
        break

# Home work for students
# display total number of participants
# prevent empty names from being added
# add a menu option to clear all registrations
# Create a backup of registrations
# save the participant names in alphabatical order and display












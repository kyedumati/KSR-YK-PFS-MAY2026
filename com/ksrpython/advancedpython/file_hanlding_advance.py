import os

def read_expenses_data(file_loc):
    if os.path.exists(file_loc):
        with open(file_loc, "r") as f:
            # data = f.readlines()
            print(f.read(60))
            # for line in data:
            #     print(line)
    else:
        print("File that you are trying to access is not exist")

if __name__ == '__main__':
    file_location = "/Users/kasiyedumati/Desktop/expense.txt" # foldername/filename.txt # full qualified path# full path
    read_expenses_data(file_location)


# homework
# Create a program to take all the expenses(category, item, price, date) as an input and then save those expendes to csv file
# Write methods also to calculate final expenses catogory wise
#ex: category : food, healthcare, entertainment
# IteM: biryani, op and medicine bill for fever, movies/games

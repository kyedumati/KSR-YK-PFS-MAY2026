# write a program to find number of occurances of each letter present in the given string?
# input: australia
# a occured 3 times
# u occured 1 times
# s occured 1 time
# t occured 1 time
# r occured 1 time
# l occured 1 time
# i occured 1 time
# step1: take the string from the user
# Step2: iterate over string and get each character
# Step3: find the count of given character
# step4: if the character count is already found, we need to skip it
# Step5: print the output
# input_str = input("Enter a string to find occurance:")
# char_count = {}  # {'character': 'count'}
# for c in input_str:
#     count = input_str.count(c) # count = 3, count=1,.... count=3
#     char_count[c] = count  # if item is already there it will override count, otherwise it will add new item: char_count['a'] =3, char_count['u']=1,......char_count['a']=3
#
# print(char_count)
# # for a,b in char_count.items():# [('a',3), ('b',2), ('c',1)]
# #     print(a, "occurs", b, "times")
#
# for a,b in char_count.items(): # [('a',3), ('b',2), ('c',1)]
#     print(a,b)

# a,b = ('a', 3) # tuple unpacking


# write a program to find number of occurances of each vowel present in the given string
# input: virat kohli
# ouput: i occurs 2 times
#        a occurs 1 time
#        o occurs 1 time
# word = input("Enter a word:")
# vowels = ('a', 'e', 'i', 'o', 'u')
# d = {} # {'char': count}
# for char in word:
#     if char in vowels:
#         # d[char] = word.count(char)
#         d[char] = d.get(char,0) + 1 # d['v'] = 0 + 1 =1, d['i'] = 0+1=1,..... d['i'] = 1+1 =2
#     else:
#         continue
# print(d)


# ==================================================#
# LIBRARY MANAGEMENT SYSTEM
# ===================================================
# write a program to maintain library management system, which covers:
# 1. display books
# 2. Add book
# 3. Search book
# 4. Borrow book
# 5. Return book
# 6. Exit

library = {
    "Python": 5,
    "java": 4,
    "C": 3
}

while True:
    print("=================Library Menu=====================")
    print("1. display books")
    print("2. Add book")
    print("3. Search book")
    print("4. Borrow book")
    print("5. Return book")
    print("6. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        print("Available books:")
        print("="*30)
        for book, qty in library.items():
            print(book,"is available",qty)
    elif choice == "2":
        book = input("Enter book name: ")
        qty = int(input("Enter book quantity: "))
        library[book] = library.get(book, 0) + qty
        print(book, "added successfully")
    elif choice == "3":
        book = input("Enter book name you are searching: ")
        if book in library:
            print(book, "is available")
            print("Quantity:",library.get(book)) # library[book]
        else:
            print("Book not found")
    elif choice == "4":
        book = input("Enter book name you want to borrow: ")
        if book not in library:
            print("Book not found")
            continue
        if library[book] == 0:
            print("Book is currently unavailable")
            continue
        if book in library:
            print(book, "is available")
            library[book] = library[book] - 1
            print("Book borrowed successfully")
        else:
            print("Book not found")
    elif choice == "5":
        book = input("Enter book name you are returning: ")
        if book in library:
            library[book] = library.get(book) + 1
            print("Book returned",book,"successfully")
    elif choice == "6":
        print("Thank you for visiting library management system")
        break

# Bonus challenges
# Extend this program with below options
'''
1. delete a book from library
2. show the total number of book copies (hint: using sum(library.values())))
3. display only books with quantity greater than 0
4. find the book with highest quantity
5. track which student borrowed which book using a sendary dictionry 
   ex: borrowed = {
   "Rahul": ["Python", "Java"],
   "Anjali": ["C"]
   }
'''














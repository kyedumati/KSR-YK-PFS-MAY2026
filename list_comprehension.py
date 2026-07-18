# write a program to print first character of all the stars
# input: top_stars = ["prabhas","mahesh", "ntr", "pawan kalyan", "nani", "allu arjun", "ram charan"]
# output: first_char_list = ["p", "m", "n", "p", "n", "a", "r"]
top_stars = ["prabhas","mahesh", "ntr", "pawan kalyan", "nani", "allu arjun", "ram charan"]

# step1: first get the name of star
# step2: get the first character from star name :
# appraoch 1: using explicit list initialisation
# char_list_stars = []
# for star_name in top_stars:
#     char_list_stars.append(star_name[0])
#
# print(char_list_stars)

# approach2: using list comprehension
char_list_stars = [star_name[0] for star_name in top_stars]
print(char_list_stars)

# write a program to print even numbers from 1 to 100
even_numbers = []
for i in range(1,101):
    if i % 2 == 0:
        even_numbers.append(i)
print(even_numbers)

# list comprehension
even_numbers = [i for i in range(1,101) if i % 2 == 0]
print(even_numbers)

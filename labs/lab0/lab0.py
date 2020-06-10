########################################################################################################################
# Class: Computer Networks
# Date: 06/10/2020
# Lab0: Getting Started with Python
# Goal: Learning the basics of Python
# Student Name: Calvin Tam
# Student ID: 917902523
# Student Github Username: ctam4
# Instructions: Complete the TODO sections for each problem
# Guidelines: Read each problem carefully, and implement them correctly. Grade is based on lab correctness/completeness
#               No partial credit will be given.
#               No unit test are provided for lab #0
########################################################################################################################
import unittest # don't modify this line of code.
########################## Problem 0: Print  ###########################################################################
"""
Print your name, student id and Github username
Sample output:
Name: Jose
SID: 91744100
Github Username:
"""
name = "Calvin Tam" # TODO: your name
SID = 917902523 # TODO: your student id
git_username = "ctam4" # TODO: your github username
print("Name: " + name)
print("SID: " + str(SID))
print("Github Username: " + git_username)
print('\n')

########################## Problem 1: Processing user input ############################################################
"""
Accept two int values from the user, and print their product. If their product is greater than 500, then print their sum

Sample output:
Enter the first integer: 2
Enter the second integer: 4
Result is 8
Enter the first integer: 2
Enter the second integer: 1000
Result is 1002
"""
print("Problem 1 ********************") # problem header (don't modify)
# TODO: your code here
print("Enter the first integer: ")
first = int(input())
print("Enter the second integer: ")
second = int(input())
if first * second <= 500:
	print("Result is " + str(first * second))
else:
    print("Result is " + str(first + second))
########################## Problem 2: String Processing ##############################################################
"""
Given a string print the number of times the string "Alice" appears anywhere in the given string

For example, given the string: "Alice and Bob go to the same school. They learned today in class how to treat a lice 
infestation, and Alice found the lecture really interesting", the sample output would be: 
Alice appeared 2 times. 
"""
print("Problem 2 ********************") # problem header (don't modify)
# the given string
myString = "Alice and Bob go to the same school. They learned today in class how to treat a lice" \
           "infestation, and Alice found the lecture really interesting"
# TODO: your code here
import re
print("Alice appeared " + str(len(re.findall(r"Alice", myString))) + " times.")
########################## Problem 3: Loops ############################################################################
"""
Given a list of numbers iterate over them and output the sum of the current number and previous one.

Given: [5, 10, 24, 32, 88, 90, 100] 
Outputs: 5, 15, 34, 56, 120, 178, 190.
"""
print("Problem 3 ********************") # problem header (don't modify)
numbers = [5, 10, 24, 32, 88, 90, 100]
# TODO: your code here
result = []
for index in range(len(numbers)):
    if index is 0:
        result.append(numbers[0])
    else:
    	result.append(numbers[index - 1] + numbers[index])
print("Given: [" + ", ".join(str(x) for x in numbers) + "]")
print("Outputs: " + ", ".join(str(x) for x in result) + ".")
########################## Problem 4: Functions/Methods/Lists ##########################################################
"""
Create the method mergeOdds(l1, l2) which takes two unordered lists as parameters, and returns a new list with all the 
odd numbers from the first a second list sorted in ascending order. Function signature is provided for you below

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = [1,5,7,9,13,33] 
"""
print("Problem 4 ********************") # problem header (don't modify)
# function skeleton
def merge_odds(l1, l2):
    odds = []
    # TODO: your code here
    for x in l1 + l2:
        if x % 2 is not 0: odds.append(x)
    odds.sort()
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)
########################## Problem 5: Functions/Methods/Dictionaries ###################################################
"""
Refactor problem #4 to return a python dictionary instead a list where the keys are the index of the odd numbers in l1,
and l2, and the values are the odd numbers. 

For example: Given l1 = [2,1,5,7,9] and l2 = [32,33,13] the function will return odds = {1: [1, 33], 2: [5,13], 3: [7], 4: [9]} 
"""
print("Problem 5 ********************") # problem header
# function skeleton
def merge_odds(l1, l2):
    odds = {}
    # TODO: your code here
    odds1 = []
    odds2 = []
    for x in l1:
        if x % 2 is not 0: odds1.append(x)
    for x in l2:
        if x % 2 is not 0: odds2.append(x)
    odds1.sort()
    i1 = 0
    i2 = 0
    for index in range(max(len(odds1), len(odds2))):
        if i1 < len(odds1):
            if i2 < len(odds2):
                odds[index + 1] = [odds1[i1], odds2[i2]]
                i1 += 1
                i2 += 1
            else:
                odds[index + 1] = [odds1[i1]]
                i1 += 1
        else:
            odds[index + 1] = [odds2[i2]]
            i2 += 1
    return odds
l1 = [2,1,5,7,9]
l2 = [32,33,13]
odds = merge_odds(l1, l2)
print(odds)

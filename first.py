# #This program adds two numbers
# num1 = 1
# num2 = 2

# #Add two numbers
# sum = num1 + num2

# #Display the sum
# print("The sum of the numbers is:", sum)
# print(2+2/((2+2)+(2**2)))

# input = "Four score and seven years ago"

# print([c for c in input if c.lower() in ['a', 'e', 'i', 'o', 'u']])
# print ("hello world")
# def is_palindrome(input_string):
#     # Two variables are initialized as string date types using empty 
#     # quotes: "reverse_string" to hold the "input_string" in reverse
#     # order and "new_string" to hold the "input_string" minus the 
#     # spaces between words, if any are found.
#     new_string = ""
#     reverse_string = ""

#     # Complete the for loop to iterate through each letter of the
#     # "input_string"
#     for letter in input_string:

#         # The if-statement checks if the "letter" is not a space.
#         if letter != " ":

#             # If True, add the "letter" to the end of "new_string" and
#             # to the front of "reverse_string". If False (if a space
#             # is detected), no action is needed. Exit the if-block.
#             new_string = "".join(letter)
#             reverse_string = "".join(letter)

#     # Complete the if-statement to compare the "new_string" to the
#     # "reverse_string". Remember that Python is case-sensitive when
#     # creating the string comparison code. 
#     if new_string == reverse_string:

#         # If True, the "input_string" contains a palindrome.
#         return True
		
#     # Otherwise, return False.
#     return False


# print(is_palindrome("Never Odd or Even")) # Should be True
# print(is_palindrome("abc")) # Should be False
# print(is_palindrome("kayak")) # Should be True

def get_word(sentence, n):
	# Only proceed if n is positive 
	if n > 0:
		words = sentence[4]
		print(words)
		# Only proceed if n is not more than the number of words 
	# 	if n <= len(words):
	# 		return(words)
	# return("")

get_word("This is a lesson about lists", 4)
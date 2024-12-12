
# Tristan Fogle
# 11/20/24
# Displays a multiplication table for the number that the user inputs
def main():
 
while True: # used to let the program run more than once
 
try:
 
# Ask the user to enter an integer
 
number = int(input("Enter an integer: "))
 
if number < 0:
 
# handle negative number
 
print("This program does not handle negative numbers.")
 
else:
 
# show multiplication table
 
print(f"Multiplication table for {number}:")
 
i = 1
 
while i <= 12: # repeat until the number 12
 
print(f"{number} * {i} = {number * i}") 
 
i += 1 # add 1 to i and continue in the while loop until i is equal to 12
 
# ask to run again
 
run_again = input("Would you like to run the program again? (yes/no): ").lower()
 
if run_again == "yes" or run_again == "y":
 
continue
 
else:
 
print("Exiting program...")
 
break # Exit the loop to end the program
 
except ValueError:
 
print("Invalid input. Please enter an integer.")
main()

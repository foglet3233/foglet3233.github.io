mport requests
# function to get a random word from the WordsAPI
def get_random_word():
 
url = "https://random-word-api.herokuapp.com/word" # WordsAPI
 
response = requests.get(url)
 
 
if response.status_code == 200:
 
word = response.json()[0] # parse json from response
 
return word
 
else:
 
return None
def main():
 
word = get_random_word()
 
vowels = "aeiou"
 
 
if word: 
 
print(f"The random word is: {word}")
 
 
# if word is longer than 5 letters then say its long
 
if len(word) > 5:
 
print("Your word is pretty long.")
 
else:
 
print("Your word isn't very long.")
 
 
 
# check if the word has a vowel
 
for letter in word:
 
if letter in vowels:
 
print("The word starts with a vowel.")
 
break 
# its sloppy to put a break here but i had a hard time figuring out how to just see if the first letter is a vowel
 
else:
 
print("The word starts with a consonant.")
 
break
 
else:
 
print("Couldn't generate a random word")
# Run the main function
if __name__ == "__main__":
 
main()

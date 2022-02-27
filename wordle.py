import sys
import random

def validate_guess(guess, word_len, word_list, guessed_words):
    validated = True
    failed_reason = None
    if guess in guessed_words:
        validated = False
        failed_reason = "You've already guessed it!"
    if len(guess) != word_len:
        validated = False
        failed_reason = "Length don't match. We need a %s-letter word." % word_len
    elif guess not in word_list:
        validated = False
        failed_reason = "Word not in our dictionary."
    return validated, failed_reason

def evaluate_guess(guess, secret_word):
    eval_dict = {}
    success = False
    if guess.upper() == secret_word.upper():
        success = True
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            eval_dict[i] = (guess[i], True, True)
        elif guess[i] in secret_word:
            eval_dict[i] = (guess[i], True, False)
        else:
            eval_dict[i] = (guess[i], False, False)
    return success, eval_dict

def evaluate_letters(letter_dict, eval_dict):
    for eval in eval_dict:
        letter, contain, perfect_match = eval_dict[eval]
        if perfect_match:
            letter_dict[letter] = 'perfect'
        elif contain:
            letter_dict[letter] = 'contain'
        else:
            letter_dict[letter] = 'not_contain'
    return letter_dict

def print_visuals(visuals, letter_dict):
    for visual in visuals:
        print("")
        for i in visual:
            letter, contain, perfect_match = visual[i]
            if perfect_match:
                sys.stdout.write(u'\u001b[42;1m %s \u001b[0m' % letter)
            elif contain:
                sys.stdout.write(u'\u001b[43;1m %s \u001b[0m' % letter)
            else:
                sys.stdout.write(' %s ' % letter)
    print("\n")
    for letter in letter_dict:
        letter_status = letter_dict[letter]
        if letter_status == 'perfect':
            sys.stdout.write(u'\u001b[42;1m %s \u001b[0m' % letter)
        elif letter_status == 'contain':
            sys.stdout.write(u'\u001b[43;1m %s \u001b[0m' % letter)
        elif letter_status == 'not_contain':
            sys.stdout.write(u'\u001b[47;1m %s \u001b[0m' % letter)
        else:
            sys.stdout.write(' %s ' % letter)

# settings
word_len = 5
max_attempt = 6

# pick a secret word
word_file_name = "wordlist.txt"
word_file = open(word_file_name)
word_list = []
for l in word_file:
    word_list.append(l.strip())
word_file.close()
secret_word = random.choice(word_list)

# load dictionary
dictionary_file_name = "dictionary.txt"
dictionary_file = open(dictionary_file_name)
dictionary_dict = {}
for l in dictionary_file:
    dictionary_dict[l.strip()] = 1
dictionary_file.close()

# starting prompt
success = False
guess_count = 0
letters = 'abcdefghijklmnopqrstuvwxyz'
letter_dict = {}
for l in letters:
    letter_dict[l] = 'unknown'

print("\n#######################################")
print("I have a %s-letter word in mind. Can you guess what it is?" % word_len)
print("You have %s chances to try. Good luck!" % max_attempt)
print("#######################################\n")

guessed_words = []
visuals = []
guessed_letters = []
while not success and guess_count < max_attempt:
    guess_count += 1
    print("\nAttempt %s" % guess_count)
    my_guess = raw_input("What is your guess:")
    guess_validation = validate_guess(my_guess, word_len, dictionary_dict, guessed_words)
    if not guess_validation[0]:
        failed_reason = guess_validation[1]
        print(failed_reason)
        guess_count -= 1
        print_visuals(visuals, letter_dict)
        continue

    guessed_words.append(my_guess)

    eval_result = evaluate_guess(my_guess, secret_word)
    visuals.append(eval_result[1])
    letter_dict = evaluate_letters(letter_dict, eval_result[1])

    print_visuals(visuals, letter_dict)
    if eval_result[0]:
        success = True
        break





if success:
    print("\n\nGreat Job!")
else:
    print("\n\nSorry, the secret word is %s. Better luck next time." % secret_word)



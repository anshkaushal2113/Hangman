
import pygame
import string
import random
import requests
# from dotenv import load_dotenv
import openai
import os
import api
api_key = api.api_key

# def config():
#     load_dotenv()
# config()
pygame.init()
winHeight = 500
winWidth = 900
win = pygame.display.set_mode((winWidth, winHeight))

# initialize global variables

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)
NEW = (255,255,0)
RAINBOW = (255,137,0)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
word = ''
buttons = []
guessed = []
# hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'),
#                pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'),
#                pygame.image.load('hangman6.png')]
hangmanPics = [pygame.image.load(f'hangman{i}.png') for i in range(7)]
limbs = 0


def redraw_game_window():
    # config()
    global guessed
    global hangmanPics
    global limbs
    win.fill(RAINBOW)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1, (winWidth / 2 - length / 2, 400))

    # synonym = generate_synonym(word, api_key)
    label2 = guess_font.render("Synonym: " + synonym, 1, BLACK)
    win.blit(label2, (winWidth / 2 - label2.get_width() / 2, 450))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth / 2 - pic.get_width() / 2 + 20, 150))
    pygame.display.update()

#using external file
# def randomWord(api_key):
#     file = open('words.txt')
#     f = file.readlines()
#     i = random.randrange(0, len(f) - 1)
#     random_word = f[i][:-1]
#     # return f[i][:-1]
#     return random_word
# random_word = randomWord
#using string function
# def randomWord():
#     length = random.randint(1, 10)  # Generate a random length between 1 and 10
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for _ in range(length))
#
#
# random_word_example = randomWord()
# print(random_word_example)

#using api
import openai
import openai


def randomWord(api_key):
    openai.api_key = api_key
    prompt = "Generate a random word:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # You can choose a different supported engine
        prompt=prompt,
        max_tokens=10,  # Increase the max_tokens to ensure the model has enough space to generate shorter words
        temperature=0.7,  # Adjust temperature for randomness
        top_p=1,  # Adjust top_p for diversity
        n=5  # Number of completions to generate
    )

    # Filter out words longer than 7 letters
    randomWords = [choice['text'].strip() for choice in response.choices if len(choice['text'].strip()) <= 7]

    if randomWords:
        return randomWords[-1]  # Return the first word from the filtered list
    else:
        return None  # If no suitable word found, return None


# api_key = "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"
random_word = randomWord(api_key)
print("Random Word:", random_word)


# def randomWord(api_key):
#     openai.api_key = api_key
#     prompt = "Generate a random word:"
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo-instruct",
#         prompt=prompt,
#         max_tokens=1
#     )
#     randomWord = response.choices[0].text.strip()
#     return randomWord
#
# api_key = "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"
# random_word = randomWord(api_key)
# print("Random Word:", random_word)

# def randomWord(api_key):
#     url = f'https://api.wordnik.com/v4/words.json/randomWord?api_key={api_key}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data['word']
#     else:
#         print("Failed to fetch random word:", response.status_code)
#         return None
#
#
# # api_key = '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'
# api_key = "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"
# random_word = randomWord(api_key)
# print("Random Word:", random_word)


#hint generator
import openai


def generate_synonym(word, api_key):
    openai.api_key = api_key
    prompt = f"Find a synonym for the word '{word}'."
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",  # You can choose a different supported model
        prompt=prompt,
        max_tokens=20,  # Adjust max_tokens for the desired length of the completion
        temperature=0.7,  # Adjust temperature for randomness
        top_p=1,  # Adjust top_p for diversity
        n=1  # Number of completions to generate
    )

    synonym = response.choices[0].text.strip()  # Get the generated synonym
    return synonym


# Example usage:
# api_key = "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"
word = random_word  # Replace with your word
synonym = generate_synonym(word, api_key)
print(f"Synonym for your word is : {synonym}")


# def generate_hint(word, api_key):
#     url = f'https://api.wordnik.com/v4/word/{word.lower()}/definitions?api_key={api_key}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if data:
#             return data[0]['text']  # Return the first definition as a hint
#         else:
#             return "No hint available for this word."
#     else:
#         print("Failed to fetch hint:", response.status_code)
#         return None

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord


def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(NEW)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth / 2 - wordTxt.get_width() / 2, 295))
    win.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord(api_key)
    synonym = generate_synonym(word, api_key)


# MAINLINE


# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

# word = randomWord(api_key)
word = random_word
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))

                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()


import pygame
import string
import random
import requests
import openai  # Import only once
import api
import os


first_reset = True

pygame.init()
winHeight = 500
winWidth = 900
win = pygame.display.set_mode((winWidth, winHeight))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)
NEW = (255, 255, 0)
RAINBOW = (255, 137, 0)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load(f'hangman{i}.png') for i in range(7)]
limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs

    win.fill(RAINBOW)
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1, (winWidth / 2 - length / 2, 400))

    label2 = guess_font.render("Synonym: " + synonym, 1, BLACK)
    win.blit(label2, (winWidth / 2 - label2.get_width() / 2, 450))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth / 2 - pic.get_width() / 2 + 20, 150))
    pygame.display.update()


# def randomWord(api_key):
#     file = open('words.txt')
#     f = file.readlines()
#     i = random.randrange(0, len(f) - 1)
#     random_word = f[i][:-1]
#     return random_word
#
# def generate_synonym1(api_key):
#     file = open('synonyms.txt')
#     f = file.readlines()
#     i = random.randrange(0, len(f) - 1)
#     random_word = f[i][:-1]
#     return random_word
def randomWord(api_key, index):
    with open('words.txt') as file:
        f = file.readlines()
        random_word = f[index][:-1]
    return random_word

def generate_synonym1(api_key, index):
    with open('synonyms.txt') as file:
        f = file.readlines()
        random_word = f[index][:-1]
    return random_word

# Example usage

# word = randomWord(api_key, index)
# synonym = generate_synonym1(api_key, index)

def randomWord1(api_key):
    openai.api_key = api_key
    prompt = "Generate a random word:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=10,
        temperature=0.7,
        top_p=1,
        n=5
    )

    randomWords = [choice['text'].strip() for choice in response.choices if len(choice['text'].strip()) <= 7]

    if randomWords:
        return randomWords[-1]
    else:
        return None


def generate_synonym(word, api_key):
    openai.api_key = api_key
    prompt = f"Find a synonym for the word '{word}'."
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=20,
        temperature=0.7,
        top_p=1,
        n=1
    )

    synonym = response.choices[0].text.strip()
    return synonym


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
    global synonym
    global first_reset

    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    synonym = generate_synonym(word, api_key)
    if first_reset:
        word = randomWord1(api_key)
        synonym = generate_synonym(word, api_key)
        first_reset = False
    else:
        # word = randomWord(api_key)
        index = random.randrange(0, 10)  # Assuming 10 as the number of lines in the files
        word = randomWord(api_key,index) if first_reset else randomWord(None,index)
        synonym = generate_synonym1(api_key,index) if first_reset else generate_synonym1(None,index)


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

word = randomWord1(api_key) if first_reset else randomWord(api_key)
synonym = generate_synonym(word, api_key)

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
            if letter is not None:
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
    if first_reset:  # Check if it's the first reset
        first_reset = False  # Update first_reset to False after the first reset
pygame.quit()

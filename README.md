# Hangman
This Python script implements a Hangman game using the Pygame library. The game begins by initializing the Pygame environment and setting up the game window. Global variables are defined to hold information such as window dimensions, colors, fonts, the word to guess, buttons, guessed letters, hangman images, and limbs.

The script includes several functions:

redraw_game_window(): Updates and redraws the game window, displaying buttons, guessed letters, the hangman image, and any necessary updates.

randomWord(): Generates a random word for the game. This can be done by either reading from an external file containing a list of words, generating a random string of letters using the string module, or making an API call to fetch a random word.

generate_hint(): Utilizes an API call to generate a hint for the word, providing players with additional assistance if needed.

hang(): Checks if a guessed letter is not in the word, incrementing the hangman limbs if the guess is incorrect.

spacedOut(): Formats the display of the word to guess, showing guessed letters and underscores for unguessed letters.

buttonHit(): Checks if a button (corresponding to a letter) is clicked by the player.

end(): Ends the game, displaying either a win or lose message along with the correct word, and allowing the player to play again.

reset(): Resets the game state, allowing the player to start a new game.

The main game loop handles user input events, such as mouse clicks and key presses, to interact with the game. Players can click on buttons representing letters to guess them. The game loop continuously redraws the game window, checks for win or loss conditions, and ends the game accordingly.

Overall, this script provides a functional Hangman game with graphical interface elements using Pygame, offering players an enjoyable gaming experience of guessing words within the context of the classic Hangman game.

# File: Wordle.py

"""
Parker Watts, Aiki Takaku, Donna Kim, Mac Hartsell
Description : Write a python program that simulates the game wordle

I have completed Milestone 1 so far. I added comments to see where I added my code
"""

import random
from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR, UNKNOWN_COLOR, KEY_COLOR
from tkinter import messagebox
import emoji # need to import pip install emoji

# Selecting a random word from the dictionary and setting variables - (Parker) MILESTONE #1 
iNum = random.randrange(0, len(FIVE_LETTER_WORDS) + 1)  # Corrected range
sWordOfTheDay = FIVE_LETTER_WORDS[iNum]
bPlayGame = True

# These are default sets of variables value
iTry = 0
iGameCount = 0
iWins = 0

# Setting up result emojis
GREENBOX = (emoji.emojize(':green_square:'))
YELLOWBOX = (emoji.emojize(':yellow_square:'))
GREYBOX = (emoji.emojize(':white_large_square:'))

results = ""
resultList = ['X','X','X','X','X']

def wordle(sWordOfTheDay, bPlayGame):
    # Make a function to see if the user input is the same word - (Aiki) MILESTONE #2
    def enter_action(s):
        #set global variables to be used
        global iWins
        global iGameCount
        global iTry
        global sWordOfTheDay
        global bPlayGame
        global results
        global resultList

        user_guess = s.upper()  # Set String to uppercase

        if bPlayGame == True:
            # In the word list, or not in the word list. (Aiki) MILESTONE #2
            if user_guess.lower() in FIVE_LETTER_WORDS:

                # Checks each individual letter and adds color (Parker) MILESTONE #3
                LetterList = [sWordOfTheDay[0], sWordOfTheDay[1], sWordOfTheDay[2], sWordOfTheDay[3], sWordOfTheDay[4]]
                
                # Mark the correct letters first (Parker) MILESTONE #3
                for iCount in range(5):
                    sGuessedLetter = user_guess[iCount].lower()
                    sCorrectLetter = sWordOfTheDay[iCount]

                    if (sGuessedLetter == sCorrectLetter):
                        gw.set_square_color(gw.get_current_row(), iCount, CORRECT_COLOR)
                        LetterList.remove(sCorrectLetter)
                        # Milestone #4 Color the Correct Keys
                        gw.set_key_color(sGuessedLetter.upper(), CORRECT_COLOR)

                        #Emoji Results for green squares
                        resultList[iCount] = "G"
                
                # Mark the other letters that are not in the correct spot. First find yellow letter then letters that aren't in the word (Parker) MILESTONE #3
                for iCount in range(5):
                    sGuessedLetter = user_guess[iCount].lower()
                    sCorrectLetter = sWordOfTheDay[iCount]

                    if (sGuessedLetter in LetterList):
                        gw.set_square_color(gw.get_current_row(), iCount, PRESENT_COLOR)
                        LetterList.remove(sGuessedLetter)
                        
                        #Emoji Results for yellow squares
                        resultList[iCount] = "Y"

                        # Milestone #4 Color the Yellow Keys
                        if (gw.get_key_color(sGuessedLetter.upper()) != CORRECT_COLOR) and (gw.get_key_color(sGuessedLetter.upper()) != MISSING_COLOR) :
                            gw.set_key_color(sGuessedLetter.upper(), PRESENT_COLOR)
                    
                    elif sGuessedLetter != sCorrectLetter:
                        gw.set_square_color(gw.get_current_row(), iCount, MISSING_COLOR)
                        
                        # Milestone #4 Color the Non Correct Keys
                        if (gw.get_key_color(sGuessedLetter.upper()) != CORRECT_COLOR) and (gw.get_key_color(sGuessedLetter.upper()) != PRESENT_COLOR) :
                            gw.set_key_color(sGuessedLetter.upper(), MISSING_COLOR)
                
                # Add Emojis to results
                for iEmojiCount in range(5):
                    if resultList[iEmojiCount] == "G":
                        results += GREENBOX
                        
                    elif resultList[iEmojiCount] == "Y":
                        results += YELLOWBOX

                    elif resultList[iEmojiCount] == "X":
                        results += GREYBOX
                
                resultList = ['X','X','X','X','X']
                
                # If it is the correct word, display a message.
                if user_guess == sWordOfTheDay.upper():
                    # Add 1 to numbers of tries, wins, and game count
                    iTry = iTry + 1
                    iWins += 1
                    iGameCount += 1
                    gw.show_message("Congratulations! You guessed the entire word!")

                    # Display statistics and ask user to play again
                    bWon = True
                    showMessageBox(bWon)
                # Elif Go down a row and let user type again. 
                elif gw.get_current_row() < N_ROWS: 
                    iTry = iTry + 1
                    if gw.get_current_row() < N_ROWS - 1:
                        gw.set_current_row(gw.get_current_row() + 1)
                        results += '\n'
                    else: # Once the user reaches the max row count. End the game
                        iGameCount += 1
                        gw.show_message(f"Game over! The word was {sWordOfTheDay}.")
                        bWon = False

                        # Display statistics and ask user to play again
                        showMessageBox(bWon)
            else:
                gw.show_message("Not in word list.")
    
    #Restart the Game
    def resetGame():
        global iTry
        global results
        # Set Rows Back to White
        for row in range(N_ROWS):
            for col in range(N_COLS):
                gw.set_square_letter(row, col, " ")
                gw.set_square_color(row, col, UNKNOWN_COLOR)
        # Set each key back to grey
        for key in gw._keys.values():
            key.set_color(KEY_COLOR)
        # Set current row to 0 and message to blank
        gw.set_current_row(0)
        gw.show_message(" ")
        iTry = 0
        results = ""
    
    #Statistics Message Box Displayed AIKI 
    def showMessageBox(bWon):
        global bPlayGame
        global sWordOfTheDay
        global results

        #Show statistics for player's wordle games. Display different messages depending if they won or not
        if bWon == True: 
            messagebox.showinfo(title="Wordle", message=f"Congrats! You guessed the word with {iTry} guesses. \n\n Wins: {iWins} time(s) \n Total Games: {iGameCount} \n WinPercentage: {round(iWins/iGameCount*100, 2)}% \n\nResults: {iTry}/6 \n{results}")
        else:
            messagebox.showinfo(title="Wordle", message=f"Sorry! You weren't able to guess the word. \n\n Wins: {iWins} time(s) \n Total Games: {iGameCount} \n WinPercentage: {round(iWins/iGameCount*100, 2)}% \n\nResults: X/6 \n {results}")

        #Ask user if they want to continue to play
        response = messagebox.askquestion(title="Wordle", message="Do you want to play again?")
        
        #If yes, set new words, and play again
        if response == 'yes':
            iNum = random.randrange(0, len(FIVE_LETTER_WORDS) + 1)
            sWordOfTheDay = FIVE_LETTER_WORDS[iNum]
            print(sWordOfTheDay)
            resetGame()
        else:
            bPlayGame = False


    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)

    """ (Parker) MILESTONE #1 - Putting the the word of the day using the function Set_Square_Letter and looping through each letter
      for iCount in range(5):
        sLetter = sWordOfTheDay[iCount]
        gw.set_square_letter(N_ROWS - 6, iCount, sLetter)
    """

# Startup code
if __name__ == "__main__":
    wordle(sWordOfTheDay, bPlayGame)

# Testing to see what the random word is by printing - (Parker) MILESTONE #1
print(sWordOfTheDay)
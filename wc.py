#!/usr/bin/env python3
import random
import string
import os

def main():
    callingdir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    wordgame = Game()
    print()
    print("Welcome to my Wordle clone.")
    print()
    playagain = "y"
    mode = "regular"
    wordgame.guesscount = 0
    print("Hardmode is OFF")
    print("Type 'hard' to enter or exit hardmode.")
    playagain = input("Start new game? ('n' to exit) ")
    while playagain[0].lower() != "n":
        if playagain == "hard":
            if mode == "regular":
                print("Entering hardmode")
                mode = "hard"
            else:
                print("Exiting hardmode")
                mode = "regular"
        if playagain == "force":
            forceword = input("forceword? ")
            wordgame.new(forceword, hardmode=mode)
        else:
            wordgame.new(hardmode=mode)
            print("Type 'pass' to pass on a word.")
            # print("Type 'view' to view all guesses.")
            # print("Type 'used' to see used and unused letters.")
            print()
        over = False
        while not (wordgame.won or over):
            if wordgame.guesscount < 6:
                nextguess = input("Guess? ")
            if nextguess == "pass" or wordgame.guesscount == 6:
                print(f"It was {wordgame.answer}.")
                over = True
            else:
                wordgame.taketurn(nextguess)
                print()
                for count, guess, hint in wordgame.guesses:
                    gspaced = ''.join([f"{l:3}" for l in guess.upper()])
                    print(f"{count}: {gspaced}")
                    print(f"   {hint}")
                if not wordgame.won:
                    print()
                    print("Unused letters")
                    print("--------------")
                    print(" ".join(sorted([l.upper() for l in wordgame.unpicked])))
                    print()    
        if wordgame.won:
            print(f"You got it in {wordgame.guesscount}!")    
        print()
        if mode == "regular":
            print("Hardmode is OFF")
        else:
            print("Hardmode is ON")
        print("Type 'hard' to enter or exit hardmode.")
        playagain = input("Play again? ('n' to exit) ")
        if not playagain:
            playagain = "y"
        print()
    os.chdir(callingdir)

class Game():

    def __init__(self):
        with open("word-bank.csv") as IFH:
            self.wordbank = [w.strip() for w in IFH.readlines()]
        with open("valid-words.csv") as IFH:
            self.dictionary = [w.strip() for w in IFH.readlines()]

    def new(self, force=None, hardmode="regular"):
        if force:
            self.answer = force
        else:
            self.answer = random.choice(self.wordbank)
        self.won = False
        self.guesscount = 0
        self.guesses = []
        self.picked = set()
        self.unpicked = set(string.ascii_lowercase)
        if hardmode == "hard":
            self.hardmode = True
        else:
            self.hardmode = False
        self.prevcpos = {}
        self.prevlet = []

    def taketurn(self, guess):
        ans = self.answer
        guess = guess.lower()
        if guess not in self.dictionary:
            print()
            print("*** invalid ***")
            return
        if self.hardmode:
            for pos, ltr in self.prevcpos.items():
                if ltr != guess[pos]:
                    print()
                    print("*** invalid for hardmode ***")
                    return
            lguess = list(guess)
            for ltr in self.prevlet:
                if ltr not in lguess:
                    print()
                    print("*** invalid for hardmode ***")
                    return
                lguess.remove(ltr)
        self.guesscount += 1
        for letter in guess:
            self.picked.add(letter)
            if letter in self.unpicked:
                self.unpicked.remove(letter)
        gans = list(ans)
        hint = ['⬛️'] * 5
        cpos = []
        wpos = []
        lans = list(ans)
        self.prevcpos = {}
        self.prevlet = []
        for x in range(5):
            if guess[x] == ans[x]:
                cpos.append(x)
                self.prevcpos[x] = guess[x]
                lans.remove(guess[x])
        for x in range(5):
            if x in cpos:
                continue
            elif guess[x] in lans:
                wpos.append(x)
                self.prevlet.append(guess[x])
                lans.remove(guess[x])
        for x in range(5):
            if x in cpos:
                hint[x] = "🟩"
            elif x in wpos:
                hint[x] = "🟨"
        if hint == ['🟩'] * 5:
            self.won = True
        jhint = " ".join(hint)
        self.guesses.append((self.guesscount, guess, jhint))


if __name__ == '__main__':
    main()

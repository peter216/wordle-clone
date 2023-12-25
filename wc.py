#!/usr/bin/env python3
import random

def main():
    wordgame = Game()
    print()
    print("Welcome to my Wordle clone.")
    print("Type 'pass' to pass on a word.")
    print()
    playagain = "y"
    wordgame.guesscount = 0
    while playagain[0].lower() != "n":
        if playagain == "force":
            forceword = input("forceword? ")
            wordgame.new(forceword)
        else:
            wordgame.new()
        over = False
        while not (wordgame.won or over):
            if wordgame.guesscount < 6:
                nextguess = input("Guess? ")
            if nextguess == "pass" or wordgame.guesscount == 6:
                print(f"It was {wordgame.answer}.")
                over = True
            else:
                nexthint = wordgame.taketurn(nextguess)
                gspaced = ''.join([f"{l:3}" for l in nextguess.upper()])
                print()
                print(f"Guess {wordgame.guesscount}")
                print(nexthint)
                print(gspaced)
                #print(f" {gspaced}")
                print()
        if wordgame.won:
            print(f"You got it in {wordgame.guesscount}!")    
        print()
        playagain = input("Play again? ('n' to exit) ")
        if not playagain:
            playagain = "y"
        print()

class Game():

    def __init__(self):
        with open("word-bank.csv") as IFH:
            self.wordbank = [w.strip() for w in IFH.readlines()]
        with open("valid-words.csv") as IFH:
            self.dictionary = [w.strip() for w in IFH.readlines()]

    def new(self, force=None):
        if force:
            self.answer = force
        else:
            self.answer = random.choice(self.wordbank)
        self.won = False
        self.guesscount = 0

    def taketurn(self, guess):
        ans = self.answer
        guess = guess.lower()
        if guess not in self.dictionary:
            return ("invalid")
        self.guesscount += 1
        gans = list(ans)
        hint = ['⬛️'] * 5
        cpos = []
        wpos = []
        lans = list(ans)
        for x in range(5):
            if guess[x] == ans[x]:
                cpos.append(x)
                lans.remove(guess[x])
        for x in range(5):
            if x in cpos:
                continue
            elif guess[x] in lans:
                wpos.append(x)
                lans.remove(guess[x])
        for x in range(5):
            if x in cpos:
                hint[x] = "🟩"
            elif x in wpos:
                hint[x] = "🟨"
        if hint == ['🟩'] * 5:
            self.won = True
        return " ".join(hint)


if __name__ == '__main__':
    main()

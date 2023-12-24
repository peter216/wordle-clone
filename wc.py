#!/usr/bin/env python3
import random

def main():
    wordgame = Game()
    print()
    print("Welcome to my Wordle clone.")
    print("Use the sequence 'qqqqq' to")
    print("pass on a word.")
    print()
    playagain = "y"
    while playagain[0].lower() != "n":
        if playagain == "force":
            forceword = input("forceword? ")
            wordgame.new(forceword)
        else:
            wordgame.new()
        over = False
        while not (wordgame.won or over):
            nextguess = input("Guess? ")
            if nextguess == "qqqqq":
                print(f"It was {wordgame.answer}")
                over = True
            else:
                guessnum, nexthint = wordgame.taketurn(nextguess)
                print(f"{guessnum}: {nexthint}")
        if wordgame.won:
            print(f"You got it in {guessnum}!")    
        print()
        playagain = input("Play again? ")
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
            return (self.guesscount, "invalid")
        self.guesscount += 1
        gans = list(ans)
        hint = ['_'] * 5
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
                hint[x] = "🟢"
            elif x in wpos:
                hint[x] = "🟡"
        if hint == ['🟢'] * 5:
            self.won = True
        return (self.guesscount, " ".join(hint))


if __name__ == '__main__':
    main()

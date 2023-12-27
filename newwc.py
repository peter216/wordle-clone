#!/usr/bin/env python3
import random
import string

def main():
    wordgame = Game()
    print()
    print("Welcome to my Wordle clone.")
    print()
    playagain = "y"
    wordgame.guesscount = 0
    while playagain[0].lower() != "n":
        if playagain == "force":
            forceword = input("forceword? ")
            wordgame.new(forceword)
        else:
            wordgame.new()
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
                print()
                print("   Guesses so far")
                print("   --------------")
                print()    
                print("Used letters")
                print("--------------")
                print(" ".join(sorted([l.upper() for l in wordgame.picked])))
                print()    
                print("Unused letters")
                print("--------------")
                print(" ".join(sorted([l.upper() for l in wordgame.unpicked])))
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
        self.guesses = []
        self.picked = set()
        self.unpicked = set(string.ascii_lowercase)

    def taketurn(self, guess):
        ans = self.answer
        guess = guess.lower()
        if guess not in self.dictionary:
            return ("invalid")
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
        jhint = " ".join(hint)
        self.guesses.append((self.guesscount, guess, jhint))
        return jhint


if __name__ == '__main__':
    main()

import random
import argparse
import logging

# -------------------#
# Classes definition #
# -------------------#
class DictionaryWord():
    def __init__(self, id, word):
        self.id = id
        self.word = word

class Dice():
    def __init__(self, faces):
        self.faces = faces
    
    def roll(self):
        randomNumber = random.randint(1,self.faces)
        return randomNumber
    
class DicewareWordList():
    def __init__ (self, language):
        self.language = language
        self.loadWordsList()

    def loadWordsList (self):
        self.dictionaryWordsList = []
        wordlistFileName = "word_list_diceware_" + self.language + ".txt"

        with open(wordlistFileName) as wordsFile:
            for line in wordsFile:
                if line[0].isdigit():
                    word = line.strip().split(' ')
                    #dictionaryWordsList[word[0]] = word[1]
                    self.dictionaryWordsList.append(DictionaryWord(word[0],word[1]))

    def getRandomWord (self, wordMinimumLength):
        wordFound = False
        randomWord = ''

        while not wordFound:
            randomNumber = ''
            dice = Dice(6)
            for x in range (5):
                randomNumber = randomNumber + str(dice.roll())    

                for dictionaryWord in self.dictionaryWordsList:
                    if dictionaryWord.id == randomNumber:
                        randomWord = dictionaryWord.word
                    
                    if len(randomWord) >= wordMinimumLength:
                        wordFound = True

        return randomWord

class Passphrase():
    def __init__(self, language, numberOfWords, wordsMinimumLenght, separatorCharacter, maximumLength, specialCharacterRequired, numberRequired, upperCaseRequired, debugEnabled):
        
        if debugEnabled:            
            logging.basicConfig(level=logging.DEBUG)

        #Initialize instance variables
        self.passphrase = ''
        self.language = language
        self.numberOfWords = numberOfWords
        self.wordsMinimumLenght = wordsMinimumLenght
        self.separatorCharacter = separatorCharacter
        self.maximumLength = maximumLength
        self.specialCharacterRequired = specialCharacterRequired
        self.numberRequired = numberRequired
        self.upperCaseRequired = upperCaseRequired
        self.debugEnabled = debugEnabled

        logging.debug('Language ' + self.language)
        logging.debug('Number of words ' + str(self.numberOfWords))
        logging.debug('Word minimum length ' + str(self.wordsMinimumLenght))
        logging.debug('Separator ' + self.separatorCharacter)
        logging.debug('Passphrase maximum length ' + str(self.maximumLength))
        logging.debug('Special char required ' + str(self.specialCharacterRequired))
        logging.debug('Number required ' + str(self.numberRequired))
        logging.debug('Uppercase required ' + str(self.upperCaseRequired))
        logging.debug('Debug enabled ' + str(self.debugEnabled) )

        #Create word list
        self.dicewareWordList = DicewareWordList(language)

    # Replace one of the separators in the passphrase with a special character
    def replaceSeparatorWithSpecialChar(self):
        if len (self.passphrase) > 0:
            specialChars = '$%&!£?^§'

            #Sceglie in modo casuale il carattere speciale da usare
            randomSpecialCharPosition = random.randint (0,len(specialChars) - 1)
            specialChar = specialChars[randomSpecialCharPosition]

            #Sceglie in modo casuale quale separatore sostituire
            separators = self.passphrase.count(self.separatorCharacter)
            randomSeparator = random.randint (1, separators)

            separatorPosition = -1

            for x in range (randomSeparator):
                separatorPosition = self.passphrase.find(self.separatorCharacter, separatorPosition + 1, len(self.passphrase) - 1)

            self.passphrase = self.passphrase[:separatorPosition] + specialChar + self.passphrase[separatorPosition+1:]
        else:
            logging.error('Passphrase empty, cannot replace any separator')

    # Add a number to the passphrase in a random position
    def addNumber(self):
        if len (self.passphrase) > 0:
            randomNumberPosition = random.randint (0,len(self.passphrase) - 1)
            randomNumber = random.randint(0,9)
            self.passphrase = self.passphrase[:randomNumberPosition] + str(randomNumber) + self.passphrase[randomNumberPosition:]

    # Transform a character in the passphrase to uppercase
    def oneUppercaseChar (self):
        if len (self.passphrase) > 0:
            uppercaseSucceeded = False
            while not uppercaseSucceeded:
                uppercasePosition = random.randint(0, len(self.passphrase)) - 1

                if (self.passphrase[uppercasePosition] != self.separatorCharacter):
                    self.passphrase = self.passphrase[:uppercasePosition] + self.passphrase[uppercasePosition:uppercasePosition+1].upper() + self.passphrase[uppercasePosition+1:]
                    uppercaseSucceeded = True
    
    def generate (self):
        for x in range (self.numberOfWords):
            self.passphrase = self.passphrase + self.dicewareWordList.getRandomWord(self.wordsMinimumLenght)

            if x < self.numberOfWords - 1:
                self.passphrase = self.passphrase + self.separatorCharacter

        #Truncate the string so it doesn't exceed the maximum length
        if self.numberRequired:
            self.passphrase = self.passphrase[:self.maximumLength - 1]
        else:
            self.passphrase = self.passphrase[:self.maximumLength]

        if self.specialCharacterRequired:
            #Replace one of the separators characters with a special character
            self.replaceSeparatorWithSpecialChar()

        if self.numberRequired:
            #Add a number in a random position
            self.addNumber()

        if self.upperCaseRequired:
            #Switch to uppercase a random character
            self.oneUppercaseChar()    
# --------------------------#
# End of classes definition #
# --------------------------#

# ---------------------#
# Functions definition #
# ---------------------#
def getArguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-l", "--dictionary-language", choices=["it","en","es","fr"], required=True, help="Choose dictionary language")
    parser.add_argument("-w", "--words", type=int, default=4, help="Number of words in the passphrase")
    parser.add_argument("-m", "--word-min-length", type=int, default=5, help="Minimum length of the words")
    parser.add_argument("-x", "--maximum-length", type=int, default=99, help = "Passphrase maximum length")
    parser.add_argument("-s", "--separator-character", default='.', help="Character to use as a separator")
    parser.add_argument("-c", "--special-char-required", help="Special character required", action="store_true")
    parser.add_argument("-n", "--number-required", help= "Number required", action="store_true")
    parser.add_argument("-u", "--uppercase-required", help= "Uppercase character required", action="store_true")
    parser.add_argument("-d", "--debug-enabled", help="Enable debug mode", action="store_true")

    args = parser.parse_args()

    argumentsDict = {}

    if args.dictionary_language:
        language = args.dictionary_language
        argumentsDict["language"] = args.dictionary_language

    if args.words:
        numberOfWords = args.words
        argumentsDict["numberOfWords"] = args.words

    if args.word_min_length:
        wordsMinimumLength = args.word_min_length
        argumentsDict["wordsMinimumLength"] = args.word_min_length

    if args.separator_character:
        separatorCharacter = args.separator_character
        argumentsDict["separatorCharacter"] = args.separator_character

    if args.maximum_length:
        passphraseMaximumLength = args.maximum_length
        argumentsDict["passphraseMaximumLength"] = args.maximum_length

    argumentsDict["specialCharacterRequired"] = args.special_char_required
    argumentsDict["numberRequired"] = args.number_required
    argumentsDict["upperCaseRequired"] = args.uppercase_required
    argumentsDict["debugEnabled"] = args.debug_enabled

    return argumentsDict
# ----------------------------#
# End of functions definition #
# ----------------------------#


# -------------------------------------#
# Code executed when the script is ran #
# -------------------------------------#
arguments = getArguments()
passphrase = Passphrase(arguments.get('language'), 
                        arguments.get('numberOfWords'), 
                        arguments.get('wordsMinimumLength'), 
                        arguments.get('separatorCharacter'), 
                        arguments.get('passphraseMaximumLength'), 
                        arguments.get('specialCharacterRequired'), 
                        arguments.get('numberRequired'), 
                        arguments.get('upperCaseRequired'),
                        arguments.get('debugEnabled'))


passphrase.generate()
print(passphrase.passphrase)
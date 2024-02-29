import random
import argparse
import logging

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
            #print(f'Passphrase prima di aggiungere il numero: ',aPassphrase)
            self.passphrase = self.passphrase[:randomNumberPosition] + str(randomNumber) + self.passphrase[randomNumberPosition:]
            #print(f'Passphrase dopo aver aggiunto il numero: ',aPassphrase)

    # Transform a character in the passphrase to uppercase
    def oneUppercaseChar (self):
        if len (self.passphrase) > 0:
            #print (f'prima di oneUppercaseChar', aPassphrase)
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

        #Tronca la stringa per fare in modo che non sia più lunga della lunghezza massima
        if self.numberRequired:
            self.passphrase = self.passphrase[:self.maximumLength - 1]
        else:
            self.passphrase = self.passphrase[:self.maximumLength]

        if self.specialCharacterRequired:
            #sostituisce uno dei caratteri separatori con un carattere speciale
            self.replaceSeparatorWithSpecialChar()

        if self.numberRequired:
            #aggiunge un numero in una posizione casuale
            self.addNumber()

        if self.upperCaseRequired:
            #trasforma uno dei caratteri in maiuscolo
            self.oneUppercaseChar()
        
        




'''
def loadWordsList (wordsFileName):
    dictionaryWordsList = []
    with open(wordsFileName) as wordsFile:
        for line in wordsFile:
            if line[0].isdigit():
                word = line.strip().split(' ')
                #dictionaryWordsList[word[0]] = word[1]
                dictionaryWordsList.append(DictionaryWord(word[0],word[1]))

    return dictionaryWordsList

def loadWordsList (wordsFileName):
    dictionaryWordsList = {}
    with open(wordsFileName) as wordsFile:
        for line in wordsFile:
            if line[0].isdigit():
                word = line.strip().split(' ')
                dictionaryWordsList[word[0]] = word[1]

    return dictionaryWordsList


def rollTheDice():
    dice = Dice(6)
    return dice.roll()


def getRandomWord (wordsList, wordMinimumLength):
    wordFound = False
    randomWord = ''

    while not wordFound:
        randomNumber = ''
        dice = Dice(6)
        for x in range (5):
            randomNumber = randomNumber + str(dice.roll())    

            for dictionaryWord in wordsList:
                if dictionaryWord.id == randomNumber:
                    randomWord = dictionaryWord.word
                
                if len(randomWord) >= wordMinimumLength:
                    wordFound = True
    
    return randomWord


def replaceSeparatorWithSpecialChar(aPassphrase, separatorCharacter):
    specialChars = '$%&!£?^§'

    #Sceglie in modo casuale il carattere speciale da usare
    randomSpecialCharPosition = random.randint (0,len(specialChars) - 1)
    specialChar = specialChars[randomSpecialCharPosition]

    #Sceglie in modo casuale quale separatore sostituire
    separators = aPassphrase.count(separatorCharacter)
    randomSeparator = random.randint (1, separators)

    separatorPosition = -1

    for x in range (randomSeparator):
        separatorPosition = aPassphrase.find(separatorCharacter, separatorPosition + 1, len(aPassphrase) - 1)

    aPassphrase = aPassphrase[:separatorPosition] + specialChar + aPassphrase[separatorPosition+1:]

    return aPassphrase


def addNumber(aPassphrase):
    randomNumberPosition = random.randint (0,len(aPassphrase) - 1)
    randomNumber = random.randint(0,9)
    print(f'Passphrase prima di aggiungere il numero: ',aPassphrase)
    aPassphrase = aPassphrase[:randomNumberPosition] + str(randomNumber) + aPassphrase[randomNumberPosition:]
    print(f'Passphrase dopo aver aggiunto il numero: ',aPassphrase)
    return aPassphrase

def oneUppercaseChar (aPassphrase, theSeparatorCharacter):
    print (f'prima di oneUppercaseChar', aPassphrase)
    uppercaseSucceeded = False
    while not uppercaseSucceeded:
        uppercasePosition = random.randint(0, len(aPassphrase)) - 1

        if (aPassphrase[uppercasePosition] != theSeparatorCharacter):
            aPassphrase = aPassphrase[:uppercasePosition] + aPassphrase[uppercasePosition:uppercasePosition+1].upper() + aPassphrase[uppercasePosition+1:]
            uppercaseSucceeded = True

    return aPassphrase

def generatePassphrase (language, wordsQuantity, wordMinimumLenght, separatorCharacter, passphraseMaximumLength, specialCharacterRequired, numberRequired, upperCaseRequired):
    passphrase = ''
    dicewareWordList = DicewareWordList(language)
    
    for x in range (wordsQuantity):
        passphrase = passphrase + dicewareWordList.getRandomWord(wordMinimumLenght)
        if x < wordsQuantity - 1:
            passphrase = passphrase + separatorCharacter

    #Tronca la stringa per fare in modo che non sia più lunga della lunghezza massima
    if numberRequired:
        passphrase = passphrase[:passphraseMaximumLength - 1]
    else:
        passphrase = passphrase[:passphraseMaximumLength]

    if specialCharacterRequired:
        #sostituisce uno dei caratteri separatori con un carattere speciale
        passphrase = replaceSeparatorWithSpecialChar(passphrase, separatorCharacter)

    if numberRequired:
        #aggiunge un numero in una posizione casuale
        passphrase = addNumber(passphrase)

    if upperCaseRequired:
        #trasforma uno dei caratteri in maiuscolo
        passphrase = oneUppercaseChar(passphrase, separatorCharacter)
    
    return passphrase
'''

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

#print (getRandomWord (loadWordsList("word_list_diceware_it.txt"),5))
#print (getRandomWord(loadWordsList("word_list_diceware_it-IT-3.txt"),5))
#print (generatePassphrase("it", 4, 3, ".", 99, True, True, True))

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
'''
passphrase = Passphrase("it", 
                        4, 
                        3, 
                        ".", 
                        99, 
                        True, 
                        True, 
                        True)
'''

passphrase.generate()
print(passphrase.passphrase)

#replaceSeparatorWithSpecialChar('pippo')

'''
dwWordList = DicewareWordList('it')
print(dwWordList.getRandomWord(5))
'''

'''
arguments = getArguments()
print (arguments)
'''
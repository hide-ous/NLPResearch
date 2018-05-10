"""
Program parses through input text to identify and output the cue, claim, and source
of sentences within the input text.

---------------------------------------------
Global Variables
----------------

textInput is a string that represents the input
jsonFile represents the output file
inputFile represents the input file
sentenceList will contain a list of sentences from the input after tokenizeToSents()
             called in the program
numSentences represents the number of sentences in sentenceList
hasNSUBJ and hasCCOMP are boolean variables used to confirm that the cue has
                      outgoing edges of type NSUBJ and CCOMP
isNamedEntity is a boolean variable used to determine if the current sentence
              has a named entity in it
hasCue is a boolean variabled used when checking if the current sentence
       contains a cue
source is a spaCy token of the doc that represents the source in a sentence
claim is spaCy token of the doc that represents the claim in a sentence
cue is spaCy token of the doc that represents the cue in a sentence
claimMark is a spaCy token of the doc that represents the head of the 
          CCOMP relationship from the cue
sentenceArr is an array that is used to represent the different components
            of a sentence that is being stored in an array (direct_quote,
            sentence, source, cue, and claim)
sentencesLoopCount is an integer used to keep track of the while loop
currSentence is of doc type that represents the current sentence that is being
             parsed. It is obtained throught the sentenceList
allSentencesDict is a dictionary that will contain the array of all of the
                 sentences by appending the sentenceArr
accordingToPattern is a regex pattern used to obtain the cue, claim, and 
                   source from a sentence that has 'according to' in it
quotePattern is a regex pattern that is used obtain the direct quotes in a 
             sentence
---------------------------------------------
Functions
---------
def setInputString(inputToProcess):
    Function that sets the textInput to be an input string.
    
    inputToProcess is a string that will become the textInput

def setInputFile(fileName):
    Function that sets the textInput to be the contents of an input file.
    
    fileName is the name of the file that will be set as the textInput
    Example fileName parameter is 'input.txt'
    
def preprocess():
    Function that preprocesses the text by removing new line characters and
    periods before the '@' character
    
def createOutputFile(fileName):
    Function that creates and opens the the output file with write permissions.
    
    fileName is the name of the file that will be created for the output
    Example fileName parameter is 'output.json'
    Note the the output can be in either json or txt format

def tokenizeToSents():
    Function that tokenizes the input into sentence using nltk's
    sent_tokenize. The tokenized sentences are stored in the sentenceList and
    numSentences is set to be the length of sentenceList

def accordingToCheck():
    Function that makes the regular expression to see if 'according to' is in
    a sentence. If it is, then the cue, claim, and source will be added to
    sentenceArr, which will then be appended to allSentencesDict.

    Returns True if 'according to' was in the sentence, else returns False
    
def obtainDirectQuote():
    Function that peforms regex check to see if a direct quote is present
    in a sentence. If it is, then it adds the quote to the sentenceArr.
    Otherwise, the 'direct_quote' in the sentenceArr is set to None.

def setBoolVarsFalse():
    Function that sets all of the boolean variables to false. This is done
    within the while loop of main on each iteration of the loop so that the
    proper checks can be made.

def cueCheck(token):
    Function that checks if the token parameter is a lemma of one of the cues.
    The function is called in a for loop of all of the tokens in the sentence,
    so each word in the sentence will be checked.
    
    token is part of a doc from spaCy. The token is an individal component
    of a sentence.
    
    Returns True if a cue was found, else returns False.

def cueDependencyCheck(token):
    Function iterates through the children of the token to see if it has
    outgoing edges of type NSUBJ and CCOMP. If it does, then it sets the
    corresponding hasNSUBJ and hasCCOMP variables as true or false.
    
    token will be the cue that is inputted into the function as a token.
    
    Returns True if both hasNSUBJ and hasCCOMP is true, else returns False.

def obtainSourceAndMark(cueParam):
    Function sets the source to be the head of the NSUBJ edge from the cue and
    sets the claimMark to be the head of the CCOMP edge from the cue by 
    iterating through the children of the cue.
    
    cueParam is the cue inputted into the function as a token

def obtainClaim():
    Function obtains and sets the claim by getting the start and end index of 
    the claimMark subtre.

def twitterUsernameCheck():
    Function checks if the sentence has a twitterUsername with regex so that
    the username may be considered as a named entity. If a username is found,
    isNamedEntity will be set to true.

def obtainMultiWordEntity():
    Function obtains the complete named entity if there is a multiple word
    named entity in the sentence. The function loops through all of the named
    entities found in the sentence using spaCy's .ents method for a doc.
    If the index of the source is within the range of an entity within the
    named entities list, then the source is set to equal the complete named 
    entity.

def createSentenceArr(passedNamedEntity):
    Function creates the sentence, source, cue, and claim parts of the
    sentenceArr.
    
    passedNamedEntity is boolean variable passed into the Function to determine
    if there is a named entity in the current sentence.

def writeOutput():
    Function that dumps the allSentencesDict of all the sentenceArr's into
    the output file and then closes the output file.

def main():
    Runs the whole program to properly obtain the cue, claim, and source of
    a sentence.

"""
#import spacy
#import re
#from nltk.tokenize import sent_tokenize
#import json
#nlp = spacy.load('en_core_web_lg')

global textInput
global jsonFile
global inputFile
global sentenceList
global numSentences
global hasNSUBJ
global hasCCOMP
global isNamedEntity
global hasCue
global source
global claim
global cue
global claimMark
global sentenceArr
global sentencesLoopCount
global currSentence
global allSentencesDict

allSentencesDict = {'Sentences':[]}
accordingToPattern = re.compile('^(?P<claim>.*?)[\W]*according to[\W]*(?P<source>.*?)[\W]*$', flags=re.I|re.U)
quotePattern = re.compile(r'\“(.+?)\”')

def setInputString(inputToProcess):
    global textInput 
    textInput = inputToProcess
    return

def setInputFile(fileName):
    global inputFile
    global textInput
    inputFile = open(fileName, 'r')
    textInput = inputFile.read()
    inputFile.close()
    return
    
def preprocess():
    global textInput
    textInput = textInput.replace('\n', ' ')
    textInput = textInput.replace('.@', '@')
    return

def createOutputFile(fileName):
    global jsonFile
    jsonFile = open(fileName, 'w')
    return

def tokenizeToSents():
    global sentenceList
    global numSentences
    sentenceList = sent_tokenize(textInput)
    numSentences = len(sentenceList)
    return

def accordingToCheck():
    global sentenceArr
    global allSentencesDict
    global sentencesLoopCount
    global currSentence
    accordingToMatch = re.match(accordingToPattern, currSentence)
    if accordingToMatch != None:
        sentenceArr['sentence'] = currSentence
        sentenceArr['source'] = accordingToMatch.group('source')
        sentenceArr['cue'] = 'according to'
        sentenceArr['claim'] = accordingToMatch.group('claim')
        allSentencesDict['Sentences'].append(sentenceArr)
        sentencesLoopCount += 1
        return True
    else:
        return False

def obtainDirectQuote():
    global currSentence
    quoteMatch = re.match(quotePattern, currSentence)
    if quoteMatch != None:
        sentenceArr['direct_quote'] = quoteMatch.string
    else:
        sentenceArr['direct_quote'] = None

def setBoolVarsFalse():
    global hasNSUBJ
    global hasCCOMP
    global isNamedEntity
    global hasCue
    hasNSUBJ = False
    hasCCOMP = False
    isNamedEntity = False
    hasCue = False
    return

def cueCheck(token):
    if (token.pos_ == 'VERB' and (token.lemma_ == 'say' or token.lemma_ == 'report'
                              or token.lemma_ == 'tell' or token.lemma_ == 'told'
                              or token.lemma_ == 'observe' or token.lemma_ == 'state'
                              or token.lemma_ == 'state' or token.lemma_ == 'accord'
                              or token.lemma_ == 'insist' or token.lemma_ == 'insist'
                              or token.lemma_ == 'assert' or token.lemma_ == 'claim'
                              or token.lemma_ == 'maintain' or token.lemma_ == 'explain'
                              or token.lemma_ == 'deny' or token.lemma_ == 'learn'
                              or token.lemma_ == 'admit' or token.lemma_ == 'discover'
                              or token.lemma_ == 'forget' or token.lemma_ == 'forgot'
                              or token.lemma_ == 'think' or token.lemma_ == 'thought'
                              or token.lemma_ == 'predict' or token.lemma_ == 'suggest'
                              or token.lemma_ == 'guess' or token.lemma_ == 'believe'
                              or token.lemma_ == 'doubt' or token.lemma_ == 'wonder'
                              or token.lemma_ == 'ask' or token.lemma_ == 'hope'
                              or token.lemma_ == 'sense' or token.lemma_ == 'hear'
                              or token.lemma_ == 'feel')):
        return True
    else:
        return False

def cueDependencyCheck(token):
    global hasNSUBJ
    global hasCCOMP
    for child in token.children:
        if (child.dep_ == 'nsubj'):
            hasNSUBJ = True
        if (child.dep_ == 'ccomp'):
            hasCCOMP = True
    if (hasNSUBJ and hasCCOMP):
        return True
    else:
        return False

def obtainSourceAndMark(cueParam):
    global source
    global claimMark
    global isNamedEntity
    global cue
    for child in cue.children:
        if (child.dep_ == 'nsubj'):
            source = child

            if (source.ent_type != 0):
                isNamedEntity = True
        if (child.dep_ == 'ccomp'):
            claimMark = child
    return

def obtainClaim():
    global claim
    children = list(claimMark.subtree)
    childrenIndices = [child.i for child in children]
    claimStart = min(childrenIndices)
    claimEnd = max(childrenIndices) + 1
    claim = currSentenceDoc[claimStart:claimEnd]
    return

def twitterUsernameCheck():
    global currSentence
    global isNamedEntity
    global source
    if (not isNamedEntity):
        usernamePattern = re.compile('@[\w+]*')
        usernameMatch = re.findall(usernamePattern, currSentence)
        for entity in list(match):
            if (source.text == entity):
                isNamedEntity = True
    return

def obtainMultiWordEntity():
    global source
    entityLoopCount = 0
    numEntities = len(currSentenceDoc.ents)
    foundEntityGroup = False
    while entityLoopCount < numEntities and not foundEntityGroup:
        currEntity = currSentenceDoc.ents[entityLoopCount]
        
        if (source.i >= currEntity.start and source.i <= currEntity.end):
            source = currEntity
            foundEntityGroup = True
    entityLoopCount += 1
    return

def createSentenceArr(passedNamedEntity):
    global sentenceArr
    global currSentence
    if passedNamedEntity:
        sentenceArr['sentence'] = currSentenceDoc.text
        sentenceArr['source'] = source.text
        sentenceArr['cue'] = cue.text
        sentenceArr['claim'] = claim.text
    else:
        sentenceArr['sentence'] = currSentence
        sentenceArr['source'] = None
        sentenceArr['cue'] = None
        sentenceArr['claim'] = None
    return

def writeOutput():
    global jsonFile
    print(json.dumps(allSentencesDict, indent=4))
    jsonFile.write(json.dumps(allSentencesDict, indent=4))
    jsonFile.close()

def main():
    global sentenceArr
    global hasCue
    global currSentence
    global sentencesLoopCount
    global cue
    global currSentenceDoc
    
    setInputFile('input.txt')
    preprocess()
    createOutputFile('json_output.json')
    tokenizeToSents()
    
    sentencesLoopCount = 0
    while sentencesLoopCount < numSentences:
        sentenceArr = {}
        currSentence = sentenceList[sentencesLoopCount]
        accordingToMatch = re.match(accordingToPattern, currSentence)
        obtainDirectQuote()
        if not accordingToCheck():
            currSentenceDoc = nlp(currSentence)
            setBoolVarsFalse() 
            for token in currSentenceDoc: 
                hasCue = cueCheck(token)
                if hasCue:
                    if cueDependencyCheck(token):
                        cue = token
                        obtainSourceAndMark(cue)
                        obtainClaim()
                        twitterUsernameCheck()
                        if (isNamedEntity):
                            obtainMultiWordEntity()
                        createSentenceArr(isNamedEntity)
            allSentencesDict['Sentences'].append(sentenceArr)
            sentencesLoopCount += 1
    writeOutput()
    return

if __name__ == "__main__":
    main()
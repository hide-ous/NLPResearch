# -*- coding: utf-8 -*-

import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'I guess, since FBI claims it couldn’t match Tsarnaev, we can assume ...')

count = 0;
innerCount = 0;
hasNSUBJ = False;
hasCCOMP = False;
for token in doc:

    claimMark = doc[0]; #just declaring claimMark to be some random part of sentence
    cue = doc[0]
    #getting the cue from a sentence
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
        
        #check if the potential cue has a NSUBJ and a CCOMP
        for child in doc[count].children:
            if (child.dep_ == 'nsubj'):
                hasNSUBJ = True;
            if (child.dep_ == 'ccomp'):
                hasCCOMP = True;
        
        #only taking the cue if it has an NSUBJ and CCOMP child
        if (hasNSUBJ and hasCCOMP):
            cue = doc[count];
            print('The cue is ' + token.text)
        
        #obtaining source and mark of the claim
        for child in cue.children:
            innerCount += 1;
            if (child.dep_ == 'nsubj'):
                print('The source is ' + child.text)
            if (child.dep_ == 'ccomp'):
                claimMark = child;
                
                
        
        print('The claim is ')
        for child in claimMark.lefts:
            print(child.text + ' ')
        print(claimMark.text + ' ')
        for child in claimMark.rights:
            print(child.text + ' ')
        
    count += 1;


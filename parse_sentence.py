# -*- coding: utf-8 -*-

import spacy

nlp = spacy.load('en_core_web_lg')
doc = nlp(u'I guess, since FBI claims it couldn’t match Tsarnaev, we can assume ...')

hasNSUBJ = False
hasCCOMP = False
isNamedEntity = False

claimLeft = 0
claimLeftEnd = 0
claimRightStart = 0
claimRightEnd = 0

claimMark = doc[0]
cue = doc[0]

for token in doc:

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
        for child in token.children:
            if (child.dep_ == 'nsubj'):
                hasNSUBJ = True
            if (child.dep_ == 'ccomp'):
                hasCCOMP = True
        
        #only taking the cue if it has an NSUBJ and CCOMP child
        if (hasNSUBJ and hasCCOMP):
            cue = token
        
            #obtaining source and mark of the claim
            for child in cue.children:
                if (child.dep_ == 'nsubj' and child.ent_type != 0):
                    isNamedEntity = True
                    source = child
                if (child.dep_ == 'ccomp'):
                    claimMark = child
                
                
        
            #if the potential source found is a named entity, then we can proceed
            #with the processing
            if (isNamedEntity):
                print('The source is ' + source.text)
                print('The cue is ' + cue.text)
        
                children = list(claimMark.subtree)
                childrenIndices = [child.i for child in children]
                claimStart = min(childrenIndices)
                claimEnd = max(childrenIndices) + 1
                claim = doc[claimStart:claimEnd]
                
                print('The claim is ' + claim.text)
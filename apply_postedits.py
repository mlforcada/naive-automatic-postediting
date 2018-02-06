#!/usr/bin/env python3

import argparse, subprocess, itertools, pprint, sys
import collections
from collections import Counter
import re # regular expressions
from streamparser.streamparser import parse
import csv

def analyzeText(text, locPair, pair, directory=None):
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    if directory:
        p2 = subprocess.Popen(['lt-proc', '-a', './{2}-{3}.automorf.bin'.format(locPair[0], locPair[1], pair[0], pair[1])], stdin=p1.stdout, stdout=subprocess.PIPE, cwd=directory)
    else:
        p2 = subprocess.Popen(['lt-proc', '-a', '/usr/local/share/apertium/apertium-{0}-{1}/{2}-{3}.automorf.bin'.format(locPair[0], locPair[1], pair[0], pair[1])], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    return p2.communicate()[0].decode('utf-8').strip()

def translateText(text, pair, directory=None):
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    if directory:
        p2 = subprocess.Popen(['apertium', '-d', directory, '{0}-{1}'.format(*pair)], stdin=p1.stdout, stdout=subprocess.PIPE)
    else:
        p2 = subprocess.Popen(['apertium', '{0}-{1}'.format(*pair)], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    return p2.communicate()[0].decode('utf-8').strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apertium translation parts')
    parser.add_argument('sourceLanguage', help='source language')
    parser.add_argument('targetLanguage', help='target language')
#    parser.add_argument('text', help="input text", metavar='S')
    parser.add_argument('-m', '--maxSourceLength', help='maximum length of whole-word subsegments (for source text)', type=int, default=5)
    parser.add_argument('-M', '--maxTranslationLength', help='maximum length of whole word subsegments (for translated text)', type=int, default=5)
    parser.add_argument('-d', '--directory', help='directory of Apertium language pair', default=None)
    parser.add_argument('-t', '--table', help='prints reference table of characters', action='store_true', default=False)
    parser.add_argument('-i', '--ignoreCase', help='ignore case in analyzations (use lower always)', action='store_true', default=False)
    parser.add_argument('-o', '--operators', help='Postediting operator file')
    parser.add_argument('-v', help='Verbose Mode', action='store_true')
    parser.add_argument('--go', help='To patch only grounded mismatches', action='store_true')
    parser.add_argument('-f', '--source_texts', help='source file', default=None)
    
    args = parser.parse_args()
    verbose = args.v

    grounded = args.go 

    operators = args.operators
    pair = (args.sourceLanguage, args.targetLanguage)


    opC=set()
    with open(operators, 'r') as f:
      reader = csv.reader(f)
      for row in reader:
         if grounded :
            test=(row[1].split())[0]
            if (row[1].split())[0]==(row[2].split())[0] and (row[1].split())[len(row[1].split())-1]==(row[2].split())[len(row[2].split())-1] :
               opC.add((row[0],row[1],row[2]))         
      #                if verbose:
      #                   print(row[0]+"\t"+row[1]+"\t"+row[2]+"\n")
         else :
            opC.add((row[0],row[1],row[2]))
            if verbose:
               print(row[0]+"\t"+row[1]+"\t"+row[2]+"\n")
    f.close()



#    sourceText = args.text.lower() if args.ignoreCase else args.text #S
    if args.source_texts==None :
       f=sys.stdin
    else : 
       f=open(args.source_texts, 'r')
    sen_num=0
    
    for sourceText in f:
            sourceText=sourceText.strip()
            sen_num=sen_num+1
            analyzedSourceText = analyzeText(sourceText, pair, pair, directory=args.directory)
            analyzedSourceUnits = list(parse(analyzedSourceText, withText=True))

            Correspondence = collections.namedtuple('Correspondence', ['s', 't', 'i', 'j', 'k', 'l'])
            correspondences = []

            analyzedSourceUnitsSubsegments = []

            for length in range(1, args.maxSourceLength + 1):
                for startIndex in range(0, len(analyzedSourceUnits) - length + 1):
                    lastIndex = startIndex + length - 1 
                    analyzedSourceUnitsSubsegments.append((analyzedSourceUnits[startIndex:lastIndex+1], startIndex, lastIndex)) #s, i, j (analyzed units forms of them)

            translatedText = translateText(sourceText, pair, directory=args.directory)
            if args.ignoreCase:
                translatedText = translatedText.lower()
            analyzedTranslation = analyzeText(translatedText, pair, pair[::-1], directory=args.directory)
            analyzedTranslationUnits = list(parse(analyzedTranslation, withText=True))
            translatedText=re.sub("\s+", " ", translatedText) # This substitutes multiple whitespace by a single space

            analyzedTranslationUnitsSubsegments = []
            for length in range(1, args.maxTranslationLength + 1):
                for startIndex in range(0, len(analyzedTranslationUnits) - length + 1):
                    lastIndex = startIndex + length - 1
                    analyzedTranslationUnitsSubsegments.append((analyzedTranslationUnits[startIndex:lastIndex+1], startIndex, lastIndex))

            #pprint.pprint(analyzedSourceUnits)

            translatedTextSubsegements = []
            for analyzedSourceUnitsSubsegment, startIndexInUnits, lastIndexInUnits in analyzedSourceUnitsSubsegments:
                sourceTextSubsegment = '' #s
                for i, (analyzedSourceUnitPreceedingText, analyzedSourceLexicalUnit) in enumerate(analyzedSourceUnitsSubsegment):
                    sourceTextSubsegment += (analyzedSourceUnitPreceedingText if i != 0 else '') + analyzedSourceLexicalUnit.wordform

                startIndexInSourceText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedSourceUnits[:startIndexInUnits]))) + len(analyzedSourceUnitsSubsegment[0][0]) #i
                lastIndexInSourceText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedSourceUnits[:lastIndexInUnits+1]))) - 1 #j

                if args.ignoreCase:
                    sourceTextSubsegment = sourceTextSubsegment.lower()

                translatedTextSubsegment = translateText(sourceTextSubsegment, pair, directory=args.directory) #t
                if args.ignoreCase:
                    translatedTextSubsegment = translatedTextSubsegment.lower()
                analyzedTranslatedTextSubsegment = analyzeText(translatedTextSubsegment, pair, pair[::-1], directory=args.directory)
                analyzedTranslatedTextSubsegmentUnits = list(parse(analyzedTranslatedTextSubsegment, withText=True))
                #pprint.pprint(analyzedTranslatedTextSubsegmentUnits)

                subsegmentMatches = list(filter(lambda x: list(map(lambda y: str(y[1]), x[0])) == list(map(lambda z: str(z[1]), analyzedTranslatedTextSubsegmentUnits)) , analyzedTranslationUnitsSubsegments))
                if subsegmentMatches:
                    startIndexInTranslatedText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedTranslationUnits[:subsegmentMatches[0][1]]))) + len(subsegmentMatches[0][0][0][0]) #k
                    lastIndexInTranslatedText = sum(list(map(lambda x: len(x[0]) + len(x[1].wordform), analyzedTranslationUnits[:subsegmentMatches[0][2]+1]))) - 1 #l

                    correspondences.append(Correspondence(
                        s=sourceTextSubsegment, 
                        t=translatedTextSubsegment,
                        i=startIndexInSourceText, 
                        j=lastIndexInSourceText, 
                        k=startIndexInTranslatedText, 
                        l=lastIndexInTranslatedText
                    ))

            #print('Source text: %s' % repr(sourceText))
            #print('Translated text: %s\n' % repr(translatedText))
            opB=set()
            for s,t,i,j,k,l in correspondences :
                        t=re.sub("\s+", " ", t) # This substitutes multiple whitespace by a single space
                        opB.add((s,t))
            if verbose :
                        print("source and target:")
                        pprint.pprint(opB)


            opD=set()
            for s,t in opB :
                        for source, hyp, ref in opC :
                           if s==source :
                             opD.add((s,t,ref))
            tokT = translatedText.split()
#            if verbose :
#               print(translatedText)
            print("[",sen_num,"]", sourceText)
            print("@ ",translatedText)
            results=Counter() #empty counter container for all postedits of this sentence
            for s,t,ref in opD :
                toktprime = ref.split()
                tokt = t.split()       
                if verbose :
        #           print(translatedText)
                    print("s=",s)
                    print("t=",tokt)
                    print("t'=",toktprime)

                res = [(tokt,i) for i in range(len(tokT)) if tokT[i:i+len(tokt)] == tokt]


                if verbose :	
                    print(res) # List of successful post-editing operations
                    print("----------") 



                for (x,j) in res : # each postedit is applied only once
                   posteditedlist=tokT[0:j]+toktprime+tokT[j+len(tokt):]
        #           if verbose :
        #              print(posteditedlist)   
                   postedited=""
                   for element in posteditedlist :
                      postedited=postedited+" "+element
                   results[postedited.strip()] += 1
            for p in results :
                print(p,results[p])

        #           print(translatedText[0:pos-1]+"\t" + ref)
        #           print((translatedText[0:pos-1] + ref).split())

    

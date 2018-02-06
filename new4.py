import argparse 
from lib.edwf2 import EDWF # Modified version of Pankaj's library
from lib.phr_ex import phrase_extraction # code lifted from http://stackoverflow.com/questions/25109001/phrase-extraction-algorithm-for-statistical-machine-translation

from lib.explain2 import getCorrespondences
import pprint # for pretty printing of correspondences
import re # regular expressions

parser = argparse.ArgumentParser(description='Apertium translation parts')
parser.add_argument('sourceLanguage', help='source language')
parser.add_argument('targetLanguage', help='target language')

parser.add_argument('text_in_fn', help='Source text, input') 
parser.add_argument('hyp_in_fn', help='Hypothesis file, input')
parser.add_argument('ref_in_fn', help='Postedited output file, input')
parser.add_argument('hyp_out_fn', help='Hypothesis file, output') # these may have to be removed later
parser.add_argument('ref_out_fn', help='Postedited output file, output') # these may have to be removed later
parser.add_argument('fmt', help='Fuzzy Match Threshold', type=float)
parser.add_argument('-v', help='Verbose Mode', action='store_true')

parser.add_argument('-m', '--maxSourceLength', help='maximum length of whole-word subsegments (for source text)', type=int, default=5)
parser.add_argument('-M', '--maxTranslationLength', help='maximum length of whole word subsegments (for translated text)', type=int, default=5)
parser.add_argument('-d', '--directory', help='directory of Apertium language pair', default=None)
parser.add_argument('-t', '--table', help='prints reference table of characters', action='store_true', default=False)
parser.add_argument('-i', '--ignoreCase', help='ignore case in analyses (use lower always)', action='store_true', default=False)

args = parser.parse_args()
verbose = args.v
# DEBUGGING:
# print(args.directory);


# open output files
hyp_out = open(args.hyp_out_fn, 'w')
ref_out = open(args.ref_out_fn, 'w')


with open(args.text_in_fn, "r") as text_in, open(args.hyp_in_fn, "r") as hyp_in, open(args.ref_in_fn,"r") as ref_in : 
    for s, x, y in zip(text_in, hyp_in, ref_in):  
           s_tuple=tuple((s.strip()).split())
           x_tuple=tuple((x.strip()).split())
           y_tuple=tuple((y.strip()).split()) 
           wf=EDWF(x_tuple,y_tuple)
           distance=wf.get_distance()*1.0
           if verbose :
              print ("==============================")
              print (x.strip(),y.strip(),distance,args.fmt)          
              print (len(x_tuple), len(y_tuple), 1.0-distance/max(len(x_tuple),len(y_tuple)))
           if 1.0-distance/max(len(x_tuple),len(y_tuple))>1.0*args.fmt :
             hyp_out.write(x.strip()+"\n")  
             ref_out.write(y.strip()+"\n")  
             if verbose :
                print (x.strip()+"\n")  
                print (y.strip()+"\n") 
             alignment = wf.get_alignment()
             if verbose :
               print(alignment)
             opA=set()
#             print(phrase_extraction(x.strip(),y.strip(),alignment))
             for pair,hyp,ref in phrase_extraction(x.strip(),y.strip(),alignment) :
               hyp=hyp.strip()
               ref=ref.strip()
               if verbose :
                   print( "('" , pair , "')=('", hyp, "','", ref,"')")
               opA.add((hyp,ref))
             if verbose : 
                 print ("==================================")
                 print("target side:")
                 pprint.pprint(opA)
             correspondences=getCorrespondences(args.sourceLanguage,args.targetLanguage,args.ignoreCase,args.maxSourceLength,args.directory,args.maxTranslationLength,s.strip())
#             pprint.pprint(correspondences)
             opB=set()
             for s,t,i,j,k,l in correspondences :
                t=re.sub("\s+", " ", t) # This substitutes multiple whitespace by a single space
                opB.add((s,t))
             if verbose :
                print("source and target:")
                pprint.pprint(opB)
                print("joined:")
             posteditops=list()
             for s,t in opB :
                for hyp, ref in opA :
                   if t==hyp :
                     posteditops.append((s,t,ref))
                     if verbose :
                        print( "('", s ,"','", "')('",  t ,"','","')('",  ref ,"')" )
           if verbose :
             print ("==================================")
           

text_in.close()
hyp_in.close()
ref_in.close()
hyp_out.close()
ref_out.close()
exit()




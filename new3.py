import argparse #, sys 
#from itertools import zip
from lib.edwf2 import EDWF # Modified version of Pankaj's library
from lib.phr_ex import phrase_extraction # code lifted from http://stackoverflow.com/questions/25109001/phrase-extraction-algorithm-for-statistical-machine-translation
#reload(sys)
#sys.setdefaultencoding('utf-8')

# Open 4 files, two input and two output
parser = argparse.ArgumentParser(description='Selecting pairs')
parser.add_argument('hyp_in_fn', help='Hypothesis file, input')
parser.add_argument('ref_in_fn', help='Postedited output file, input')
parser.add_argument('hyp_out_fn', help='Hypothesis file, output')
parser.add_argument('ref_out_fn', help='Postedited output file, output')
parser.add_argument('fmt', help='Fuzzy Match Threshold', type=float)
parser.add_argument('-v', help='Verbose Mode', action='store_true')
args = parser.parse_args()
verbose = args.v



# open output files
hyp_out = open(args.hyp_out_fn, 'w')
ref_out = open(args.ref_out_fn, 'w')


with open(args.hyp_in_fn, "r") as hyp_in, open(args.ref_in_fn,"r") as ref_in: 
    for x, y in zip(hyp_in, ref_in):  
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
             print (x.strip()+"\n")  
             print (y.strip()+"\n") 
             alignment = wf.get_alignment()
             print(alignment)
#             print(phrase_extraction(x.strip(),y.strip(),alignment))
             for pair,sz,tz in phrase_extraction(x.strip(),y.strip(),alignment) :
               print("(", pair, ")=(", sz, ",", tz,")")
             print ("==================================")
           
           print ("==================================")

hyp_in.close()
ref_in.close()
hyp_out.close()
ref_out.close()
exit()


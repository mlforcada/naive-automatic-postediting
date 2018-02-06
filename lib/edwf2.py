#! /bin/env python
#
## Python Implementation of Wagner Fischer algorithm for finding edit distance between two sentences.
## Author: pankajksharma
## Recent changes 20150528

import numpy

class EDWF(object):
 def __init__(self, source, target):
  self._src = source
  self._tgt = target
  self.sl, self.tl = len(self._src)+1, len(self._tgt)+1
  self.matd = numpy.zeros((self.sl, self.tl),dtype=int) # Pankaj had no type here, defaulting to numpy.float64
  self.mati = numpy.zeros((self.sl, self.tl),dtype=int) # Pankaj had no type here, defaulting to numpy.float64
  self.matj = numpy.zeros((self.sl, self.tl),dtype=int) # Pankaj had no type here, defaulting to numpy.float64

 def get_distance(self):

  for i in range(self.sl):
            self.matd[i,0] = i
            self.mati[i,0] = i-1
            self.matj[i,0] = 0
  
  for j in range(self.tl):
            self.matd[0,j] = j
            self.mati[0,j] = j-1
            self.matj[0,j] = 0

  for j in range(1, self.tl):
   for i in range(1, self.sl):
    if self._src[i-1] == self._tgt[j-1]:
     self.matd[i,j] = self.matd[i-1,j-1]
     self.mati[i,j] = i-1
     self.matj[i,j] = j-1
                                        
    else:
     self.matd[i,j] = self.matd[i-1,j-1]+1
     self.mati[i,j] = i-1
     self.matj[i,j] = j-1
     if self.matd[i,j-1]+1<self.matd[i,j] :
        self.matd[i,j]=self.matd[i,j-1]+1
        self.mati[i,j]=i
        self.matj[i,j]=j-1
     if self.matd[i-1,j]+1<self.matd[i,j] :
        self.matd[i,j]=self.matd[i-1,j]+1
        self.mati[i,j]=i-1
        self.matj[i,j]=j
                         #min([mat[i-1,j]+1, mat[i, j-1]+1, mat[i-1, j-1]+1]) only for edit distance

  return self.matd[self.sl-1, self.tl-1]


 def get_alignment(self):
   alignment=list()
   i=len(self._src)-1
   j=len(self._tgt)-1
   if (self._src[i]==self._tgt[j]) :
	    alignment.append((i,j))
   while i!=0 and j!=0 :
      i,j=self.mati[i,j],self.matj[i,j]
      if self._src[i]==self._tgt[j] :
         alignment.append((i,j))
   return alignment

 
 

  




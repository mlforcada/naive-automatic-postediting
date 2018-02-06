def phrase_extraction(srctext, trgtext, alignment):
    """
    Phrase extraction algorithm.
    """
    def extract(f_start, f_end, e_start, e_end):
        if f_end < 0:  # 0-based indexing.
            return {}
        # Check if alignement points are consistent.
        for e,f in alignment:
            if ((f_start <= f <= f_end) and
               (e < e_start or e > e_end)):
                return {}

        # Add phrase pairs (incl. additional unaligned f)
        # Remark:  how to interpret "additional unaligned f"?
        phrases = set()
        fs = f_start
        # repeat-
        while True:
            fe = f_end
            # repeat-
            while True:
                # add phrase pair ([e_start, e_end], [fs, fe]) to set E
                # only if it contains unaligned words in either side 20150601
                # Need to +1 in range  to include the end-point.
                src_phrase = " ".join(srctext[i] for i in range(e_start,e_end+1))
                trg_phrase = " ".join(trgtext[i] for i in range(fs,fe+1))
                valid_src = False 
                for i in range(e_start,e_end+1):
                   valid_src = valid_src or (not(i in e_aligned))
 
                valid_tgt = False 
                for i in range(fs,fe+1):
                   valid_tgt = valid_tgt or (not(i in f_aligned))
 
                # Include more data for later ordering.
                if valid_src or valid_tgt :
                     phrases.add(((e_start, e_end+1,fs,fe+1), src_phrase, trg_phrase))  # adding target info 20150601
                fe += 1 # fe++
                # -until fe aligned or out-of-bounds
                if fe in f_aligned or fe == trglen:
                    break
            fs -=1  # fe--
            # -until fs aligned or out-of- bounds
            if fs in f_aligned or fs < 0:
                break
        return phrases


    # Calculate no. of tokens in source and target texts.
    srctext = srctext.split()   # e
    trgtext = trgtext.split()   # f
    srclen = len(srctext)       # len(e)
    trglen = len(trgtext)       # len(f)
    # Keeps an index of which source/target words are aligned.
    e_aligned = [i for i,_ in alignment]
    f_aligned = [j for _,j in alignment]

    bp = set() # set of phrase pairs BP
    # for e start = 1 ... length(e) do
    # Index e_start from 0 to len(e) - 1
    for e_start in range(srclen):
        # for e end = e start ... length(e) do
        # Index e_end from e_start to len(e) - 1
        for e_end in range(e_start, srclen):
            # // find the minimally matching foreign phrase
            # (f start , f end ) = ( length(f), 0 )
            # f_start in [0, len(f) - 1]; f_end in [0, len(f) - 1]
            f_start, f_end = trglen-1 , -1  #  0-based indexing
            # for all (e,f) in A do
            for e,f in alignment:
                # if e start <= e <= e end then
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)
            # add extract (f start , f end , e start , e end ) to set BP
            phrases = extract(f_start, f_end, e_start, e_end)
            if phrases:
                bp.update(phrases)
    return bp



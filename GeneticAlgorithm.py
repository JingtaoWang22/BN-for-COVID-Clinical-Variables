import TwoDMatrixIterator as mat
import random
import SortedList as SL
import timeit

def Score( subject ):
    score = 0
    for i in range( len( subject ) ):
        for j in range( len( subject[i]) ):
            if ( subject[i][j] == 1 ):
                score += 1
    return score

def GetBestChildren( matrixListe, numb_to_keep, index_to_vertex ):
    lList = SL.SortedList( numb_to_keep, index_to_vertex )
    for i in range( len( matrixListe ) ):
        lList.insert( matrixListe[i] )
    return lList

def MakeNextGen( matrixListe, mutate_numb, numb_to_keep, mutate_perc, index_to_vertex ):
    i = 0
    allChildren = []
    for i in range( len( matrixListe )):
        for j in range( len( matrixListe )):
            children = mat.Mate( matrixListe[i], matrixListe[j], index_to_vertex )
            allChildren += children
            j += 1
        i += 1
    for k in range( mutate_numb ):
        rand = random.randint( 0, len( allChildren ) - 1 )
        mutated = mat.MutateMatrix( allChildren[rand], mutate_perc, index_to_vertex )
        allChildren.append( mutated )
    return GetBestChildren( allChildren, numb_to_keep, index_to_vertex )

#start_parents are the start candidates
#end_thresh represents the minimum difference % from gen to gen for the algorithm to continue running
#mutate_numb is the number of children that we will mutate every gen
#best_cand_num is the number of best children that we will keep every generation
#mutatePerc is the number of children that we will mutate every generation
def GeneticRun( start_parents, end_thresh, mutate_numb, best_cand_num, bad_reprod_accept, mutate_perc, index_to_vertex ):
    f = open( "ScoreByIteration.txt", "w")
    
    difference = 1
    previous_gen_best = -999999
    current_bad_reprod = 0
    
    lastGen = GetBestChildren( start_parents, 10, index_to_vertex )
    print( lastGen.GetBest() )

    while( True ):
        starttime = timeit.default_timer()
        next_Gen = MakeNextGen( lastGen.list, mutate_numb, best_cand_num, mutate_perc, index_to_vertex )
        endtime =  timeit.default_timer()
        print('duration',str(endtime-starttime))
        best = next_Gen.GetBest()
        f.write( str( best ) )
        f.write( "\n")
        print( best )
        difference = ( best - previous_gen_best )/previous_gen_best
        lastGen = next_Gen
        previous_gen_best = best

        if ( ( difference <= end_thresh ) and (current_bad_reprod > bad_reprod_accept ) ):
            f.close()
            return next_Gen
        elif ( ( difference <= end_thresh ) and (current_bad_reprod <= bad_reprod_accept ) ):
            current_bad_reprod += 1
        else:
            current_bad_reprod = 0



    

    


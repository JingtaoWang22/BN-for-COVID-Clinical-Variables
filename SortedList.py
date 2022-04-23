from sympy import false
import pandas as pd
import pgmpy
import BinaryStringToBayesianN as BSTB
import networkx as nx

class SortedList( object ):
    def __init__ ( self, size, index_to_vertex ):
        self.list = []
        self.max_size = size
        self.current_size = 0
        self.scores = []
        self.index_to_vertex = index_to_vertex

    def insert( self, object ):
        inserted = False
        score = SortedList.Score( object, self.index_to_vertex )
        for i in range( len(self.list) ):
            local_score = self.scores[i]
            if ( score >= local_score ):
                self.list.insert( i, object )
                self.scores.insert( i, score )
                inserted = True
                break
        if ( inserted ):
            if ( self.current_size >= self.max_size ):
                del self.list[-1]
                del self.scores[-1]
            else:
                self.current_size += 1
        else:
            if ( self.current_size < self.max_size ):
                self.list.append( object )
                self.scores.append( score )
                self.current_size += 1

    def ScoreGraph(g, method = 'k2', data=None):
        if type(data) == type(None):
            data=pd.read_csv('ScoringDataframe.csv')
        if method == 'k2':
            grader = pgmpy.estimators.K2Score(data,complete_samples_only=False)
        severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
        graphscore = 0
        for node in g.nodes:
            if node == severity:
                continue
            parents = list(g.predecessors(node))
            edgescore = grader.local_score(node,parents)
            graphscore += edgescore
        return graphscore

    def Score( adjMatrix, index_to_vertex ):
        graph = BSTB.MatrixToNetwork( adjMatrix, index_to_vertex )
        if ( nx.is_directed_acyclic_graph( graph ) == False ):
            return -999999
        else:
            return SortedList.ScoreGraph( graph )
    
    def GetScoreAverage( self ):
        sum = 0
        for i in range( len( self.scores ) ):
            sum += self.scores[i]
        return sum/self.current_size
    
    def GetBest( self ):
        return self.scores[0]


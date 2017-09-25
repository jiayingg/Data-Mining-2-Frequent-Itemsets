import sys
import json
from itertools import combinations

class Apriori:
    def __init__(self):
        self.c={}
        self.l={}

    # Generate the candidate itemsets in C1
    def candidate_1(self,c,baskets):
        for basket in baskets:
            for item in basket:
                # Save all distinct items from baskets to C1
                if [item] not in self.c[1]:
                    self.c[1].append([item])
        return sorted(self.c[1])

    # Generate the candidate itemsets in Ck from the frequent itemsets in Lk-1
    def candidate_n(self,c,l,k):
        candidate=[]
        for i in range(0,len(self.l[k-1])):
            for j in range(i+1,len(self.l[k-1])):
                u=sorted(list(set(self.l[k-1][i])|set(self.l[k-1][j])))
                if ((u not in candidate) & (len(u)==k)):
                    candidate.append(u)

        # Prune all candidate itemsets from Ck where some (k-1)-subsets of the candidate itemset are not in the frequent itemset Lk-1
        for i in candidate:
            comb=[]
            # Generate all (k-1)-subsets of each candidate itemset, save them to comb[]
            for x in combinations(i,k-1):
                comb.append(list(x))
            # Save the candidate itemset to Ck if all its (k-1)-subsets are in Lk-1
            if (i not in self.c[k]) & all(x in self.l[k-1] for x in comb):
                self.c[k].append(i)

        return sorted(self.c[k])

    # Generate the frequent itemsets in Lk from the candidate itemsets in Ck
    def frequent_n(self,c,l,baskets,minsup,k):
        for item in self.c[k]:
            count=0
            for basket in baskets:
                # Scan the baskets to determine the support for each candidate itemset in Ck
                if set(item).issubset(basket):
                    count+=1
            # Save the frequent itemsets in Lk
            if count>=len(baskets)*minsup:
                self.l[k].append(item)
        return sorted(self.l[k])

    def apriori(self,baskets,prRst):
        for k in range(1,10):
            self.c[k]=[]
            self.l[k]=[]

            if k==1:
                self.c[k]=self.candidate_1(self.c,baskets)
            else:
                self.c[k]=self.candidate_n(self.c,self.l,k)

            self.l[k]=self.frequent_n(self.c,self.l,baskets,0.3,k)

            if (self.l[k]==[])|(self.c[k]==[]):
                break

        if prRst:
            for i in range(1,len(self.c)+1):
                if self.c[i]!=[]:
                    print ("C"+str(i)+": "+str(self.c[i]))
                    print ("L"+str(i)+": "+str(self.l[i]))

        return self.l.values()

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    for line in inputdata:
        baskets = json.loads(line)
        Apriori().apriori(baskets,True)
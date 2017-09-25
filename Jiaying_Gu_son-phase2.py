import sys
import MapReduce
import json

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # argv[2]: phase1output.json
    baskets=open(sys.argv[2])
    for items in baskets:
        candidates=json.loads(items)
        count=0
        for chunks in record:
            if set(candidates).issubset(chunks):
                count+=1

        # key: candidate itemset C
        # value: (v,n)
        mr.emit_intermediate(tuple(candidates),(count,len(record)))

def reducer(key, list_of_values):
    # v: C's count in the chunk
    # n: number of baskets in the chunk
    v=0
    n=0

    for i in range(0,len(list_of_values)):
        v+=list_of_values[i][0]
        n+=list_of_values[i][1]

    # v/n: support ratio
    if float(v)/n >= 0.3:
        mr.emit((key,v))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    # argv[1]: chunks.json
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
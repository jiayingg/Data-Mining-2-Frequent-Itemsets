import sys
import Jiaying_Gu_apriori
import MapReduce

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # Collect frequent itemsets from each chunk
    freq_local=Jiaying_Gu_apriori.Apriori().apriori(record,False)
    for freq in freq_local:
        for item in freq:
            # Data type list cannot be the key of dictionary, change it to tuple
            mr.emit_intermediate(tuple(item),1)

def reducer(key, list_of_values):
    # Generate local frequent itemsets
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
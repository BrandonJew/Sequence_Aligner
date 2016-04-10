import needleman

txt = raw_input("Enter name of file with 2 sequences, 1 per line: ")
source = open(txt, 'r')
str1 = source.readline()[:-1]
str2 = source.readline()[:-1]
print "Original Sequences:\n" + str1 + '\n' + str2
MISMATCH, INDEL, MATCH = -1, -1, 1
#Set up grid
gr = needleman.setupGrid(str1, str2, MATCH, MISMATCH, INDEL)
#Find path for best alignment
path = needleman.findPath(gr, str1, str2)
#Construct alignment
result = needleman.constructAlignment(path, txt, str1, str2)
print result
needleman.saveOutput(result)



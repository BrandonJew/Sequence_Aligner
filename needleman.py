import os.path
#1 = vertical, 2 = horizontal, 3 = diagonal

def setupGrid(str1, str2, MATCH, MISMATCH, INDEL):
    #Set up grid
    gr = [[[0,0]]]
    for i in range(0, len(str1)):
        gr.append([[(-i - 1), 2]])
    for i in range(0, len(str2)):
        gr[0].append([(-i - 1), 1])
    #Fill in grid
    for i in range(1, len(str2)+1):
        for j in range(1, len(str1)+1):
            best = [(int(gr[j][i-1][0]) + INDEL), 1]        #Check Up Indel
            if (gr[j-1][i][0] + INDEL) >= best[0]:          #Check Left Indel
                best = [(int(gr[j-1][i][0]) + INDEL), 2]
            if (str1[j-1] == str2[i-1]):                    #Check Diagonal Match
                if ((gr[j-1][i-1][0] + MATCH) >= best[0]):
                    best = [(int(gr[j-1][i-1][0]) + MATCH), 3]
            elif (gr[j-1][i-1][0] + MISMATCH) >= best[0]:   #Check Diagonal Mismatch
                best = [(int(gr[j-1][i-1][0]) + MISMATCH), 3]
            gr[j].append(best)
    return gr

def findPath(gr, str1, str2):
    path = [0]
    c,r = len(str1), len(str2)
    arrow = gr[c][r][1]
    while (arrow != 0):
    	path.append(arrow)
    	if arrow == 1:  
    	    r -= 1
    	    arrow = gr[c][r][1]
    	elif arrow == 2:
    	    c -= 1
            arrow = gr[c][r][1]
    	elif arrow == 3:
    	    r -= 1
    	    c -= 1
    	    arrow = gr[c][r][1]
    return path

def constructAlignment(path, source, str1, str2):
    s1, s2 = "",""
    space = ""
    i1, i2 = 0,0
    arrow = path.pop()
    while (arrow != 0):
    	if (arrow == 1):            #Advance str2 but not str1 so deletion
    	    s1 += '-'
    	    s2 += str2[i2]
    	    i2 += 1
    	    space += '|'
    	elif (arrow == 2):          #Advance str1 but not str2 so insertion
    	    s1 += str1[i1]
    	    i1 += 1
    	    s2 += '-'
    	    space += '|'
    	elif (arrow == 3):          #Both strings advance so match/mismatch
    	    if str1[i1] != str2[i2]:
    	        space += '*'
    	    else:
    	        space += ' '
            s1 += str1[i1]
	    i1 += 1
	    s2 += str2[i2]
	    i2 += 1
	arrow = path.pop()
    result = "Alignment of " + source + ':\n'  + s1 + '\n' + space + '\n' + s2
    return result

def saveOutput(result):
    outtxt = raw_input("If you'd like to save these results to a text file, enter the name of the output file without any extensions. Otherwise, press enter: ")
    if (outtxt == ""):
        exit()
    else:
        outtxt += ".txt"
        while (os.path.isfile(outtxt)): 
            owrite = raw_input(outtxt + " already exists. Press enter to overwrite or enter a new name: ")
            if owrite == "":
                break
            else:
                outtxt = owrite + ".txt"
        output = open(outtxt, 'w')
        output.write(result)
        output.close()
        print "Saved as", outtxt

def printGrid(gr, str1, str2):
    for i in range (0, len(str1)+1):
	for j in range (0, len(str2)+1):
    	    if gr[j][i][0] >= 0:
                print "+" + str(gr[j][i][0])+"("+str(gr[j][i][1])+")",
	    else:
	        print str(gr[j][i][0])+"("+str(gr[j][i][1])+")",
        print '\n'

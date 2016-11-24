def readdata(filename):
    with open(filename, 'r') as f:
        X, Y = f.readline().strip().split(",")[1:3]
        g, ga = [int(i) for i in f.readline().strip().split(",")[1:3]]
        sym = f.readline().strip().split(",")
        S = {}
        for i, line in enumerate(f):
            S[sym[i+1]] = {}
            for j, score in enumerate(line.strip().split(",")):
                if j > 0:
                    S[sym[i+1]][sym[j]] = int(score)
    return X, Y, S, g, ga



#Returns the best score and state given a list of each possible score and their associated state and the following precedence rules: Iy > Ix > M.
def getbest(poss, s = 0):
    t = {}
    for p in poss:
        t[p[1]] = p[0]
    maximum = max(t.values())
    states = []
    for state in t.keys():
        if t[state] == maximum:
            states.append(state)
    return [maximum + s, sorted(states)[-1]]

#Returns path tuple for most likely endpoint, given that we must end on M(x,y) X(x-1,y) or Y(x,y) where x and y are the lengths of X and Y respectively
def getendpoint(Vm, Vi, X, Y):
    end_m, end_x, end_y = Vm[len(X)-1][len(Y)-1], Vi[len(X)-1][len(Y)], Vi[len(X)][len(Y)-1]
    mostprob = ('m', len(X)-1, len(Y)-1, end_m, X[-1], Y[-1])
    if end_x >= end_m:
        mostprob = ('x', len(X)-1, len(Y), end_x, "-", Y[-1])
    if end_y >= mostprob[3]:
        mostprob = ('y', len(X), len(Y)-1, end_y, X[-1], "-")
    return mostprob

#Given a path tuple, checks its stored backtrack and updates path to state pointed to by this backtrack.
def updatepath(mostprob, Vm, Vi, Rm, Ri, X, Y):
    t, u = mostprob[1:3]
    if mostprob[0] == 'm':
        newstate = Rm[t][u]
    elif mostprob[0] == 'x':
        newstate = Ri[t][u]
    else: # mostprob[0] == 'y':
        newstate = Ri[t][u]
    if newstate == 'm':
        newT, newU = (t-1,u-1)
        newprob = Vm[newT][newU]
        newX = X[newT]
        newY = Y[newU]
    elif newstate == 'x':
        newT, newU = (t-1, u)
        newprob = Vi[newT][newU]
        newX = X[newT]
        newY = '-'
    else:  #newstate == 'y'
        newT, newU = (t, u-1)
        newprob =  Vi[newT][newU]
        newX = '-'
        newY = Y[newU]
    return (newstate, newT, newU, newprob, newX, newY)
    

def align(X, Y, S, g, ga): 
    """X, Y are two sequences, S[l1][l2] is substitution scoring,g is the gap opening penalty, and ga is the gap extension penalty"""
    Ri = [[0 for u in range(len(Y)+1)] for t in range(len(X)+1)]
    Vi = [[0 for u in range(len(Y)+1)] for t in range(len(X)+1)]
    Rm = [[0 for u in range(len(Y))] for t in range(len(X))]
    Vm = [[0 for u in range(len(Y))] for t in range(len(X))]
    Vi[0][0] = g
    Ri[0][0] = "START"
    Vm[0][0] = S[X[0]][Y[0]]
    Rm[0][0] = "START"
    for t in range(len(X)+1):
        for u in range(len(Y)+1):
            if t == 0 and u == 0:
                continue
            #Calculate possible edges
            poss = {}
            if t-1 >= 0 and u-1 >= 0: #Check best mutation
                poss['m'] = Vm[t-1][u-1]
            if t-1 >= 0:  #Check best x-insertion
                poss['x'] = Vi[t-1][u]
            if u-1 >= 0: #Check best y-insertion
                poss['y'] = Vi[t][u-1]
            #Calculate Possible Emission Values for each state given edges
            ViPoss, VmPoss = [], []
            if 'y' in poss.keys():
                ViPoss.append([poss['y'] + ga, 'y'])
                VmPoss.append([poss['y'], 'y'])
            if 'x' in poss.keys():
                ViPoss.append([poss['x'] + ga, 'x'])
                VmPoss.append([poss['x'], 'x'])
            if 'm' in poss.keys():
                ViPoss.append([poss['m'] + g, 'm'])
                VmPoss.append([poss['m'], 'm'])
            Vi[t][u], Ri[t][u] = getbest(ViPoss)
            if t < len(X) and u < len(Y):
                Vm[t][u], Rm[t][u] = getbest(VmPoss, S[X[t]][Y[u]])
    mostprob = getendpoint(Vm, Vi, X, Y)
    path = []
    path.append(mostprob)
    t, u = mostprob[1], mostprob[2]
    while mostprob[1] != 0 and mostprob[2] != 0:
        mostprob = updatepath(mostprob, Vm, Vi, Rm, Ri, X, Y)
        path.append(mostprob)
    return path[::-1]

if __name__ == "__main__":
    X, Y, S, g, ga = readdata("viterbi_test_data.csv")
    print("Original Sequences")
    print(X)
    print(Y)
    x_fin, y_fin = "", ""
    for tup in align(X, Y, S, g, ga):
        x_fin+=tup[4]
        y_fin+=tup[5]
    print("Aligned Sequences")
    print(x_fin)
    print(y_fin)

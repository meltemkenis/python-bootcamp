clause = []
Clause1 = []
Clause2 = []


def readfile(filename):
    f = open(filename)
    data = f.read()
    data = data.strip(" ")
    data = data.split("\n")

    for element in data:
        clause.append(element)
    return clause


knowledge_base = readfile("kb.txt")
print("{:20} {:20} {:20}".format("\033[4mClause1\033[0m", "\033[4mClause2\033[0m", "\033[4mResolvent\033[0m"))


def resolution(kb):
    Clause1 = []
    Clause2 = []
    resolvent = []

    for l in kb:
        if len(l) == 1:
            Clause1.append(l)
        else:
            Clause2.append(l)

    for i in Clause1:
        for j in Clause2:
            if i in j and j[j.index(i) - 1] == '!':
                k = str(j[j.index(i) - 1] + j[j.index(i)])
                j = j.replace(k, '')
                resolvent.append(j)
                resolvent = [x.strip(' ') for x in resolvent]

            elif i in j and j[j.index(i) - 1] != '!':
                print("No proof")

    for i in range(0, len(Clause1)):
        print("{:12} {:12} {:12}".format(Clause1[i], Clause2[i], resolvent[i]))

    if len(resolvent) != 1:
        res = resolution(resolvent)

        return res


resolution(knowledge_base)



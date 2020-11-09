# the code for P02 part 2

###### input for AIpine Club ###### 11
# A(tony)
# A(mike)
# A(john)
# L(tony, rain)
# L(tony, snow)
# (¬A(x), S(x), C(x))
# (¬C(y), ¬L(y, rain))
# (L(z, snow), ¬S(z))
# (¬L(tony, u), ¬L(mike, u))
# (L(tony, v), L(mike, v))
# (¬A(w), ¬C(w), S(w))
###################################


#### input for hardworker(sue) #### 4
# GradStudent(sue)
# (¬GradStudent(x), Student(x))
# (¬Student(x), HardWorker(x))
# ¬HardWorker(sue)
###################################

####### input for 3' blocks ####### 5
# On(aa,bb)
# On(bb,cc)
# Green(aa)
# ¬Green(cc)
# (¬On(x,y), ¬Green(x), Green(y))
###################################
import re
import copy


def inver(clause):
    if '¬' in clause:
        return clause.replace('¬', '')
    else:
        return '¬' + clause


def fingmgu(cl1, cl2):
    for i in cl1:
        for j in cl2:
            if i[0] == inver(j[0]):
                flag = 0
                for num in range(1, len(i)):
                    l1 = len(i[num])
                    l2 = len(j[num])
                    if l1 > 1 and l2 > 1 and i[num] != j[num]:
                        flag = 1
                if flag == 1:
                    break
                for num in range(1, len(i)):
                    l1 = len(i[num])
                    l2 = len(j[num])
                    if l1 == 1 and l2 > 1:
                        for ii in cl1:
                            if ii == i:
                                continue
                            for jj in ii:
                                if jj == i[num]:
                                    cl1[cl1.index(ii)][ii.index(jj)] = j[num]
                for num in range(1, len(i)):
                    l1 = len(i[num])
                    l2 = len(j[num])
                    if l1 > 1 and l2 == 1:
                        for ii in cl2:
                            if ii == j:
                                continue
                            for jj in ii:
                                if jj == j[num]:
                                    cl2[cl2.index(ii)][ii.index(jj)] = i[num]
                n1, n2 = cl1.index(i), cl2.index(j)
                cl1.remove(i)
                cl2.remove(j)
                if cl2 != []:
                    cl1.extend(cl2)
                return n1, n2
    return -1, -1


def dwl():
    global flag
    global ans
    global cls
    dl = 4
    while True:
        ans = []
        flag = 0
        tmpdst = copy.deepcopy(dst)
        cls = copy.deepcopy(nowset)
        dfs(1, tmpdst, dl)
        if flag:
            return True
        dl += 1
        if dl >= 6:
            return False


def dfs(dep, thcl, deptop):
    global flag
    global ans
    global cls
    if dep > deptop:
        return
    if thcl == []:
        flag = 1
    if flag == 1:
        return
    for i in cls:
        cl1 = copy.deepcopy(thcl)
        cl2 = copy.deepcopy(i)
        n1, n2 = fingmgu(cl1, cl2)
        if n1 == -1:
            continue
        ans.append(i)
        cls.append(cl1)
        dfs(dep + 1, cl1, deptop)
        cls.remove(cl1)
        if flag:
            return
        ans.pop()


clauses = []
num = int(input())
for i in range(0, num):
    clause = []
    for item in re.findall(r'¬*[a-zA-Z]+\([a-zA-Z,\s]*\)', input()):
        items = re.findall(r'[¬a-zA-Z]+', item)
        clause.append(items)
    clauses.append(clause)
for ii in clauses:
    print(ii)
temp = copy.deepcopy(clauses)
clauses = copy.deepcopy(temp)
path = []
for i in range(1, num + 1):
    path.append(i)
dst = clauses[-1]
nowset = copy.deepcopy(clauses)
while dwl() == False:
    tset = copy.deepcopy(nowset)
    for i in tset:
        for j in clauses:
            n1 = tset.index(i)
            n2 = clauses.index(j)
            if n2 >= n1:
                continue
            cl1 = copy.deepcopy(i)
            cl2 = copy.deepcopy(j)
            a, b = fingmgu(cl1, cl2)
            a += 97
            b += 97
            if a == 96:
                continue
            path.append([n1, n2, chr(a), chr(b)])
            nowset.append(cl1)

uses = set()
for i in ans:
    ls = path[nowset.index(i)]
    if type(ls) == list:
        uses.add(ls[0])
        uses.add(ls[1])
    else:
        uses.add(ls)

outputv = []
for i in ans:
    if i not in clauses:
        outputv.append(nowset.index(i))
for i in outputv:
    if type(path[i]) == list:
        if path[i][0] not in outputv:
            outputv.append(path[i][0])
        if path[i][1] not in outputv:
            outputv.append(path[i][1])
outputv.sort()
idx = len(clauses)

newid = {}
for i in range(len(clauses)):
    newid[i] = i + 1
for i in outputv:
    if nowset[i] in clauses: continue
    idx = idx + 1
    newid[i] = idx
    output = ""
    output = "R[" + str(newid[path[i][0]]) + path[i][2] + "," + str(newid[path[i][1]]) + path[i][3] + "] : "
    for j in nowset[i]:
        for k in range(len(j)):
            if (k == 0):
                output += j[k]
                output += '('
            elif (k == len(j) - 1):
                output += j[k]
                output += ')'
            else:
                output += j[k]
                output += ','
        if (j != nowset[i][-1]):
            output += ' , '
    print(newid[i], output)
lstid = len(clauses)
dst = copy.deepcopy(temp[-1])
for i in ans:
    n1, n2 = fingmgu(dst, copy.deepcopy(i))
    n1 = n1+97
    n2 = n2+97
    output = "R[" + str(lstid) + chr(n1) + "," + str(newid[nowset.index(i)]) + chr(n2) + "] : "
    idx = idx + 1
    lstid = idx
    for j in dst:
        for k in range(len(j)):
            if k == 0:
                output += j[k]
                output += '('
            elif k == len(j) - 1:
                output += j[k]
                output += ')'
            else:
                output += j[k]
                output += ','
        if j != dst[-1]:
            output += ' , '
    print(idx, output)

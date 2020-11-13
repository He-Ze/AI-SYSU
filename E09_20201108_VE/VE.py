class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables,
                  orderdListOfHiddenVariables, evidenceList):
        for evidence in evidenceList:
            for factor in factorList:
                if evidence in factor.varList:
                    factorList.append(factor.restrict(evidence, evidenceList[evidence]))
                    factorList.remove(factor)

        for variable in orderdListOfHiddenVariables:
            eliminationList = list(filter(lambda factor: variable in factor.varList,factorList))
            new_var = eliminationList[0]
            for e in eliminationList:
                for i in factorList:
                    if i.name == e.name:
                        factorList.remove(i)
                if not e == eliminationList[0]:
                    new_var = new_var.multiply(e)
            new_var = new_var.sumout(variable)
            factorList.append(new_var)
        print("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.printInf()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}

    def setCpt(self, cpt):
        self.cpt = cpt

    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def multiply(self, factor):
        newList = [var for var in self.varList]
        new_cpt = {}
        
        idx1 = []
        idx2 = []
        for var1 in self.varList:
            for var2 in factor.varList:
                if var1 == var2:
                    idx1.append(self.varList.index(var1))
                    idx2.append(factor.varList.index(var2))
                else:
                    newList.append(var2)

        for k1, v1 in self.cpt.items():
            for k2, v2 in factor.cpt.items():
                flag = True
                for i in range(len(idx1)):
                    if k1[idx1[i]] != k2[idx2[i]]:
                        flag = False
                        break
                if flag:
                    new_key = k1
                    for i in range(len(k2)):
                        if i in idx2: continue
                        new_key += k2[i]
                    new_cpt[new_key] = v1 * v2
        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node

    def sumout(self, variable):
        new_var_list = [var for var in self.varList]
        new_var_list.remove(variable)
        new_cpt = {}
        idx = self.varList.index(variable)
        for k, v in self.cpt.items():
            if k[:idx] + k[idx+1:] not in new_cpt.keys():
                new_cpt[k[:idx] + k[idx+1:]] = v
            else: new_cpt[k[:idx] + k[idx+1:]] += v
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        new_var_list = [i for i in self.varList]
        new_var_list.remove(variable)
        new_cpt = {}
        idx = self.varList.index(variable)
        for k, v in self.cpt.items():
            if k[idx] == str(value):
                new_cpt[k[:idx] + k[idx+1:]] = v
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

B = Node("B", ["B"])
E = Node("E", ["E"])
A = Node("A", ["A", "B", "E"])
J = Node("J", ["J", "A"])
M = Node("M", ["M", "A"])

B.setCpt({'0': 0.999, '1': 0.001})
E.setCpt({'0': 0.998, '1': 0.002})
A.setCpt({'111': 0.95, '011': 0.05,'110': 0.94, '010': 0.06,
            '101': 0.29, '001': 0.71,'100': 0.001, '000': 0.999})
J.setCpt({'11': 0.9, '01': 0.1,'10': 0.05, '00': 0.95})
M.setCpt({'11': 0.7, '01': 0.3,'10': 0.01, '00': 0.99})

print("P(A) **********************")
VariableElimination.inference(
        [B, E, A, J, M], ['A'],
        ['B', 'E', 'J', 'M'],{})

print("P(J && ~M) **********************")
VariableElimination.inference(
        [B, E, A, J, M], ['J'],
        ['B', 'E', 'A'],{'M': 0})

print("P(A | J && ~M) **********************")
VariableElimination.inference(
        [B, E, A, J, M], ['A'],
        ['B', 'E'],{'J': 1, 'M': 0})

print("P(B | A) **********************")
VariableElimination.inference(
        [B, E, A, J, M], ['B'],
        ['E', 'J', 'M'],{'A': 1})

print("P(B | J && ~M) **********************")
VariableElimination.inference(
        [B, E, A, J, M], ['B'],
        ['E', 'A'],{'J': 1, 'M': 0})

print("P(J && ~M | ~B) **********************")
VariableElimination.inference(
        [B, E, A, J, M], ['J', 'M'],
        ['E', 'A'],{'B': 0})
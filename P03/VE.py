# VE Implematation


class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables,
                  orderdListOfHiddenVariables, evidenceList):

        # Restriction
        for evidence in evidenceList:
            for factor in factorList:
                if evidence in factor.varList:
                    if len(factor.varList) > 1:
                        factorList.append(factor.restrict(
                            evidence, evidenceList[evidence]))
                    factorList.remove(factor)

        # VariableElimination.printFactors(factorList)
        # Elimination
        for variable in orderdListOfHiddenVariables:
            # Those factors, whose variable list
            # contains target variable should be
            # added into elimination list.
            # print("eliminating ", variable)
            eliminationList = list(
                filter(lambda factor: variable in factor.varList,
                       factorList))

            new_var = eliminationList[0]
            for e in eliminationList:
                for i in factorList:
                    if i.name == e.name:
                        factorList.remove(i)
                if not eliminationList.index(e) == 0:
                    new_var = new_var.multiply(e)

            new_var = new_var.sumout(variable)
            factorList.append(new_var)
            # print("Eliminating...")
            # VariableElimination.printFactors(factorList)

        # print("Eliminated:")
        # VariableElimination.printFactors(factorList)
        # Calculate the Result
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
        # Function to multiplies with another factor.
        newList = [var for var in self.varList]
        new_cpt = {}

        # To store the same variables of two factors
        idx1 = []
        idx2 = []
        for var in factor.varList:
            if var in newList:
                idx1.append(self.varList.index(var))
                idx2.append(factor.varList.index(var))
            else:
                newList.append(var)
        # print(newList)
        # multiplying
        for k1, v1 in self.cpt.items():
            for k2, v2 in factor.cpt.items():
                # flag to determine which two cpts
                # should be multiplied together
                flag = True
                for i in range(len(idx1)):
                    # Check value of each variable
                    if k1[idx1[i]] != k2[idx2[i]]:
                        flag = False
                        break
                if flag:
                    # new key in new cpt is
                    # built sequentially
                    new_key = k1
                    for i in range(len(k2)):
                        if i in idx2:
                            continue
                        new_key += k2[i]
                    new_cpt[new_key] = v1 * v2

        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        # new_node.printInf()
        return new_node

    def sumout(self, variable):
        # Fuction to sum out a variable given a factor.
        new_var_list = [var for var in self.varList]
        new_var_list.remove(variable)
        new_cpt = {}

        # To store the index of the variable to sum out
        idx = self.varList.index(variable)

        # For each value of the target variable,
        # sum it up to build a new cpt dict.
        for k, v in self.cpt.items():
            if k[:idx] + k[idx+1:] not in new_cpt.keys():
                new_cpt[k[:idx] + k[idx+1:]] = v
            else:
                new_cpt[k[:idx] + k[idx+1:]] += v

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        # Function to restrict a variable
        # in a given factor to some value.
        new_var_list = [i for i in self.varList]
        new_var_list.remove(variable)
        new_cpt = {}

        # To store the index of the variable to restrict
        idx = self.varList.index(variable)

        # Only choose the same value as the parameter
        # to build the new cpt
        for k, v in self.cpt.items():
            if k[idx] == str(value):
                new_cpt[k[:idx] + k[idx+1:]] = v

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

P = Node("p", ["P"])
M = Node("M", ["M"])
C = Node("C", ["C"])
A = Node("A", ["A"])
S = Node("S", ["S", "C", "M"])
D = Node("D", ["D", "S", "P"])
Mo = Node("Mo", ["Mo", "S", "A"])

# Cpts for each Node
P.setCpt({'0': 0.10, '1': 0.30, '2': 0.60})
# 0 - IS; 1 - HS; 2 - SM
# 0 - Ne; 1 - Mo; 2 - Se
C.setCpt({'0': 0.7, '1': 0.3})
M.setCpt({'0': 0.7, '1': 0.3})
A.setCpt({'0': 0.5, '1': 0.5})
S.setCpt({'000': 0.8, '001': 0.5,
                    '010': 0.5, '011': 0.0,
                    '100': 0.0, '101': 0.4,
                    '110': 0.4, '111': 0.9,
                    '200': 0.2, '201': 0.1,
                    '210': 0.1, '211': 0.1})
Mo.setCpt({'000': 0.56, '001': 0.28,
                        '010': 0.58, '011': 0.99,
                        '020': 0.05, '021': 0.10,
                        '100': 0.44, '101': 0.72,
                        '110': 0.42, '111': 0.01,
                        '120': 0.95, '121': 0.90})
D.setCpt({'000': 0.80, '010': 0.70, '020': 0.90,
                    '001': 0.60, '011': 0.50, '021': 0.40,
                    '002': 0.30, '012': 0.20, '022': 0.10,
    
                    '100': 0.10, '110': 0.20, '120': 0.05,
                    '101': 0.30, '111': 0.40, '121': 0.30,
                    '102': 0.40, '112': 0.20, '122': 0.10,
    
                    '200': 0.10, '210': 0.10, '220': 0.05,
                    '201': 0.10, '211': 0.10, '221': 0.30,
                    '202': 0.30, '212': 0.60, '222': 0.80})


# Nodes for Bayes Net
# P ---> D
#       /'
# M -> S ---> Mo
#     /'     /'
#    C      A

# Results
print("p1 = P(Mortality=’True’ ∧ CTScanResult=’Ischemic Stroke’ | PatientAge=’31-65’ )​")
VariableElimination.inference(
        [P, M, C, A, S, D, Mo], ['Mo', 'C'],
        ['M', 'A', 'S', 'D'],
        {'P': 1}
)
print("--------------------------------------------------------------------------------​")

print("p2=P(Disability=’Moderate’∧CTScanResult=’HemmorraghicStroke’|PatientAge=’65+’ ∧ MRIScanResult=’Hemmorraghic Stroke’)")
VariableElimination.inference(
        [P, M, C, A, S, D, Mo], ['D', 'C'],
        ['A', 'S', 'Mo'],
        {'P': 2, 'M': 1}
)
print("--------------------------------------------------------------------------------​")

print("p3=P(StrokeType=’HemmorraghicStroke’|PatientAge=’65+’∧CTScanResult=’HemmorraghicStroke’ ∧ MRIScanResult=’Ischemic Stroke’)")
VariableElimination.inference(
        [P, M, C, A, S, D, Mo], ['S'],
        ['D', 'A', 'Mo'],
        {'P': 2, 'C': 1, 'M': 0}
)
print("--------------------------------------------------------------------------------​")

print("p4 = P(Anticoagulants=’Used’ | PatientAge=’31-65’)")
VariableElimination.inference(
        [P, M, C, A, S, D, Mo], ['A'],
        ['M', 'C', 'S', 'D', 'Mo'],
        {'P': 1}
)
print("--------------------------------------------------------------------------------​")

print("p5 = P(Disability=’Negligible’)")
VariableElimination.inference(
        [P, M, C, A, S, D, Mo], ['D'],
        ['P', 'M', 'C', 'A', 'S', 'Mo'],
        {}
)
print("--------------------------------------------------------------------------------​")

import pickle as pk
import seaborn as sns
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train_data_path = 'dataset/adult.data'
test_data_path = 'dataset/adult.test'
header = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
          'marital-status', 'occupation', 'relationship', 'race', 'sex',
          'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'Salaries']
train_data = pd.read_csv(train_data_path, names=header)
test_data = pd.read_csv(test_data_path, names=header)
test_data.drop(0, inplace=True)
test_data.reset_index(drop=True, inplace=True)
train_data.replace(' ?', np.nan, inplace=True)
train_data.fillna(train_data.mode().iloc[0], inplace=True)
test_data.replace(' ?', np.nan, inplace=True)
test_data.fillna(test_data.mode().iloc[0], inplace=True)
continuous_cols = ['age', 'fnlwgt', 'education-num','capital-gain', 'capital-loss', 'hours-per-week']
pos1 = int(len(train_data)/3)
pos2 = 2 * pos1
intervals = {}

for col in continuous_cols:
    i1 = sorted(train_data[col])[pos1]
    i2 = sorted(train_data[col])[pos2]
    intervals[col] = (range(0, i1+1), range(i1+1, i2+1),
                      range(i2+1, sorted(train_data[col])[len(train_data)-1]+1))

rev_intervals = {}
for k, v in intervals.items():
    tmp = {}
    for idx, r in enumerate(v):
        for i in r:
            tmp[i] = idx
    rev_intervals[k] = tmp

dsp_dict = {
    1: ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'],
    3: ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'],
    5: ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'],
    6: ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'],
    7: ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    8: ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'],
    9: ['Female', 'Male'],
    13: ['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands']
}

def dsp2numlist(idx):
    return list(range(len(dsp_dict[idx])))

AttrSet = [
    (0, [0, 1, 2], 'age'),
    (1, dsp2numlist(1), 'workclass'),
    (2, [0, 1, 2], 'fnlwgt'),
    (3, dsp2numlist(3), 'education'),
    (4, [0, 1, 2], 'education-num'),
    (5, dsp2numlist(5), 'marital-status'),
    (6, dsp2numlist(6), 'occupation'),
    (7, dsp2numlist(7), 'relationship'),
    (8, dsp2numlist(8), 'race'),
    (9, dsp2numlist(9), 'sex'),
    (10, [0, 1, 2], 'capital-gain'),
    (11, [0, 1, 2], 'capital-loss'),
    (12, [0, 1, 2], 'hours-per-week'),
    (13, dsp2numlist(13), 'native-country')
]

train_label = [1 if val == ' >50K' else 0 for val in train_data['Salaries']]
train_input = []

for idx in range(len(train_data)):
    tmp = [dsp_dict[i].index(val.strip()) if int(i) in dsp_dict.keys()
           else rev_intervals[train_data.columns[i]].get(val, 2) for i, val in enumerate(train_data.iloc[idx][:-1])]
    train_input.append(tmp)
test_label = [1 if val == ' >50K.' else 0 for val in test_data['Salaries']]
test_input = []
for idx in range(len(test_data)):
    tmp = [dsp_dict[i].index(val.strip()) if int(i) in dsp_dict.keys()
           else rev_intervals[test_data.columns[i]].get(val, 2) for i, val in enumerate(test_data.iloc[idx][:-1])]
    test_input.append(tmp)

def Entropy(Data):
    labels = [sample[-1] for sample in Data]
    types = set(labels)
    types_counts = [labels.count(type) for type in types]
    probs = [prob/len(Data) for prob in types_counts]
    return -np.sum(probs*np.log2(probs))

def Gain(Data, attr):
    entropy = Entropy(Data)
    attr_num = attr[0]
    attr_vals = attr[1]
    entropys = [0 for val in attr_vals]
    weights = [0 for val in attr_vals]
    for idx, val in enumerate(attr_vals):
        sub_data = []
        for sample in Data:
            if sample[attr_num] == val:
                sub_data.append(sample)
                weights[idx] += 1
        entropys[idx] = Entropy(sub_data)
        weights[idx] /= len(Data)
    return entropy - np.sum(np.multiply(weights, entropys))

def Gini(Data):
    labels = [sample[-1] for sample in Data]
    types = set(labels)
    types_counts = [labels.count(type) for type in types]
    probs = [prob/len(Data) for prob in types_counts]
    return 1 - np.sum(np.power(probs, 2))

def Gini_index(Data, attr):
    gini = Gini(Data)
    attr_num = attr[0]
    attr_vals = attr[1]
    ginis = [0 for val in attr_vals]
    weights = [0 for val in attr_vals]
    for idx, val in enumerate(attr_vals):
        sub_data = []
        for sample in Data:
            if sample[attr_num] == val:
                sub_data.append(sample)
                weights[idx] += 1
        ginis[idx] = Gini(sub_data)
        weights[idx] /= len(Data)
    return np.sum(np.multiply(weights, ginis))

def chooseBestAttr(Data, Attrset, method='ID3'):
    best_attr = Attrset[0]
    best_gain = -1
    best_gini = np.Inf
    for attr_tuple in Attrset:
        gain = Gain(Data, attr_tuple)
        best_attr = attr_tuple if gain > best_gain else best_attr
        best_gain = gain if gain > best_gain else best_gain
    return best_attr

def splitData(Data, attr_num, attr_val):
    sub_data = []
    for sample in Data:
        if sample[attr_num] == attr_val:
            sub_data.append(sample[:attr_num] + sample[attr_num+1:])
    return sub_data

def getMajority(Data):
    labels = [sample[-1] for sample in Data]
    types = list(set(labels))
    types_counts = [labels.count(type) for type in types]
    major = 0
    max_count = 0
    for idx, type_count in enumerate(types_counts):
        major = types[idx] if max_count < type_count else major
        max_count = type_count if max_count < type_count else max_count
    return str(major)

def GenerateTree(Data, Attrset, method='ID3'):
    labels = [sample[-1] for sample in Data]
    if len(set(labels)) == 1:
        return str(labels[0])
    if len(Attrset) == 0:
        return getMajority(Data)
    flag = False
    for attr_tuple in Attrset:
        if len(set([sample[attr_tuple[0]] for sample in Data])) != 1:
            flag = True
            break
    if not flag:
        return getMajority(Data)
    best_attr = chooseBestAttr(Data, Attrset, method)
    attr_num = best_attr[0]
    attr_vals = best_attr[1]
    attr_name = best_attr[2]
    for idx, attr in enumerate(Attrset):
        if attr[0] > attr_num:
            Attrset[idx] = (attr[0]-1, attr[1], attr[2])
    del(Attrset[Attrset.index(best_attr)])
    Node = {attr_name: {}}
    for val in attr_vals:
        sub_data = splitData(Data, attr_num, val)
        if len(sub_data) == 0:
            return getMajority(Data)
        else:
            Node[attr_name][val] = GenerateTree(sub_data, Attrset[:], method)
    return Node

def Classifier(DecisionTree, AttrSet, SampleData):
    root = list(DecisionTree.keys())[0]
    for attr_tuple in AttrSet:
        if root == attr_tuple[2]:
            key = SampleData[attr_tuple[0]]
    succ = DecisionTree[root][key]
    if isinstance(succ, dict):
        return Classifier(succ, AttrSet, SampleData)
    else:
        return succ

def Benchmarker(DecisionTree, AttrSet, testing_data, log=False):
    labels = [sample[-1] for sample in testing_data]
    res = []
    for sample in testing_data:
        res.append(Classifier(DecisionTree, AttrSet, sample[:-1]))
    check = [labels[idx] + int(res[idx]) for idx in range(len(testing_data))]
    if log:
        print("Total Accuracy: %.5f" % (1-check.count(1)/len(testing_data)))
    else:
        return 1 - check.count(1)/len(testing_data)

testing_data = [
    [0, 1, 1, 1],
    [1, 3, 5, 1],
    [3, 3, 3, 1],
    [3, 2, 2, 1],
    [2, 1, 6, 1],
    [0, 3, 3, 1],
    [1, 2, 4, 1],
    [1, 2, 2, 1],

    [0, 1, 6, 0],
    [1, 3, 4, 0],
    [1, 3, 3, 0],
    [0, 2, 3, 0],
    [2, 2, 2, 0],
    [0, 0, 1, 0],
    [1, 2, 3, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 1]
]

testing_attrset = [(0, [0, 1, 2, 3], '2nd'), (1, [0, 1, 2, 3],'3rd'), (2, [0, 1, 2, 3, 4, 5, 6], '4th')]
dt = GenerateTree(testing_data, testing_attrset[:])
X_train = [data + [train_label[idx]] for idx, data in enumerate(train_input)]
X_test = [data + [test_label[idx]] for idx, data in enumerate(test_input)]
SalaryPredict_DT_ID3 = GenerateTree(X_train, AttrSet[:])
print("="*10+' Testing ID3 '+"="*10)
Benchmarker(SalaryPredict_DT_ID3, AttrSet, X_test, True)

import pandas as pd
import numpy as np

attr = {"age":0, "workclass":1, "fnlwgt":0, "education":1, "education-num":0, "marital-status":1, "occupation":1, "relationship":1, "race":1, "sex":1, "capital-gain":0, "capital-loss":0, "hours-per-week":0, "native-country":1, "salary":0}
train = pd.read_csv("dataset/adult.data",names=attr.keys(),index_col=False)
test = pd.read_csv("dataset/adult.test",names=attr.keys(),index_col=False,header=0)
attributes = list(attr.keys())
attributes.remove("fnlwgt")
attributes.remove("capital-gain")
attributes.remove("capital-loss")
train= train[attributes]
test= test[attributes]

def fill(data,flag=1):
    if flag == 0:
        for a in data.columns.values:
            if attr[a]:
                data = data[data[a] != " ?"]
        return data
    else:
        for a in data.columns.values:
            if attr[a]:
                data.loc[data[a] == " ?",a] = data[a].value_counts().argmax()
            else:
                pass
        return data
train = fill(train,1)
test = fill(test,1)

class NB():
    def __init__(self,train,attr):
        self.train = train
        self.attr = attr
        self.prob = {}
        self.prob[" >50K"] = train["salary"].value_counts(normalize=True)[" >50K"]
        self.prob[" <=50K"] = 1 - self.prob[" >50K"]
        self.attributes = train.columns.values[train.columns.values != "salary"]
        less = train[train["salary"] == " <=50K"]
        more = train[train["salary"] == " >50K"]
        for a in self.attributes:
            if self.attr[a]:
                a_less = less[a].value_counts()
                a_more = more[a].value_counts()
                V = len(train[a].unique())
                for xi in train[a].unique():
                    self.prob[(xi," <=50K")] = (a_less.get(xi,0) + 1) / (len(less) + V)
                    self.prob[(xi," >50K")] = (a_more.get(xi,0) + 1) / (len(more) + V)
            else:
                mu_less = np.mean(less[a])
                sigma_less = np.var(less[a])
                self.prob[(a," <=50K")] = lambda x: 1 / np.sqrt(2*np.pi*sigma_less) * np.exp(-(x-mu_less)**2/(2*sigma_less))
                mu_more = np.mean(more[a])
                sigma_more = np.var(more[a])
                self.prob[(a," >50K")] = lambda x: 1 / np.sqrt(2*np.pi*sigma_more) * np.exp(-(x-mu_more)**2/(2*sigma_more))
            
    def predict(self,test):
        accurary = 0
        for i, row in test.iterrows():
            prod = np.array([self.prob[" <=50K"],self.prob[" >50K"]])
            for a in self.attributes:
                xi = row[a]
                if self.attr[a]:
                    prod[0] *= self.prob[(xi," <=50K")]
                    prod[1] *= self.prob[(xi," >50K")]
                else: 
                    prod[0] *= self.prob[(a," <=50K")](xi)
                    prod[1] *= self.prob[(a," >50K")](xi)
            catagory = " <=50K" if prod.argmax() == 0 else " >50K"
            if catagory == row["salary"][:-1]:
                accurary += 1
        accurary /= len(test)
        print("The accurary is {:f}%.".format(accurary * 100))
        return accurary
    
nb = NB(train,attr)
nb.predict(test)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class NeuralNetwork(object):
    def __init__(self,in_features,hidden_features,out_features,learning_rate=0.1):
        self.fc1 = FullyConnectedLayer(in_features,hidden_features,True)
        self.fc2 = FullyConnectedLayer(hidden_features,out_features,True)
        self.learning_rate = learning_rate
        self.memory = {}
        self.train_flag = True

    def train(self):
        self.train_flag = True
        
    def eval(self):
        self.train_flag = False
        
    def relu(self,x):
        return np.maximum(0,x)

    def d_relu(self,x):
        x[x <= 0] = 0
        x[x > 0] = 1
        return x

    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def d_sigmoid(self,x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def tanh(self,x):
        return np.tanh(x)

    def d_tanh(self,x):
        return 1 - np.tanh(x) ** 2

    def MSE(self,y_hat,y):
        return np.linalg.norm(y_hat - y)

    def cross_entropy(self,y_hat,y):
        return y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat)

    def forward(self,x):
        if self.train_flag:
            self.memory["a0"] = np.copy(x)
            x = self.fc1(x)
            self.memory["z1"] = np.copy(x)
            x = self.sigmoid(x)
            self.memory["a1"] = np.copy(x)
            x = self.fc2(x)
            self.memory["z2"] = np.copy(x)
            x = self.sigmoid(x)
        else:
            x = self.fc1(x)
            x = self.sigmoid(x)
            x = self.fc2(x)
            x = self.sigmoid(x)
        return x

    def backward(self,y_hat,y,lamb=0):
        batch_size = y.shape[0]
        delta = [0] * 3
        delta[2] = (y_hat - y) * self.d_sigmoid(self.memory["z2"])
        delta[1] = np.dot(delta[2],self.fc2.weight) * self.d_sigmoid(self.memory["z1"]) 
        nabla_W = [0] * 2
        nabla_W[1] = np.einsum("ij,ik->ijk",delta[2],self.memory["a1"])
        nabla_W[0] = np.einsum("ij,ik->ijk",delta[1],self.memory["a0"])
        nabla_b = [0] * 2
        nabla_b[1] = delta[2]
        nabla_b[0] = delta[1]
        nabla_W[1] = nabla_W[1].mean(axis=0)
        nabla_W[0] = nabla_W[0].mean(axis=0)
        nabla_b[1] = nabla_b[1].mean(axis=0)
        nabla_b[0] = nabla_b[0].mean(axis=0)
        self.fc2.weight -= self.learning_rate * (nabla_W[1] + lamb * self.fc2.weight / batch_size)
        self.fc1.weight -= self.learning_rate * (nabla_W[0] + lamb * self.fc1.weight / batch_size)
        self.fc2.bias -= self.learning_rate * nabla_b[1]
        self.fc1.bias -= self.learning_rate * nabla_b[0]

class FullyConnectedLayer(object):
    def __init__(self, in_features, out_features, bias=True):
        self.in_features = in_features
        self.out_features = out_features
        self.weight = np.random.normal(0,np.sqrt(2/in_features),(out_features,in_features))
        if bias:
            self.bias = np.random.rand(out_features)
        else:
            self.bias = None
            
    def forward(self, inputs):
        if type(self.bias) != type(None):
            return np.dot(inputs, self.weight.T) + self.bias
        else:
            return np.dot(inputs, self.weight.T)
        
    def __call__(self,x):
        return self.forward(x)

def preprocessing(data):
    drop_attr = ["type of lesion 2", "type of lesion 3","Hospital Number","nasogastric reflux PH","abdomcentesis total protein"]
    attributes = []
    for a in data.columns.values:
        in_flag = attr_dict.get(a,None)
        if in_flag == None:
            attributes.append(a)
        elif in_flag == 0 and a not in drop_attr:
            attributes.append(a)
        else:
            pass
    df = data[attributes]
    return df

def fill_data(data):
    for a in data.columns.values:
        if a in ["type of lesion 1", "Hospital Number"]:
            continue
        if data[a].dtype != np.int64:
            have_data = data[data[a] != "?"][a]
            if attr_dict[a]:
                data.loc[data[a] == "?",a] = have_data.value_counts().idxmax() 
                if a != "outcome" and attr_dict[a] != 2:
                    data[a] = pd.Categorical(data[a])
                    dummies = pd.get_dummies(data[a],prefix="{}_category".format(a))
                    data = pd.concat([data,dummies],axis=1)
            else:
                data.loc[data[a] == "?",a] = np.mean(have_data.astype(np.float))
        elif attr_dict[a] == 1:
            data[a] = pd.Categorical(data[a])
            dummies = pd.get_dummies(data[a],prefix="{}_category".format(a))
            data = pd.concat([data,dummies],axis=1)
    return data.astype(np.float)

def get_batches(data,label,batch_size=1):
    num_batches = len(data) // batch_size
    for i in range(0,num_batches,batch_size):
        yield data[i:i+batch_size].to_numpy(), np.array(label[i:i+batch_size])

def test(net,test_X,test_y,flag=True,print_flag=False):
    cnt = 0
    for j, x in test_X.iterrows():
        net.eval()
        Y_hat = net.forward(x.to_numpy().reshape(1,-1))
        predicted = np.argmax(Y_hat) + 1
        y = test_y[j]
        if print_flag:
            print(Y_hat,predicted,y)
        if flag:
            if predicted == y:
                cnt += 1
        else:
            if [1 if t + 1 == predicted else 0 for t in range(3)] == y:
                cnt += 1
    return (cnt / len(test_X))

def train(net,max_iter=1000):
    loss_history, accuracy_history = [], []
    losses = []
    for i in range(max_iter):
        net.train()
        batches = get_batches(train_data,train_label,16)
        for x, y in batches:
            Y_hat = net.forward(x)
            loss = net.MSE(Y_hat, y)
            losses.append(loss)
            net.backward(Y_hat,y,0.1)
        if (i+1) % 100 == 0:
            avg_loss = np.array(losses).mean()
            loss_history.append(avg_loss)
            losses = []
            acc = test(net,test_data,test_label)
            accuracy_history.append(acc)
            print("迭代{}次/{}次：  Loss: {}  Accuracy Rate: {}%".format(i+1,max_iter,avg_loss,acc*100))
    return loss_history, accuracy_history


attr_dict = {"surgery": 1,
 "Age": 2,
 "Hospital Number": 1,
 "rectal temperature": 0,
 "pulse": 0,
 "respiratory rate": 0,
 "temperature of extremities": 2,
 "peripheral pulse": 2,
 "mucous membranes": 1,
 "capillary refill time": 2,
 "pain": 1,
 "peristalsis": 2,
 "abdominal distension": 1,
 "nasogastric tube": 1,
 "nasogastric reflux": 2,
 "nasogastric reflux PH": 0,
 "rectal examination": 2,
 "abdomen": 1,
 "packed cell volume": 0,
 "total protein": 0,
 "abdominocentesis appearance": 1,
 "abdomcentesis total protein": 0,
 "outcome": 1,
 "surgical lesion": 1,
 "type of lesion 1": 1,
 "type of lesion 2": 1,
 "type of lesion 3": 1,
 "cp_data": 1}

train_data = pd.read_csv("horse-colic.data",names=attr_dict.keys(),index_col=False,delim_whitespace=True)
test_data = pd.read_csv("horse-colic.test",names=attr_dict.keys(),index_col=False,delim_whitespace=True)
data = pd.concat([train_data,test_data],axis=0)
data = fill_data(data)
label = data["outcome"].astype(np.float)
train_label, test_label = label[:len(train_data)], label[len(train_data):]
train_label = [[1,0,0] if label == 1 else ([0,1,0] if label == 2 else [0,0,1]) for label in train_label]
data = preprocessing(data)
train_data, test_data = data[:len(train_data)], data[len(train_data):]

net = NeuralNetwork(len(train_data.columns.values),5,3,0.1)
loss_history, accuracy_history = train(net,30000)
fig = plt.figure()
ax = fig.add_subplot(111)
lns1 = ax.plot(loss_history,"-c",label="Loss")
ax2 = ax.twinx()
lns2 = ax2.plot(accuracy_history,"-b",label="Accuracy Rate")
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
ax.legend(lns,labs,loc=0)
ax.set_xlabel("Iteration (x100)")
ax.set_ylabel("Loss")
ax2.set_ylabel("Accuracy Rate")
ax2.set_ylim(0,1)
plt.show()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def EM(dataMat, n_components=3, times=1):
    n_samples, a = np.shape(dataMat)
    pi_k = np.ones(n_components) / n_components 
    miu_k = np.array([dataMat[i,:] for i in [2,52,102]]).reshape(n_components,a)
    sigma_k = [np.eye(a) for x in range(n_components)]
    gamma_k = np.zeros((n_samples, n_components))
    for i in range(times):
        for n in range(n_samples):
            sum_pi_mul = 0
            for k in range(n_components):
                a=dataMat[n, :].shape[0]
                expOn = - 1 / 2 * np.matmul(np.matmul((dataMat[n, :] - miu_k[k]).T,np.linalg.inv(sigma_k[k])),dataMat[n, :] - miu_k[k])
                divBy = np.power(2 * np.pi, a / 2) * np.sqrt(np.linalg.det(sigma_k[k]))
                gamma_k[n, k] = pi_k[k] *  np.exp(expOn) / divBy
                sum_pi_mul += gamma_k[n, k]
            for k in range(n_components):
                gamma_k[n, k] /= sum_pi_mul
        N_k = np.sum(gamma_k, axis=0)
        for k in range(n_components):
            miu_k[k] = np.zeros(a,dtype=np.float64)
            for n in range(n_samples):
                miu_k[k] += gamma_k[n, k] * dataMat[n, :]
            miu_k[k] /= N_k[k]
            sigma_k[k] = np.zeros((a, a),dtype=np.float64)
            for n in range(n_samples):
                sigma_k[k] += gamma_k[n, k] * np.matmul((dataMat[n, :] - miu_k[k]).reshape(1,-1).T, (dataMat[n, :] - miu_k[k]).reshape(1,-1))
            sigma_k[k] /= N_k[k]
            pi_k[k] = N_k[k] / n_samples
        sigma_k += np.eye(a)
    print("Gamma: \n",gamma_k)
    print("Miu: \n",miu_k)
    print("Sigma: \n",sigma_k)
    return gamma_k

if __name__ == '__main__':
    dataset = pd.read_csv("iris.data",sep=",")
    dataset.head()
    n_components = 3
    data = dataset[dataset.columns.values[dataset.columns.values != "iris"]].to_numpy()
    n_samples, a = np.shape(data.astype(np.float64))
    centroids = np.zeros((n_components, a))
    gamma = EM(data.astype(np.float64),n_components,1)
    clusterAssign = np.zeros((n_samples, 2))
    for n in range(n_samples):
        clusterAssign[n, :] = np.argmax(gamma[n, :]), np.amax(gamma[n, :])
    for k in range(n_components):
        pointsInCluster = data.astype(np.float64)[np.nonzero(clusterAssign[:, 0] == k)[0]]
        centroids[k, :] = np.mean(pointsInCluster, axis=0)
    centroids, labels = centroids, clusterAssign[:,0]
    numSamples, dim = data.shape
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    for i in range(numSamples):
        markIndex = int(labels[i])
        plt.plot(data[i, 0], data[i, 1], mark[markIndex])
    for i in range(n_components):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)
    plt.show()
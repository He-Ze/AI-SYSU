from cs231n.data_utils import get_CIFAR10_data
from cs231n.classifiers.cnn import ThreeLayerConvNet
from cs231n.solver import Solver
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = get_CIFAR10_data()
    for k, v in data.items():
        print('{}: '.format(k), v.shape)
    model = ThreeLayerConvNet(hidden_dim=512, reg=0.001)
    solver = Solver(model, data,
                    num_epochs=1,
                    batch_size=50,
                    update_rule='adam',
                    optim_config={
                      'learning_rate': 0.001,
                    },
                    verbose=True,
                    print_every=1)
    solver.train()
    solver.check_accuracy(data["X_test"],data["y_test"])
    fig = plt.figure()
    a = fig.add_subplot(111)
    a.set_xlabel("Iteration")
    a.set_ylabel("Loss")
    a.plot(solver.loss_history)
    plt.show()
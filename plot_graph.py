import matplotlib.pyplot as plt


def plot(start_year, end_year, y, label):
    plt.stackplot(range(start_year, end_year), y, labels=label)
    plt.legend(loc='upper left')
    plt.show()

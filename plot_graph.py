import matplotlib.pyplot as plt
import numpy as np


# def plot(start_year, end_year, y, label):
#     plt.stackplot(range(start_year, end_year), y, labels=label)
#     plt.legend(loc='upper left')
#     plt.show()

def plot(start_year, end_year, y, label):
    # Initialize the figure
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num = 0
    column: object
    for column, title in zip(y, label):
        num += 1

        # Find the right spot on the plot
        plt.subplot(3, 3, num)

        # plot every groups, but discreet
        for v in y:
            plt.plot(range(start_year, end_year), v, marker='', color='grey', linewidth=0.6, alpha=0.3)

        # Plot the lineplot
        plt.plot(range(start_year, end_year), column, marker='', color=palette(num), linewidth=2.4, alpha=0.9, label=column)

        # Subplot titles
        plt.title(title, loc='left', fontsize=8.5, fontweight=0, color=palette(num))

    plt.show()
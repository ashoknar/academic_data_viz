import matplotlib.pyplot as plt
import datetime

def plot(start_year, end_year, y, label, topic_1, topic_2):
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

    plt.tight_layout()

    plt.suptitle(topic_1 + " and " + topic_2, fontsize=8, fontweight=0, color='black',
                 style='italic', y=1.00)
    # # Axis title
    # plt.text(0.5, 0.02, 'Year', ha='center', va='center')
    # plt.text(0.06, 0.5, 'FOS score', ha='center', va='center', rotation='vertical')

    plt.savefig('plot' + str(datetime.datetime.now()) + '.png', dpi=100, bbox_inches='tight')

    plt.show()
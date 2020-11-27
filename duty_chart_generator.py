import pandas as pd
from itertools import permutations, combinations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import argparse


def nCr(choices, r):
    assert (0 < r <= len(choices))
    return [f"{'    '.join(x)}" for x in combinations(choices, r)]


def nPr(choices, r):
    assert (0 < r <= len(choices))
    return [f"{'    '.join(x)}" for x in permutations(choices, r)]


def create_duty_dataframe(initials, columns, rs, flags):
    """This method creates a pandas dataframe that contains the duty columns
    and the initial combinations depending on the rs value for that column

    Args:
        initials (list(str)): A list of initials of the people who will be
        assigned duty e.g. ['A', 'B', 'C']
        columns (list(str)): A list of duty names e.g. ['Duty1', 'Duty2']
        rs (list(int)): A list of integers containing number of people per
        day.
        flags list('yes'|'no'): This is a list of 'yes', 'no' values where
        the former means that the order matters in the grouping as in AB is
        different from BA and the latter means that the order does not matter.

    Returns:
        pandas_dataframe: A pandas dataframe containing the populated duty
        columns seperated by date columns.
    """
    duty_columns = []
    for i in range(len(columns)):
        duty_columns.append(columns[i])
        duty_columns.append('Date')
    duty_dataframe = pd.DataFrame('', index=range(50), columns=duty_columns)
    for col, r, flag in zip(columns, rs, flags):
        pattern = ''
        if flag == 'yes':
            pattern = nPr(initials, r)
        elif flag == 'no':
            pattern = nCr(initials, r)
        rep_pattern = pattern * (50 // len(pattern) + 1)
        duty_dataframe.loc[:, col] = rep_pattern[:50]
    return duty_dataframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser("A utility for creating duty charts.")
    parser.add_argument(
        '--initials',
        '-i',
        nargs='+',
        required=True,
        help='Enter the initials of the individuals e.g. A B C',
    )
    parser.add_argument('--duty-columns',
                        '-dc',
                        nargs='+',
                        required=True,
                        help="Enter the duties e.g. Duty1 Duty2")
    parser.add_argument(
        '--persons-per-duty-nos',
        '-ppd',
        type=int,
        nargs='+',
        required=True,
        help="Enter the persons per duty number i.e. how many of the people"
        " from the initials list would work at a time on a single duty.")
    parser.add_argument(
        '--order_matters',
        '-om',
        choices=['yes', 'no'],
        nargs='+',
        required=True,
        help="This is a list of 'yes', 'no' values where the former means"
        " that the order matters in the grouping as in AB is different"
        " from BA and the latter means that the order does not matter.")
    args = parser.parse_args()
    assert (len(args.duty_columns) == len(args.persons_per_duty_nos) == len(
        args.order_matters))
    duty_dataframe = create_duty_dataframe(args.initials, args.duty_columns,
                                           args.persons_per_duty_nos,
                                           args.order_matters)
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=duty_dataframe.values,
                         cellLoc='center',
                         colLabels=duty_dataframe.columns,
                         loc='center')

    pp = PdfPages("duty_chart.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

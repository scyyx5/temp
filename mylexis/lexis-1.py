# reference: https://github.com/cacrespo/pylexis

import pandas as pd
import matplotlib.pyplot as plt


__doc__ = """
PyLexis - A tool to easily plot Lexis Diagrams within Python.
=====================================================================

In demography a Lexis diagram (named after economist and social
scientist Wilhelm Lexis) is a two dimensional diagram that is used to
represent events (such as births or deaths) that occur to individuals
belonging to different cohorts.
"""

"""Common functionality for inputs."""


def check_range_grid(start, end, input):
    """Validates that the input value are between the maximum and minimum
    possible."""
    if start <= input <= end:
        return
    else:
        message = f"""Invalid Data
            Range of allowed grid values: {start} to {end}
            Value: {input}"""
        raise ValueError(message)



class Diagram():
    """ Basic Lexis Diagram """

    def __init__(self,
                 year_start: int, year_end: int,
                 age_start: int, age_end: int):

        self.year_start = year_start
        self.year_end = year_end
        self.age_end = age_end
        self.age_start = age_start

        self.fig, self.ax = plt.subplots(figsize=(year_end - year_start,
                                                  age_end - age_start))
        self.ax.set(xlim=(year_start, year_end),
                    xticks=range(year_start, year_end+1),
                    ylim=(age_start, age_end),
                    yticks=range(age_start, age_end+1))

        plt.grid()

        self.titles()

        for i in range(year_start - age_end, year_end):
            plt.axline((i, age_start),
                       (i + 1, age_start + 1),
                       linewidth=0.3, color='gray')

        


    def titles(self, x_label="Year", y_label="Age", title="Lexis Diagram"):
        """
        Add title and x, y axis labels
        """

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

    def lexis_fill(self, target: str, value: int, color: str):
        """
        Highlight a certain age, year or cohort in the grid.

        :param target: Set "age", "year" or "cohort".
        :param value: This is the value of the *target* selected.
        :param color: Color to fill.
        """

        if target == 'age':
            self.ax.axhspan(value, value + 1, alpha=0.5, color=color)

        if target == 'year':
            self.ax.axvspan(value, value + 1, alpha=0.5, color=color)

        ###########seems it doesn't work
        if target == 'cohort':
            _range = self.year_end - value
            self.ax.fill_between((value, self.year_end),
                                 (self.age_start, _range),
                                 (self.age_start - 1, _range - 1),
                                 color=color, alpha=0.2)

    def add_default(self,age: int, year: int, value: int):
        plt.text(year + 0.5,
            age + 0.3,
            value,
            fontsize=12)


    def save(self,path:str):
        plt.savefig(path)


def dr_lexis():
    #data = pd.read_csv('simDTS2.csv')
    data = pd.read_csv('src/visualization/simDTS2.csv')
    grouped_data = data.groupby(['t','v']).agg(def_num = ('y','sum'),t = 't',v = 'v')

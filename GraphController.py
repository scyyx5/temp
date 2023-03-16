import pandas as pd
import pandas as pd
from datetime import datetime
import sys
sys.path.insert(1, '../../visualization/')
start_date = datetime(2016,1,1)

class GraphController:
    filename = "sim"
    is_color_blind = False
    feature = None
    condition = None
    value = None
    error = "0"
    age_unit = "Month"
    cohort_unit = "Month"
    data = None

    
    def __init__(self, filename="sim", is_color_blind=False, feature=None, condition=None, 
                value=None, error="0", age_unit="Month", cohort_unit="Month", separator=",", decimal="."):
        self.filename =filename
        try:
            self.data = pd.read_csv(f"../../visualization/{filename}.csv", decimal=decimal, sep=separator)
            #self.data = pd.read_csv('../../visualization/' + filename + '.csv',decimal=decimal,sep=separator)
        except:
            self.data = pd.read_csv(f"{filename}.csv", decimal=decimal, sep=separator)
            #self.data = pd.read_csv(filename + '.csv')
        self.is_color_blind = is_color_blind
        self.feature = feature
        self.condition = condition
        self.value = value
        self.error = error
        self.age_unit = age_unit
        self.cohort_unit = cohort_unit
        self.data['pd'] = self.data['pd']
        if(age_unit == "Day"):
            self.data["t"] = self.data["t"]/365.25 * 12 
            self.data = self.data.astype({'t':'int'})
        elif(age_unit == "Year"):
            self.data["t"] = self.data["t"] * 12
            self.data = self.data.astype({'t':'int'})
        if(cohort_unit == "Day"):
            self.data["v"] = self.data["v"]/365.25 * 12
            self.data = self.data.astype({'v':'int'})
            self.data = self.data.iloc[:][self.data["v"] <= 36]   #TODO
        elif(cohort_unit == "Year"):
            self.data["v"] = self.data["v"] * 12
            self.data = self.data.astype({'v':'int'})

    def data_filter(self):
        if self.condition == ">":
            data = self.data.iloc[:][self.data[self.feature] > int(self.value)]
        elif self.condition == "<":
            data = self.data.iloc[:][self.data[self.feature] < int(self.value)]
        else:
            data = self.data
        return data

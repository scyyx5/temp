import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys
sys.path.insert(1, '../../visualization/')
from adjustSlop import adjustSlop

import plotly.express as p
import plotly.offline as py
# py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.figure_factory as ff    

from datetime import datetime
from dateutil.relativedelta import relativedelta


def defaultCohort(data,isColorBlind = False):
    current_month = 20
    #pre processing
    data['cal'] = data['t'] + data['v']
    grouped_cal = data.groupby('cal')[['cal','y','pd']]
    pct_cal = grouped_cal.agg({'cal' : 'count','y':'sum','pd':'sum'})


    data['cal'] = data['t'] + data['v']
    pct_cal = data.groupby(['cal']).agg(number = ('cal','count'),
                                        dr=('y','sum'),edr=('pd','sum'))
    

    pct_cal["dr"] = pct_cal["dr"]/pct_cal["number"]
    pct_cal["edr"] = pct_cal["edr"]/pct_cal['number']

    x_range = [pct_cal.index.min(),pct_cal.index.max()]
    y_range = [pct_cal["dr"].append(pct_cal["edr"]).min(),
               pct_cal["dr"].append(pct_cal["edr"]).max()]
    visualizeData("dr_cal",pct_cal.index[0:current_month],pct_cal["dr"][0:current_month],
                  pct_cal["dr"][0:current_month],x_range,y_range,"calendar time",isColorBlind)
    visualizeData("dr_cal_predicted",pct_cal.index,pct_cal["dr"],
                  pct_cal["edr"],x_range,y_range,"calendar time",isColorBlind)

def defaultAge(data,isColorBlind = False):
    current_age = 10 
    #pre processing
    pct_age = data.groupby(['t']).agg(number = ('t','count'),
                                      dr=('y','sum'),edr=('pd','sum'),std = ('pd','std'))
    pct_age["dr"] = pct_age["dr"]/pct_age["number"]
    pct_age["edr"] = pct_age["edr"]/pct_age["number"]

    x_range = [pct_age.index.min(),pct_age.index.max()]
    y_range = [pct_age["dr"].append(pct_age["edr"]).min(),
               pct_age["dr"].append(pct_age["edr"]).max()]
    visualizeData("dr_age",pct_age.index[0:current_age],pct_age["dr"][0:current_age],
                  pct_age["edr"][0:current_age],x_range,y_range,"age(month)",isColorBlind)
    visualizeData("dr_age_predicted",pct_age.index,pct_age["dr"],
                  pct_age["edr"],x_range,y_range,"age(month)",isColorBlind)
    

    


def visualizeData(filename,x,realy,predictedy,xrange,yrange,xTitle,isColorBlind = False):
    layout = go.Layout(
        paper_bgcolor='rgb(233,233,233)',
        title=
        {
            'y':0.9,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title=xTitle,
            range=xrange
        ),
        yaxis=dict(
            title="default rate(%)",
            range=yrange
        ),
        font=dict(
            size=20
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    trace0 = go.Scatter(
        x = x,
        # y = [ i + float(error) for i in pct_age["dr"][0:current_age]] ,
        y = realy,
        mode = 'lines',
        name = 'default rate'
    )

    age_trace1 = go.Scatter(
        x = x,
        # y = [ i + float(error) for i in pct_age["edr"][0:current_age]],
        y = predictedy,
        mode = 'lines',
        name = 'expected default rate'
    )

    age_fig = go.Figure({'data': [age_trace1,trace0],'layout': layout})

    #age_fig.show()
    # save image
    if(isColorBlind):
        age_fig.update_traces(marker_color="grey")
    py.plot(age_fig,filename = '../../../res/' + filename + '.html',auto_open = False)
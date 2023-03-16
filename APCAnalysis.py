import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score 
from sklearn.model_selection import KFold 
import numpy as np
import pandas as pd
from sklearn import model_selection
import plotly.graph_objs as go
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.offline as py
import sys
sys.path.insert(1, '../../visualization/')
from adjustSlop import adjustSlop
start_date = datetime(2016,1,1)




def apcAnalysis(data,isColorBlind = False,error = "0"):
    para = getEffect(data)
    clf1 = para['clf1']
    clf2 =para['clf2']
    
    len_v = para['len_v']
    len_t = para['len_t']
    len_c = para['len_c']
    v = para['v']
    t = para['t']
    c = para['c']
    z_indices = para['z_indices']
    z_indices2 = para['z_indices2']

    clf_v1 = clf1.coef_[0:len_v-1]
    clf_t1 = clf1.coef_[len_v :len_t + len_v - 1]
    clf_c1 = clf1.coef_[len_t + len_v : len_t + len_v + len_c]
    clf_v2 = clf2.coef_[0:len_v-1]
    clf_t2 = clf2.coef_[len_v :len_t + len_v - 1]
    clf_c2 = clf2.coef_[len_t + len_v : len_t + len_v + len_c]
    #print(v,clf_v1)
    visualizeEffect("cohort",v,clf_v1,clf_v2,isColorBlind,error)
    visualizeEffect("age",t,clf_t1,clf_t2,isColorBlind,error)
    visualizeEffect("period",c,clf_c1,clf_c2,isColorBlind,error)
    theme = ["hot_r","YlGnBu","OrRd","greys"]
    for i in theme:
        visualizeLexisDiagram(i,c,t,z_indices,"apc_")
    theme = ["hot_r","YlGnBu","OrRd","greys"]
    for i in theme:
        visualizeLexisDiagram(i,c,t,z_indices2,"real_apc_")
    



def getEffect(data):
    data['c'] = data['v'] + data['t']
    data = data.groupby(['t','v','c']).agg(number = ('y','count'),
                                        dr=('y','sum'),pd=('pd','sum'))
    data["dr"] = data["dr"]/data["number"]
    data['pd'] = data['pd']/data['number']

    data.index
    #for (i,j,k) in data.index:
        #print(i,j,k)
    t_list,v_list,c_list = [],[],[]
    for (i,j,k) in data.index:
        t_list.append(i)
        v_list.append(j)
        c_list.append(k) 

    data['t'] = t_list 
    data['v'] = v_list 
    data['c'] = c_list

    #data_simplify = data[['v','t','c','pd']]
    yTrain1 = data['pd']
    yTrain2 = data['dr']
    train_encode_simplify = data[['v','t','c']]
    train_encode = pd.get_dummies(train_encode_simplify,
                                columns = ['v','t','c'])
    

    xTrain_encode = train_encode.values

    clf1 = Ridge(alpha=0.001)
    clf1.fit(xTrain_encode,yTrain1)

    clf2 = Ridge(alpha=2)
    clf2.fit(xTrain_encode,yTrain2)

    v = data['v'].unique()
    len_v = len(v)
    t = data['t'].unique()
    len_t = len(t)
    c = data['c'].unique()
    len_c = len(c)

    #for lexis diagram by predicted data

    
    z_indices = []
    for i in t:
        templist = []
        for j in c:
            #vintage = j - i  # vintage = cohort - age
            #print(i,j,v)
            try:
                encode = train_encode.loc[i].loc[j-i]
                y = clf1.predict(encode.values)[0]
            except:
                y = np.nan
            templist.append(y)
        z_indices.append(templist)
    z_indices

    c_indices =[]
    for i in c:
        str_c = start_date + relativedelta(months=i)
        c_indices.append(str_c)

    
    #
    z_indices2 = []
    for i in t:
        list = []
        for j in c:
            #v = j - i  # vintage = cohort - age
            #print(i,j,v)
            try:
                encode = train_encode.loc[i].loc[j-i]
                y = clf2.predict(encode.values)[0]
            except:
                y = np.nan
            list.append(y)
        z_indices2.append(list)
    return { 'len_t': len_t, "len_v": len_v, "len_c":len_c,"clf1": clf1,"clf2":clf2,
            'v':v, 't':t, 'c':c, "z_indices":z_indices,"z_indices2":z_indices2}


def visualizeEffect(graphName,x,predicty,realy,isColorBlind = False,error = "0"):
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
                title= graphName,
                range = [x.min(),x.max()]
            ),
            yaxis=dict(
                title=graphName + " effect"
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


    #sorted_dict = dict(sorted(dict(zip(x.tolist(), dict(zip(predicty.tolist(), realy.tolist())))).items()))
    #sorted_x = list(sorted_dict.keys())
    list_to_sort = list(zip(x.tolist(), predicty.tolist(), realy.tolist()))
    print(list_to_sort)
    list_to_sort.sort(key = lambda a: a[0])
    print(list_to_sort)
    sorted_x = [x[0] for x in list_to_sort]
    sorted_predicty = [x[1] for x in list_to_sort]
    sorted_realy = [x[2] for x in list_to_sort]
    print(sorted_x)
    print(sorted_predicty)
    print(sorted_realy)

    trace0 = go.Scatter(
        x = sorted_x,
        #y = [i + float(error) for i in clf_v],
        #y = clf_v,
        y = adjustSlop(sorted_x,sorted_predicty,error),
        mode = 'lines',
        name = 'APC by predicted data'
    )

    trace1 = go.Scatter(
        x = sorted_x,
        #y = [i + float(error) for i in clf_v],
        #y = clf_v,
        y = adjustSlop(sorted_x,sorted_realy,error),
        mode = 'lines',
        name = 'APC by real data'
    )

    fig = go.Figure({'data': [trace0,trace1],
                            'layout': layout})
    if(isColorBlind):
        fig.update_traces(marker_color="grey")
    py.plot(fig, filename='../../../res/' + graphName + 'effect.html',
            auto_open = False)
    #py.plot(fig, filename=graphName + 'effect.html',
    #        auto_open = False)
    #fig.show()
    

def visualizeLexisDiagram(theme,c,t,z,prefix):
    figure = go.Figure(data=go.Heatmap(
                    z=z,
                    x=c,
                    y=t,
                    zsmooth = "best",     #"fast" | "best" | False
                    colorscale=theme,
                    hoverongaps = True,
                    connectgaps=False))

    figure.update_layout(
                paper_bgcolor='rgb(233,233,233)',
                title="lexis diagram",
                title_x=0.5,
                xaxis_title = "calendar time",
                yaxis_title = "age",
                font=dict(
                    size=20
                ))

    #figure.show()
    py.plot(figure, filename='../../../res/'+ prefix+ 'lexis_diagram_' + theme +'.html',
            auto_open = False)



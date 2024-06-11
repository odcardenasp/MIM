import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import seaborn as sns
import random
import math
import os
import fnmatch
import openpyxl

import sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score


def range_plot(df, num_std):
    mean = df.mean()
    std = df.std()
    lower = mean - (num_std * std)
    upper = mean + (num_std * std)
    return lower, upper

def get_locator(data_type, data_interval):

    if data_type == 'minuto':
        locator_data = mdates.MinuteLocator(interval = data_interval)
    elif data_type == 'hora':
        locator_data = mdates.HourLocator(interval = data_interval)
    elif data_type == 'dia':
        locator_data = mdates.DayLocator(interval = data_interval)
    elif data_type == 'mes':
        locator_data = mdates.MonthLocator(interval = data_interval)
    elif data_type == 'año':
        locator_data = mdates.YearLocator(interval = data_interval)
    elif data_type:
        locator_data = ticker.MultipleLocator(data_interval)
    else:
        locator_data = None
    
    return locator_data

def default_ax_style(ax, title, x_label, y_label, sizelabel, sizetitle, padlabel, padtitle,
                    x_type, y_type, x_interval, y_interval, grid_state):
    
    ax.tick_params( axis = 'x', rotation = 90 )
    ax.set_title(label = title, fontsize = sizetitle, pad = padtitle)
    ax.set_xlabel(xlabel = x_label, fontsize = sizelabel, labelpad = padlabel)
    ax.set_ylabel(ylabel = y_label, fontsize = sizelabel, labelpad = padlabel)

    #ax.tick_params(axis = 'both', labelsize = sizelabel - 5, pad = 0, bottom = True,
    #                left = True)

    loc_x = get_locator(x_type, x_interval)
    loc_y = get_locator(y_type, y_interval)

    ax.xaxis.set_major_locator( loc_x ) if loc_x != None else None
    ax.yaxis.set_major_locator( loc_y )  if loc_y != None else None

    plt.grid(visible = True, color = 'lightgray', linestyle = 'dashdot' if grid_state else
            '')
    plt.subplots_adjust(bottom=0.15, left = 0.1, right = 0.9, top = 0.9)
    ax.tick_params(axis = 'both', labelsize = sizelabel - 5, pad = 0, bottom = True,
                    left = True)
    
def multiple_line_plot(dataframe, opacity_a, opacity_b, split_day, colName):
    
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = ( 25, 13 ) )
    df2 = dataframe.loc[ :, dataframe.columns != colName ]


    for index in dataframe.index:
        if dataframe.loc[ index, colName] <= split_day: 
            ax.plot(df2.columns, df2.loc[ index, : ], color = 'black', alpha = opacity_a)
        else:
            ax.plot(df2.columns, df2.loc[ index, : ], color = 'red', alpha = opacity_b)
    
    default_ax_style(ax, 'Perfiles de Energía en el día', 'Hora', 'kWh', 20, 30, 20, 30,
                    '', 'energia', 1, 10, True)
    fig.savefig( os.path.join(figpath, filename[:-5] + '_5') )
    fig.clf()

def create_mutiple_plot(dataframe, numplots, colName):
    
    df_fn = dataframe.loc[ :, dataframe.columns != colName ]
    df_list = np.array_split(df_fn, numplots, axis = 1)
    df_subsets = [pd.DataFrame(subset) for subset in df_list]

    for i, df_subset in enumerate(df_subsets):
        fig = plt.figure( i + 6 )
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = ( 25, 13 ) )
        df_subset.apply(lambda column: ax.plot(dataframe[colName], column, label = column.name) )
        
        default_ax_style(ax, 'Consumo energía por hora del día', 'Fecha', 'kWh', 20, 30, 20, 30,
                        'dia', 'energia', 10, 10, True)
        plt.legend()
        fig.savefig( os.path.join(figpath, filename[:-5] + str(i+6) ) )
        fig.clf()

def plot_metric(K, scores, metric_name):
        fig = plt.figure(dpi=110, figsize=(9, 5))
        plt.plot(K, scores)
        plt.xticks(K); plt.xlabel('$k$', fontdict=dict(family = 'serif', size = 14));  plt.ylabel(metric_name, fontdict=dict(family = 'serif', size = 14));
        plt.title(f'K vs {metric_name}', fontdict=dict(family = 'serif', size = 18))
        fig.savefig( os.path.join(figpath, filename[:-5] + '_silhouette') )
        fig.clf()


directory_str = 'C:/Users/OscarC/Downloads/Revision 2024'
directory = os.fsencode(directory_str)
figpath = os.path.join(directory_str, 'Data_Analysis')


for file in os.listdir(directory):

    filename = os.fsdecode(file)
    filepath = os.path.join(directory_str, filename)

    if filename.endswith('.xlsx'):

        df = pd.read_excel( filepath )
        print(df.head(3))
        df.dropna(axis = 1, thresh = round(len(df.index) / 2), inplace = True)
        df.dropna(axis = 0, inplace = True)
        print(df.index)

        if df.index[0] > 0:
            new_header = df.iloc[0]
            df = df.iloc[1:]
            df.columns = new_header
            df.reset_index(drop = True, inplace = True)

        print( df.info() )

        df.rename(columns = {'Día/Mes/Año' : 'Date'}, inplace = True)
        df['Date'] =  pd.to_datetime( df['Date'], dayfirst = True, format = '%d/%m/%Y')
        col_names = df.columns.difference(['Date'])
        df = df.astype({col: 'float64' for col in col_names})
        print('medias: ',df.describe())
        #print(df.head(3))
        #df.sort_index(axis = 1, ascending = True, inplace = True)
        #columns_list = sorted(df.iloc[:,1:-1], key=lambda x: int(x[2:]))
        
        temp = df.columns[1:]
        lower, upper = range_plot(df[temp], 2.5)
        df_std = df[~((df[temp] < lower) | (df[temp] > upper)).any(axis=1)]
        
        fig = plt.figure(1)
        fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (25,13))
        ax.plot(df_std['Date'], df_std['Total Día'])
        default_ax_style(ax, 'Consumo energía en el tiempo', 'Time', 'kWh', 20, 30, 20, 30,
                        'dia', 'energia', 10, 100, True)
        fig.savefig( os.path.join(figpath, filename[:-5] + '_1') )
        fig.clf()


        df_mk = df_std.iloc[ :,:-1 ]
        df_mk['Date'] = df_mk['Date'].dt.strftime('%d/%m/%y')
        df_mk.set_index(keys = 'Date', inplace = True)
        
        fig = plt.figure(2)
        fig, ax1= plt.subplots(nrows = 1, ncols = 1, figsize = (20,45))
        ax1 = sns.heatmap( df_mk, robust = True, cmap = 'turbo')
        default_ax_style(ax1, 'GreenChart 24 horas', 'Hora del día', 'Fecha', 20, 30, 20, 30,
                        '', '', 1, 1, False )
        fig.savefig( os.path.join(figpath, filename[:-5] + '_2') )
        fig.clf()

        fig = plt.figure(3)
        fig, ax2= plt.subplots(nrows = 1, ncols = 1, figsize = (20,45))
        ax2 = sns.heatmap( df_mk.iloc[ :, np.r_[0:5, 21:24] ], robust = True, cmap = 'turbo')
        default_ax_style(ax2, 'GreenChart Nocturno', 'Hora del día', 'Fecha', 20, 30, 20, 30,
                        '', '', 1, 1, False )
        fig.savefig( os.path.join(figpath, filename[:-5] + '_3') )
        fig.clf()

        fig = plt.figure(4)
        fig, ax3 = plt.subplots(nrows = 1, ncols = 1, figsize = (20,45))
        ax3 = sns.heatmap( df_mk.iloc[ :, 9:20 ], robust = True, cmap = 'turbo')
        default_ax_style(ax3, 'GreenChart Diurno', 'Hora del día', 'Fecha', 20, 30, 20, 30,
                        '', '', 1, 1, False )
        #ax.tick_params(axis = 'both', labelsize = 30 - 5, pad = 0, bottom = True, left = True)
        fig.savefig( os.path.join(figpath, filename[:-5] + '_4') )
        fig.clf()

        multiple_line_plot(df_std.iloc[:,:-1], 0.05, 0.25, datetime(2023, 8, 15), 'Date') 
        create_mutiple_plot(df_std.iloc[ :, :-1 ], 3, 'Date')
        print('Terminé')


# ____________________ANÁLISIS DE DATOS CON MACHINE LEARNING________________________

        scaler = MinMaxScaler(feature_range = (0,1) )
        df_mk_sc = scaler.fit_transform( df_mk )
        print( df_mk_sc[0,:] )
        silhouette_scores = []
        n_cluster_list = np.arange(2,15).astype(int)

        for n_cluster in n_cluster_list:
            kmeans = KMeans( n_clusters = n_cluster )
            kmeans = kmeans.fit(df_mk_sc)
            y = kmeans.predict( df_mk_sc )
            score = silhouette_score(df_mk_sc, y)
            silhouette_scores.append( score )
            
        silhouette_scores_arr = np.array(silhouette_scores)
        select_nclusters = n_cluster_list[ np.argmax(silhouette_scores_arr) ]
        plot_metric(n_cluster_list, silhouette_scores, 'Coeficiente de silueta ' + filename[:-5])

        kmeans = KMeans( n_clusters = select_nclusters )
        cluster_found = kmeans.fit_predict( df_mk_sc )
        cluster_found_sr = pd.Series( cluster_found, name = 'cluster' )
        df_mk = df_mk.set_index(cluster_found_sr, append = True )
        print( df_mk.head(5) )

        fig = plt.figure()
        fig, ax= plt.subplots(1,1, figsize=(25,13))
        color_list = ['blue','red','green', 'purple', 'orange', 'yellow']
        cluster_values = sorted(df_mk.index.get_level_values('cluster').unique())
        print('Estos son los cluster values: ', cluster_values )

        for cluster, color in zip(cluster_values, color_list):
            
            df_mk.xs(cluster, level = 1).T.plot( ax = ax, legend = False, alpha = 0.05, 
                                            color = color, label = f'Cluster {cluster}')
            df_mk.xs(cluster, level = 1).median().plot(
                ax = ax, color = color, alpha = 0.9, ls='--')
            
        default_ax_style(ax, 
                        'Patrones Consumo ' + filename[:-5] + f' k = {np.max(silhouette_scores_arr):.2f}',
                        'Hora', 'kWh', 20, 30, 20, 30, '', 'energia', 1, 10, True )
        fig.savefig( os.path.join(figpath, filename[:-5] + '_ML') )
        fig.clf()

        print(f'Cluster : {cluster} \n', df_mk.xs(cluster, level = 1).head(5))
            
        df_labels = df_mk
        df_labels['Total'] = df_mk.sum(axis = 1)
        df_labels = df_mk.reset_index(level = ['cluster'])
        print(df_labels.head(5))


        fig = plt.figure()
        fig, ax = plt.subplots(figsize = (25, 18 ) )
        ax.scatter(df_labels.index, df_labels['Total'], c = df_labels['cluster'])
        ax.tick_params(axis = 'x', rotation = 90)
        default_ax_style(ax, 
                        'Scatter Consumo '+ filename[:-5],
                        'Dia', 'kWh', 20, 30, 20, 30, 'Dia', 'energia', 10, 50, True)
        fig.savefig( os.path.join(figpath, filename[:-5] + '_Scatter') )
        fig.clf()

        """
        dfs = dict( tuple( df_mk.groupby( level = 1 ) ) )
        keys = dfs.keys()
        print('mi tipo es: ', type(dfs[0]) )
        df_total = df_mk
        df_total['Total'] = df_mk.sum(axis = 1)
        df_total = df_total['Total']

        for k, df in dfs.items():
            df['Total'] = df.sum(axis = 1)
            df = df['Total']
            df.index = df.index.droplevel(1)
            dfs[k] = df
            print( df.sample(5) )

        fig = plt.figure()
        #a = sns.lineplot(data = df)
        #plt.xticks( rotation = 90 )
        #plt.tight_layout()
        temp0 = pd.DataFrame(dfs.get(0))
        temp1 = pd.DataFrame(dfs.get(1))

        print('MI PRUEBA: \n', temp0['Total'] )   
        fig, ax = plt.subplots(figsize = (25, 23 ) )
        ax.scatter(temp0.index, temp0['Total'], c = 'red')
        ax.scatter(temp1.index, temp1['Total'], c = 'blue')
        ax.tick_params(axis = 'x', rotation = 90)
        #ax.xaxis.set_ticks(pd.Index(df_mk).get_level_values(0))
        default_ax_style(ax, 
                        'Patrones Consumo ' + filename[:-5] + f' k = {np.max(silhouette_scores_arr):.2f}',
                        'Dia', 'kWh', 20, 30, 20, 30, '', 'energia', 10, 50, True )
        
        plt.show()

        print('somos las keys: ', keys)
        df2 = df_mk.groupby(level = 1).size()
        print( df2.head(5) )

        df3 = df_mk.groupby(level = 1).mean()
        print( df3.head(5) )
        """

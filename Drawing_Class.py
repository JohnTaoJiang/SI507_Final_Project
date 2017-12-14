import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools


class Visual(object):

    def __init__(self):
        pass

    def BarChart(self, x_ls1, y_ls1, x_ls2, y_ls2):
        trace0 = go.Bar(
            x = x_ls1,
            y = y_ls1,
            text = y_ls1,
            textposition = 'auto',
            marker=dict(
                color=['rgba(204,204,204,1)', 'rgba(222,45,38,0.8)',
                       'rgba(204,204,204,1)', 'rgba(204,204,204,1)',
                       'rgba(204,204,204,1)']),
        )

        trace1 = go.Bar(
            x = x_ls2,
            y = y_ls2,
            text = y_ls2,
            textposition = 'auto',
            marker=dict(
                color=['rgba(158,202,225,1)', 'rgba(222,45,38,0.8)',
                       'rgba(158,202,225,1)', 'rgba(158,202,225,1)',
                       'rgba(158,202,225,1)'],
                line=dict(
                        color='rgb(8,48,107)',
                        width=1.5),
            ),
        )

        fig = tools.make_subplots(rows=1, cols=2, subplot_titles = ('Average Rating for Each College',
            'Ratio of Restaurants rated above 4 for Each College'))

        fig.append_trace(trace0, 1, 1)
        fig.append_trace(trace1, 1, 2)

        plot(fig, filename='BarChart.html')

    def Pie_Chart(self, ls_labels_ls, ls_rat_ls):
        fig = {
            'data' : [
                {
                    'values': ls_rat_ls[0],
                    'labels': ls_labels_ls[0],
                    'text' : 'Popular Categories',
                    'textposition' : 'inside',
                    'domain': {'x' : [0, 0.3]},
                    'name' : '',
                    'hoverinfo' : 'label+percent+name',
                    'hole' : .4,
                    'type' : 'pie'
                },
                {
                    'values' : ls_rat_ls[1],
                    'labels' : ls_labels_ls[1],
                    'text' : 'Additional Services',
                    'textposition' : 'inside',
                    'domain' : {'x' : [0.33, 0.63]},
                    'name' : '',
                    'hoverinfo' : 'label+percent+name',
                    'hole' : .4,
                    'type' : 'pie'
                },
                {
                    'values' : ls_rat_ls[2],
                    'labels' : ls_labels_ls[2],
                    'text' : 'Price',
                    'textposition' : 'inside',
                    'domain' : {'x' : [0.66, 1]},
                    'name' : '',
                    'hoverinfo' : 'label+percent+name',
                    'hole' : .4,
                    'type' : 'pie'
                }
            ],
            'layout' : {
                'title' : 'Categories, Services & Prices of Popular Restaurants',
                'annotations': [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Categories",
                        "x": 0.10,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Additional Services",
                        "x": 0.48,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Prices",
                        "x": 0.86,
                        "y": 0.5
                    }
                ]
            }
        }
        plot(fig, filename = 'Pie_Chart.html')
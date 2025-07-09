import justpy as jp
import pandas
import numpy
from datetime import datetime
from pytz import utc

spline_chart_def = """
{
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Average Rating by Week'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Average Rating',
        data: [
            [0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]
        ]

    }]
}
"""

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
data["Week"] = data["Timestamp"].dt.strftime("%Y-%U")
week_average = data.groupby(["Week"]).mean(numeric_only=True)

def app():
    wp = jp.QuasarPage() # Creating QuasarPage instance
    h1 = jp.QDiv(a=wp, text="Data Analysis of Reviews",
        classes="text-h3 text-center q-pa-lg")
    p1 = jp.QDiv(a= wp, text="These graph represent reviews analysis by week",
        classes="text-body1 text-center q-pa-lg")
    hc = jp.HighCharts(a=wp, options=spline_chart_def)
    
    hc.options.xAxis.categories = list(week_average.index)
    hc.options.series[0].data = list(week_average["Rating"])
    return wp

jp.justpy(app)
import justpy as jp
import pandas
import numpy
from datetime import datetime
from pytz import utc

stream_chart_def = """
{
    chart: {
        type: 'streamgraph',
        marginBottom: 30,
        zooming: {
            type: 'x'
        }
    },

    title: {
        floating: true,
        align: 'left',
        text: 'Number of Reviews by Course'
    },
    subtitle: {
        floating: true,
        align: 'left',
        y: 30,
        text: 'Source: <a href="https://www.olympedia.org/statistics">olympedia.org</a>'
    },

    xAxis: {
        maxPadding: 0,
        type: 'category',
        crosshair: true,
        labels: {
            align: 'left',
            reserveSpace: false,
            rotation: 270
        },
        lineWidth: 0,
        margin: 20,
        tickWidth: 0
    },

    yAxis: {
        visible: false,
        startOnTick: false,
        endOnTick: false,
        minPadding: 0.1,
        maxPadding: 0.15
    },

    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            label: {
                minFontSize: 5,
                maxFontSize: 15,
                style: {
                    color: 'rgba(255,255,255,0.75)'
                }
            },
            accessibility: {
                exposeAsGroupOnly: true
            }
        }
    },
    exporting: {
        sourceWidth: 800,
        sourceHeight: 600
    }

}
"""

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
data["Month"] = data["Timestamp"].dt.strftime("%Y-%m")
month_average = data.groupby(["Month", "Course Name"])["Rating"].count().unstack()

def app():
    wp = jp.QuasarPage() # Creating QuasarPage instance
    h1 = jp.QDiv(a=wp, text="Data Analysis of Reviews",
        classes="text-h3 text-center q-pa-lg")
    p1 = jp.QDiv(a= wp, text="These graph represent reviews analysis by month by course",
        classes="text-body1 text-center q-pa-lg")
    
    hc = jp.HighCharts(a=wp, options=stream_chart_def)
    hc.options.xAxis.categories = list(month_average.index)
    hc_data = [{
        "name":course_name, 
        "data":[course_rating for course_rating in month_average[course_name]]} 
        for course_name in month_average.columns]
    hc.options.series = hc_data
    return wp

jp.justpy(app)
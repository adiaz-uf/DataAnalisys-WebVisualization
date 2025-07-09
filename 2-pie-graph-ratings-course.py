import justpy as jp
import pandas
import numpy
from datetime import datetime
from pytz import utc

stream_chart_def = """
{
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Number of Ratings by Course'
    },
    subtitle: {
        text:
        'Source:<a href="https://www.mdpi.com/2072-6643/11/3/684/htm" target="_default">MDPI</a>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: [{
                enabled: true,
                distance: 20
            }, {
                enabled: true,
                distance: -40,
                format: '{point.percentage:.1f}',
                style: {
                    fontSize: '1.2em',
                    textOutline: 'none',
                    opacity: 0.7
                },
                filter: {
                    operator: '>',
                    property: 'percentage',
                    value: 10
                }
            }]
        }
    },
    series: [
        {
            name: 'Course',
            colorByPoint: true,
            data: [
                {
                    name: 'Water',
                    y: 55.02
                },
                {
                    name: 'Fat',
                    sliced: true,
                    selected: true,
                    y: 26.71
                },
                {
                    name: 'Carbohydrates',
                    y: 1.09
                },
                {
                    name: 'Protein',
                    y: 15.5
                },
                {
                    name: 'Ash',
                    y: 1.68
                }
            ]
        }
    ]
}
"""

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
share = data.groupby(["Course Name"])["Rating"].count()

def app():
    wp = jp.QuasarPage() # Creating QuasarPage instance
    h1 = jp.QDiv(a=wp, text="Data Analysis of Reviews",
        classes="text-h3 text-center q-pa-lg")
    p1 = jp.QDiv(a= wp, text="These graph represent reviews analysis by month by course",
        classes="text-body1 text-center q-pa-lg")
    
    hc = jp.HighCharts(a=wp, options=stream_chart_def)
    hc.options.xAxis.categories = list(share.index)
    hc_data = [{
        "name":course_name, 
        "y":course_rating} 
        for course_name, course_rating in zip(share.index, share)]
    hc.options.series[0].data = hc_data
    return wp

jp.justpy(app)
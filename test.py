import pygal                                                       # First import pygal
from datetime import datetime, timedelta
datey = pygal.DateY(x_label_rotation=20)
datey.add("Visits", [
    (datetime(2013, 1, 2), 300),
    (datetime(2013, 1, 12), 412),
    (datetime(2013, 2, 2), 823),
    (datetime(2013, 2, 22), 672)
])
datey.render_to_file('test.svg')
#bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file

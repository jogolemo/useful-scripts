import pandas as pd
import pycurl
import certifi
import re
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict
from HTMLParser import HTMLParser
try:
        from io import BytesIO
except ImportError:
        from StringIO import StringIO as BytesIO


class htmlDates(HTMLParser):
        def __init__(self):
                HTMLParser.__init__(self)
                self.recording = False
                
        def handle_starttag(self, tag, attrs):
                if tag == 'br':
                        self.recording = True

        def handle_endtag(self, tag):
                if tag == 'br':
                        self.recording = False

        def handle_data(self, data):
                if self.recording:
                        dates_and_files.append(data)

def write_file(files):     
        with open('C:/Users/gisuser/desktop/projects/curl/%s' % files, 'wb') as f:
                c = pycurl.Curl()
                c.setopt(pycurl.CAINFO, certifi.where())
                c.setopt(c.URL, 'https://metadata.boem.gov/geospatial/'+files)
                c.setopt(c.WRITEDATA,f)
                c.perform()
                c.close()



# operating on curl object c
buffer = BytesIO()
c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where()) # needed for this particular URL
c.setopt(c.URL, 'https://metadata.boem.gov/geospatial/')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

# Creates string representing URL's HTML 
body = buffer.getvalue()

# Parses html text into dates and associated files
dates_and_files = []
parser = htmlDates()
parser.feed(body)
dates = [item.replace('  ',' ') for item in dates_and_files[0:][::2]]
datetimes = [datetime.strptime(re.search('\d+/\d+/\d+ \d+:\d+ [AP]M',i).group(), '%m/%d/%Y %I:%M %p') for i in dates]
files = dates_and_files[1:][::2]

# creates dataframe from dates and files (indexing these values will be helpful)
meta = pd.DataFrame({'dates':datetimes,'files': files})

# Time to start checking for new files that were uploaded
time_now = datetime.now() #time_now = datetime(2018,3,15,10,51)
start_time = time_now - timedelta(days=1)

# Find associated files
trial = meta.files.loc[meta.dates > start_time]

# store files wherever you would like to put them.
# (please refer to write_file function above)
trial.apply(write_file)

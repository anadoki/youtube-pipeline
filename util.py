import re
import pandas as pd

def duration_parse(duration): 
    try:
        duration_regex = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
        if not isinstance(duration,str):
            return 0
        pattern = re.match(duration_regex, duration)
        if not pattern:
            return 0
        hours = int(pattern.group(1)) if pattern.group(1) else 0
        minutes = int(pattern.group(2)) if pattern.group(2) else 0
        seconds = int(pattern.group(3)) if pattern.group(3) else 0
        return hours * 60 + minutes + seconds/60

    

    except Exception as e:
        return 0

def which_bucket(hours):
    try:
        return pd.cut(hours,
                  bins=[-1, 5, 11, 17, 21, 24],
                  labels=["Late Night", "Morning", "Afternoon", "Evening", "Night"])
    except:
        return "NA"



                  


def aggregateSnowfall(t):
    """Reads numbers from a file into a dictionary of segments of snowfall 
    heights and then returns the dictionary of snowfall heights and their 
    frequency.

    Args: t (str): File name
    Returns: None"""
    file = open(t, "r")

    # dictionary of snowfall heights
    snowfall_heights = {"1_10":0, 
                        "11_20":0,
                        "21_30":0,
                        "31_40":0,
                        "41_50":0}
    
    for line in file:
        # convert line to int
        line = int(line)

        if line >= 1 and line <= 10:
            snowfall_heights["1_10"] += 1
        elif line >= 11 and line <= 20:
            snowfall_heights["11_20"] += 1
        elif line >= 21 and line <= 30:
            snowfall_heights["21_30"] += 1
        elif line >= 31 and line <= 40:
            snowfall_heights["31_40"] += 1
        elif line >= 41 and line <= 50:
            snowfall_heights["41_50"] += 1
            
    return snowfall_heights
import json
# Extraction
# Reading Files

# returns an array containing dictionaries with keys corresponding to the given collumn label
def csvReader(path, ignore=False):
    f = open(path, encoding='utf-8')
    
    # separates file into rows and collumns
    
    raw = []
    for row in f.readlines():
        raw.append(row.split('\t'))
    
    # stores the previous element of the iteration
    previous = []
    countLine = 2
    for line in raw:
        row = line[0].rstrip().split(';')
        
        if len(previous) == 0:
            previous = row

        if  len(row) == 1:
            raise Exception('Unreliable number of collumns\nFile: %s\nLine: %s' % (path, countLine))
        
        if len(previous) != len(row):
            raise Exception('Inconsistent number of collumns\nFile: %s\nLine: %s' % (path, countLine))
    
        # stores the previous set for comparison
        previous = row
        countLine += 1

    print('File Structure: OK')

    # removing and returning the header for collumn identification
    header = raw.pop(0)[0].rstrip().split(';')

    output = []
  
    # stores everything in a dictionary containing the collumns and items assigned to them.
    for row in raw:
        dictRow = dict()
        values = row[0].rstrip().split(';')
        for i in range(len(header)):
            label = header[i]
            dictRow[label] = values[i]
            
        output.append(dictRow)
    
    return output

# round cleanup is a rounds_teams specific function, its aims are:
#   checking and converting collumn contents
#   assigning key constraints and data types
#   validating key constraints and data types
#   checking and alerting for source structure
def roundCleanup(table):
    
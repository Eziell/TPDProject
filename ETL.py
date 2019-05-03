import json
from datetime import datetime
# Extraction
# Reading Files

# returns an array containing dictionaries with keys corresponding to the given collumn label
def csvReader(path, ignore=False):
    f = open(path, encoding='cp850')

    # separates file into rows and collumns

    raw = []
    for row in f.read().rstrip().split('\n'):
        raw.append(row.rstrip().split('\t'))

    # stores the previous element of the iteration
    previous = []
    countLine = 2
    for line in raw:
        if len(previous) == 0:
            previous = line

        if  len(line) == 1:
            raise Exception('Unreliable number of collumns\nFile: %s\nLine: %s' % (path, countLine))

        if len(previous) != len(line):
            raise Exception('Inconsistent number of collumns\nFile: %s\nLine: %s' % (path, countLine))

        # stores the previous set for comparison
        previous = line
        countLine += 1

    print('File Structure: OK')

    # removing and returning the header for collumn identification
    header = raw.pop(0)

    output = []

    # stores everything in a dictionary containing the collumns and items assigned to them.
    for row in raw:
        dictRow = dict()
        for i in range(len(header)):
            dictRow[header[i]] = row[i]

        output.append(dictRow)

    return output

#teste = csvReader('TPD-CSV/concorrentes.csv')
#print(teste[1].keys())

# concorrentes cleanup is a concorrentes specific function, its aims are:
#   checking and converting collumn contents
#   assigning key constraints and data types
#   validating key constraints and data types
#   checking and alerting for source structure
#   organizing data according
#   This table must contain:
#       id = Primary Key, Integer
#       nickname = String
#       birthdate = DateTime
#       address = string
#       agegroup = String (two integers separated by a dash ("-"))
#       gender = String (May be either Masculine or Feminine)
#       club = String
#       region = String
#       startdate = DateTime
def concorrentesCleanup(table, ignoreDuplicates = True):
    # table structure as of 03-05-2019
    keys = ['id', 'nickname', 'birthdate', 'address', 'agegroup', 'gender', 'club', 'region', 'startdate']
    dateFormat = '%Y-%m-%d'
    gender = ['Masculino', 'Feminino']
    # array to store primary keys and test constraints
    primaryKeys = list()

    # preparing a new array to accept the parsed values
    output = []
    for line in table:
        # checking integrity of collumn names
        if keys != list(line.keys()):
                raise ValueError("Collumn names not valid.")

        # parsing key contents to proper format
        outputLine = dict()
        try:
            outputLine['id'] = int(line['id'])
            outputLine['nickname'] = str(line['nickname']).rstrip()
            outputLine['birthdate'] = datetime.strptime(line['birthdate'].split(' ')[0], dateFormat)
            outputLine['address'] = str(line['address']).rstrip()
            outputLine['agegroup'] = str(line['agegroup']).rstrip()
            outputLine['gender'] = str(line['gender']).rstrip()
            outputLine['club'] = str(line['club']).rstrip()
            outputLine['region'] = str(line['region']).rstrip()
            outputLine['startdate'] = datetime.strptime(line['startdate'].split(' ')[0], dateFormat)
        except Exception:
            raise Exception("Something went wrong with value format parsing.")

        # checking gender contents
        try:
            gender.index(outputLine['gender'])
        except ValueError:
            raise ValueError("Gender may be assigned to an invalid choice.")

        # standardizing NULL values for club
        if outputLine['club'] == 'NULL':
            outputLine['club'] = 'Not specified'

        primaryKeys.append(line.get('id'))
        output.append(outputLine)
    # cheking for duplicates with the same primary key
    for key in primaryKeys:
        if primaryKeys.count(key) > 1:
            if ignoreDuplicates == True:
                raise Exception('Primary Key constraints do not hold up')
            else:
                raise Warning('Duplicates found in file, use of proper candidate keys is highly advised!')


    # everything with structure, domains, constraints ok!
    return(output)


f = csvReader('TPD-CSV/concorrentes.csv')
print(concorrentesCleanup(f)[0])

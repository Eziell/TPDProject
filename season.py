import Extraction as ext 
from datetime import datetime 

def createSeasonDimension(path='TPD-CSV/LigaRecord/'):
    # season is updated yearly, the "rounds.csv" file should contain the necessary information 
    # to construct this dimension.

    # season is updated every year day 07-01, and expected to end the next year's june.
    seasonStartDay = '07-01'
    seasonEndDay = '06-30'
    # reading the stored .csv file to an array of dicts
    rawTable = ext.csvReader(path + 'rounds.csv')
    formatTable = ext.tableCleanup(rawTable)

    season = dict()
    season['Season Name'] = formatTable[1]['season']
    # retrieving year from rounds.csv
    year = (formatTable[1]['start_date']).year
    season['Season Start Date'] = str('%i-%s' % (year, seasonStartDay))
    season['Season End Date'] = str('%i-%s' % (year+1, seasonEndDay))
    seasonUpdatedM = 'Updated game version'
    seasonDeprecatedM = "Deprecated game version"
    season['Season Has Updated Game Version'] = seasonUpdatedM if year >= 2015 else seasonDeprecatedM
    variableWeekdayM = "Variable weekday publish date"
    fixedWeekdayM = "Fixed weekday publish date"
    season['Season Has Variable Weekday Publish Date'] = variableWeekdayM if year >= 2015 else fixedWeekdayM
    season['Team Player Transfers Allowed Per Month'] = 1 if year >= 2015 else 2

    return season

# should be used with dimension as dict from the function createSeasonDimension()
def assignCandidateKey(key, dimension):
    dimension['Season Key (PK)'] = key

    return dimension
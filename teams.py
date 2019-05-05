import Extraction as ext 
from datetime import datetime 

def createTeamsDimension(path='TPD-CSV/LigaRecord/'):
    rawTable = ext.csvReader(path + 'teams.csv')
    formatTable = ext.tableCleanup(rawTable)

    teams = list()
    # going through every entry from the relational database.
    for line in rawTable:
        teamsDict = dict()
        teamsDict['Team Natural ID'] = line['id']
        teamsDict['Team Name'] = line['name']
        teamsDict['Team Create Date'] = line['createdate']
    return 

# should be used with dimension as dict from the function createSeasonDimension()
def assignCandidateKey(key, dimension):
    dimension['Team Key (PK)'] = key

    return dimension


print(createTeamsDimension())

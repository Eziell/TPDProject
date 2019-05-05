import extraction as ext 
from datetime import datetime 

def createTeamsDimension(path='TPD-CSV/LigaRecord/'):
    rawTable = ext.csvReader(path + 'teams.csv')
    teamsTable = ext.tableCleanup(rawTable)

    # a informação Team in League vai sair da tabela user_details_logins
    rawTable = ext.csvReader(path + 'user_details_logins.csv')
    detailsTable = ext.tableCleanup(rawTable)

    # getting users from user_details_logins.csv
    user = dict()
    for line in detailsTable:
        user[line['id_user']] = line['in_league']

    # creating array of dicts with user as key, in_league value in first position and team_id in proceeding posetions
    teams = list()
    
    # going through every entry from the relational database.
    for line in teamsTable:
        teamsDict = dict()
        teamsDict['Team Natural ID'] = line['id']
        teamsDict['Team Name'] = line['name']
        teamsDict['Team Create Date'] = line['createdate']
        teamsDict['Team Origin'] = line['origin']
        teamsDict['Team Is Paid'] = 'Team is paid' if line['is_paid']==1 else 'Team is free'
        teamsDict['Team In League'] = 'Team in league' if user[line['id_user']]==1 else 'Team not in league'
        
        #appending to output
        teams.append(teamsDict)
    
    return teams

# should be used with dimension as dict from the function createSeasonDimension()
def assignCandidateKey(key, dimension):
    dimension['Team Key (PK)'] = key

    return dimension
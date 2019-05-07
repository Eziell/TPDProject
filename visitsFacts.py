import extraction as ext    
import date, season
def createVisitsFacts(path='TPD-CSV/'):
    rawTable = ext.csvReader(path + 'LigaRecord/user_details_logins.csv')
    logins = ext.tableCleanup(rawTable)

    # retrieving rounds dictionary
    rawTable = ext.csvReader(path + 'LigaRecord/rounds.csv')
    rounds = ext.tableCleanup(rawTable)

    # compativel com tabela user_details_logins.csv
    weekdayToNumber = dict()
    weekdayToNumber['logins_monday'] = 1
    weekdayToNumber['logins_tuesday'] = 2
    weekdayToNumber['logins_wednesday'] = 3
    weekdayToNumber['logins_thursday'] = 4
    weekdayToNumber['logins_friday'] = 5 
    weekdayToNumber['logins_saturday'] = 6
    weekdayToNumber['logins_sunday'] = 7

    # loading current season dateDimension
    dateDict = date.createDateDimension()
    # loading seasonDimension
    seasonDict = season.createSeasonDimension()

    visitsFactsList = list()
    for line in logins:
        # removing season foreign key
        seasonLink = foreignCheck(seasonDict, line['season'], 'Season Name', 'Season Key (PK)')
        # retrieving user
        user = line['id_user']
        
        weekday = weekdayToNumber.keys()

        for collumn in weekday:
            # retrieving logins per day
            logins = line[collumn]
            round = line['round_order']

            
            #dict for temporary storage
            loginsDict = dict()
            
            # linking with user
            loginsDict['User Key (FK)'] = user
            # linking with season
            loginsDict['Season Key (FK)'] = seasonLink
            # dateLink
            dateLink = foreignCheck(dateDict, [round, weekdayToNumber[weekday]], ['Round Number', 'Weekday'], 'Date Key (PK)')
            loginsDict['Date Key (FK)'] = dateLink
            
            ## falta o durable user key
            loginsDict['Visit Count'] = logins

            visitsFactsList.append(loginsDict)
            
    return visitsFactsList

            

            

def foreignCheck(dict, valueToCompare, keyToCompare, keyToRetrieve):
    for key in dict:
        if len(keyToCompare) == 1:
            if key[keyToCompare] == valueToCompare:
                return key[keyToRetrieve]
        elif len(keyToCompare) == 2:
            if key[keyToCompare[0]] == valueToCompare[0] and key[keyToCompare[1]] == valueToCompare[1]:
                return key[keyToRetrieve]

createVisitsFacts()
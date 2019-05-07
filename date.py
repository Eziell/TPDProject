import extraction as ext 
from datetime import datetime 

def createDateDimension(path='TPD-CSV/'):
    rawTable = ext.csvReader(path + 'LigaRecord/rounds.csv')
    roundsTable = ext.tableCleanup(rawTable)

    rawTable = ext.csvReader(path + 'classicos.csv')
    classicosTable = ext.tableCleanup(rawTable)

    # creating array of dicts with user as key, in_league value in first position and team_id in proceeding posetions
    dates = list()
    # assigning the selected year gregorian day of the first day in the year
    gregorianYear = roundsTable[0]['start_date'].toordinal()
    
    
    candidateKey = 1
    # going through every entry from the relational database.
    for n in range(365):
        dateDict = dict()
        # properly setting up the day and returning the full date
        date = datetime.fromordinal(gregorianYear + n)
        dateDict['Date Key (PK)'] = candidateKey
        candidateKey += 1
        ##
        dateDict['Day'] = date.day
        dateDict['Day Of Month'] = date.day
        dateDict['Weekday'] = date.weekday() + 1
        dateDict['Calendar Weekday'] = getCalendarWeekday(date.weekday())
        dateDict['Month'] = date.month
        dateDict['Calendar Month'] = getCalendarMonth(date.month)
        dateDict['Year'] = date.year
        dateDict['Date Full'] = date.date().strftime('%Y-%m-%d')
        dateDict['Weekend Indicator'] = 'Weekday' if date.weekday() <= 4 else 'Weekend'
        dateDict['Season Stage Indicator'] = getStageIndicator(date, roundsTable)
        # Não temos informação sobre isto
        # dateDict['Turn'] = turn(date, roundsTable)
        # dateDict['Turn Indicator'] = turnIndicator(date, roundsTable)
        dateDict['Round Number'] = roundNumber(date, roundsTable)
        dateDict['Round Lifecycle Indicator'] = roundLifecycleIndicator(date, roundsTable)
        dateDict['Lifecycle Round Number'] = roundNumber(date, roundsTable)
        dateDict['Round Includes Classic Match'] = classicMatch(date, classicosTable)
        dateDict['Is Winter'] = 'Winter transfer season' if date.month == 2 else 'Non winter transfer season'
        
        #appending to output
        dates.append(dateDict)

    return dates

# should be used with dimension as dict from the function createSeasonDimension()
def assignCandidateKey(key, dimension):
    dimension['Date Key (PK)'] = key

    return dimension

def getCalendarWeekday(weekday):
    CalendarWeekday = dict()
    CalendarWeekday[0] = 'Segunda-Feira'
    CalendarWeekday[1] = 'Terça-Feira'
    CalendarWeekday[2] = 'Quarta-Feira'
    CalendarWeekday[3] = 'Quinta-Feira'
    CalendarWeekday[4] = 'Sexta-Feira'
    CalendarWeekday[5] = 'Sábado'
    CalendarWeekday[6] = 'Domingo'

    return CalendarWeekday.get(weekday)

def getCalendarMonth(month):
    CalendarMonth = dict()
    CalendarMonth[1] = 'Janeiro'
    CalendarMonth[2] = 'Fevereiro'
    CalendarMonth[3] = 'Março'
    CalendarMonth[4] = 'Abril'
    CalendarMonth[5] = 'Maio'
    CalendarMonth[6] = 'Junho'
    CalendarMonth[7] = 'Julho'
    CalendarMonth[8] = 'Agosto'
    CalendarMonth[9] = 'Setembro'
    CalendarMonth[10] = 'Outubro'
    CalendarMonth[11] = 'Novembro'
    CalendarMonth[12] = 'Dezembro'

    return CalendarMonth.get(month)

def getStageIndicator(date, roundsTable):
    startStage = roundsTable[0]
    endStage = roundsTable[-1]
    if startStage['start_date'] > date:
        return 'Before game starts'
    elif startStage['start_date'] <= date and startStage['end_date'] >= date:
        return 'First round'
    elif startStage['end_date'] < date and endStage['start_date'] > date:
        return 'Season ongoing'
    elif endStage['start_date'] <= date and endStage['end_date'] >= date:
        return 'Last round'
    elif endStage['end_date'] < date: 
        return 'After game ends.'

def turn(date, roundsTable):
    # first turn starts and ends with first round and by the end of january.
    # second turn starts with previous end and ends with last turn.
    startStage = roundsTable[0]
    endStage = roundsTable[-1]
    if startStage['start_date'] <= date and date.month < 2:
        return 1
    elif startStage['start_date'] <= date and date.month > startStage['start_date'].month and date.moth <= 12:
        return 1
    elif startStage['end_date'] < date and endStage['end_date'] >= date:
        return 2
    else:
        return 0

def turnIndicator(date, roundsTable):
    for line in roundsTable:
        if line['start_date'] >= date and line['end_date'] <= date:
            if line['start_date'] == date:
                return 'Turn start'
            elif line['end_date'] == date: 
                return 'Turn finish'
            else:
                return 'Turn ongoing'
    
    # if no round is captured
    return 'Not a turn'

def roundNumber(date, roundsTable):
    for line in roundsTable:
        if line['start_date'] >= date:
            return line['order']
    return 0

def roundLifecycleIndicator(date, roundsTable):
    for line in roundsTable:
        try:
            if line['start_date'] <= date and line['publish_date'] >= date:
                if line['start_date'] == date:
                    return 'Day bets start '
                elif line['end_date'] == date: 
                    return 'Day bets end'
                elif line['publish_date'] == date:
                    return 'Results publication day'
                elif line['end_date'] < date:
                    continue
                else:
                    return 'Round ongoing'
        except TypeError:
            continue
    
    return 'Not a round'

def classicMatch(date, classicosTable):
    for line in classicosTable:
        if line['date'] == date:
            return 'Round includes classic match'

    return 'Standard match round'

print(createDateDimension())
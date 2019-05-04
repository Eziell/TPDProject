import json
from datetime import datetime
# Extraction
# Reading Files

def structureReader(path='relationalSchema.csv', enc='cp850'):
    with open(path, 'r', encoding=enc) as f:
        structure = f.readlines()
        structureDict = dict()
        for line in structure:
            key, value = line.split(';')
            structureDict[key.rstrip()] = value.rstrip().split('\t')
        
    return structureDict

# returns an array containing dictionaries with keys corresponding to the given collumn label, and also the table name, ans specifications for diagostics.
def csvReader(path, struc, ignore=False, enc='cp850', cleanOutput=False):
    with open(path, encoding=enc) as f:
        

        
        # separates file into rows and collumns
        
        raw = []
        for row in f.readlines():
            line = row.rstrip().split('\t')
            # weird workaround for a weird bug were tab is not recognized.
            if len(line) == 1:
                line = row.rstrip().split(';')
            raw.append(line)
        
        # stores the previous element of the iteration
        previous = []
        countLine = 1
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

        # identifying which table we are dealing with
        try:

            # removing and returning the header for collumn identification
            header = raw.pop(0)
            #storedHeader =dict()
            storedHeader = structureReader().get(struc)
            # cheking if the structure is correctly distributed.
            for line in header:
                storedHeader.index(line)
            print('Table Attributes: OK')

            # creating output var for output storage.
            output = []
        
            # stores everything in a dictionary containing the collumns and items assigned to them.
            for row in raw:
                dictRow = dict()
                for i in range(len(header)):
                    dictRow[header[i]] = row[i]
                    
                output.append(dictRow)
            
            # getting special specifications
            specs = []
            for item in storedHeader:
                if item.count('>>') != 0:
                    specs.append(item.replace('>>', ''))
            
            if cleanOutput == False:
                return output, specs
            if cleanOutput == True:
                return output
        
        except KeyError as e:
            print(e)
            print('Required structure may not exist.')
        except KeyError as e:
            print('Header may either be broken, changed or incorrect.')
            print('Are you sure "%s" is the correct structure for this table.' % struc)
        


#teste = csvReader('TPD-CSV/concorrentes.csv')
#print(teste[1].keys())
# Cleanup functions, its aims are:
#   checking and converting collumn contents
#   assigning key constraints and data types
#   validating key constraints and data types
#   checking and alerting for source structure
#   organizing data according 


# output can be found in relationalSchema.csv
# first column corresponds to tabl name,  proceeded by column names.
# non-default parameters can be specified in the end of the list starting with an '>>' identifier.
def relationalSchemaConfig(path='relationalSchema.csv'):
    config = dict()
    config['user'] = ['id', 'nickname', 'birthdate', 'address', 'phone', 'id_gender', 'id_club', 'id_region', 'date_start']
    config['team'] = ['id', 'id_user', 'name', 'code', 'id_origin', 'lastupdate']
    config['keys'] = ['id', 'name', 'is_paid']
    config['league'] = ['id', 'name', 'id_owner']
    config['teamLeaguePrivate'] = ['id_league', 'id_team', 'lastupdate', '>>primaryKey==False']
    config['round'] = ['id', 'date_end_bets', 'date_publish']
    config['userLogin'] = ['id', 'id_user', 'timestamp']
    config['r_club'] = ['id', 'name']
    config['r_gender'] = ['id', 'name']
    config['r_player'] = ['id', 'name']
    config['r_playerposition'] = ['id', 'name']
    config['r_round'] = ['id', 'order', 'name', 'id_round', 'date_start', 'date_end']
    config['r_region'] = ['id', 'name']
    config['cache_player_round'] = ['id_player', 'id_round', 'rank', 'points_round', 'points_total', 'value']
    config['cache_team_round'] = ['id_team', 'id_round', 'points_round', 'rank_round', 'points_total', 'rank_total', 'value_playing_players', 'value_team_complete']
    config['cache_player_team_round'] = ['id_team', 'id_player', 'id_round', 'is_playing', 'default_value']
    config['game'] = ['id', 'id_home_team', 'id_visitor_team', 'goals_home_team', 'goals_visitor_team', 'date_start']
    config['codigos_postais'] = ['cod_distrito', 'cod_concelho', 'cod_localidade', 'nome_localidade', 'num_cod_postal', 'ext_cod_postal', 'desig_postal']
    config['concelhos'] = ['cod_concelho', 'nome_concelho', 'cod_distrito']
    config['distritos'] = ['cod_distrito', 'nome_distrito']
    config['holidays'] = ['day', 'feriado']
    with open(path, 'w') as f:
        for key, value in config.items():
            output = str()
            output += key + '\t;\t'
            output += "\t".join(value)
            output += '\n'
            f.write(output)
# Accepts an array of multiple correctly and cleansed tables and links everything into the Dimension table.
# 
#def dimensionAssembler(tables):
    
# Accepts days in %Y-%m-%d format.
# Returns array containing information about weekday number and wether day corresponds to holiday.
def everyDayWizard(date, path='TPD-CSV/holidays.csv', format='%Y-%m-%d', holidays='holidays.csv', cleanOutput=False):
    parsedDate = datetime.strptime(date, format)
    # retrieving number of weekday
    weekday = datetime.weekday(parsedDate)

    if cleanOutput == True:
        return weekday
    elif cleanOutput == False:
        # dict with key as datetime value, and value as designation of holiday
        holidaysDict = dict()
        for l in csvReader(path, 'holidays', cleanOutput=True):
            day = l['day']
            designation = l['feriado']
            holidaysDict[day] = designation
        
        # if retrieving holiday fails it means there the date does not correspond to holiday
        try:
            holiday = holidaysDict[date]
            return weekday, holiday
        except KeyError:
            return weekday

            

    
def tableCleanup(table, tableType, keys, ignoreDuplicates = True, primaryKey=True, dateFormat = '%Y-%m-%d'):
    
    # array to store primary keys and test constraints
    primaryKeys = list()
    # list of indexes to remove due to wrong format
    removeSchedule = list()

    for i in range(len(table)):
        line = table[i]
        # checking integrity of collumn names
        if keys != list(line.keys()):
                raise ValueError("Collumn names not valid.")
        
        try:
            if tableType == 'user':
                line['id'] = int(line['id'])
                line['nickname'] = str(line['nickname']).rstrip()
                line['birthdate'] = datetime.strptime(line['birthdate'].split(' ')[0], dateFormat)
                line['address'] = str(line['address']).rstrip()
                line['phone'] = int(line['phone'])
                line['id_gender'] = int(line['id_gender'])
                line['id_club'] = int(line['id_club'])
                line['id_region'] = int(line['id_region'])
                line['date_start'] = datetime.strptime(line['date_start'].split(' ')[0], dateFormat)
            elif tableType == 'team':
                line['id'] = int(line['id'])
                line['id_user'] = int(line['id_user'])
                line['name'] = str(line['name']).rstrip()
                line['code'] = str(line['code']).rstrip()
                line['id_origin'] = int(line['id_origin'])
                line['lastupdate'] = datetime.strptime(line['lastupdate'].split(' ')[0], dateFormat)
            elif tableType == 'teamOrigin':
                line['id'] = int(line['id'])
                line['name'] = str(line['name']).rstrip()
                line['is_paid'] = bool(line['is_paid'])
            elif tableType == 'league':
                line['id'] = int(line['id'])
                line['name'] = str(line['name']).rstrip()
                line['id_owner'] = int(line['id_owner'])
            elif tableType == 'teamLeaguePrivate':
                line['id_league'] = int(line['id_league'])
                line['id_team'] = str(line['id_team']).rstrip()
                line['lastupdate'] = int(line['lastupdate'])
            elif tableType == 'round':
                line['id'] = int(line['id'])
                line['date_end_bets'] = datetime.strptime(line['date_publish'].split(' ')[0], dateFormat)
                line['date_publish'] = datetime.strptime(line['date_publish'].split(' ')[0], dateFormat)
            elif tableType == 'userLogin':
                line['id'] = int(line['id'])
                line['id_user'] = int(line['id_user'])
                line['timestamp'] = datetime.strptime(line['timestamp'].split(' ')[0], dateFormat)
            elif tableType == 'r_club':
                line['id'] = int(line['id'])
                line['name'] = str(line['name'])
            elif tableType == 'r_gender':
                line['id'] = int(line['id'])
                line['name'] = str(line['name'])
            elif tableType == 'r_player':
                line['id'] = int(line['id'])
                line['name'] = str(line['name'])
            elif tableType == 'r_playerposition':
                line['id'] = int(line['id'])
                line['name'] = str(line['name'])
            elif tableType == 'r_round':
                line['id'] = int(line['id'])
                line['order'] = int(line['order'])
                line['name'] = str(line['name']).rstrip()
                line['id_round'] = int(line['id_round'])
                line['date_start'] = datetime.strptime(line['date_start'].split(' ')[0], dateFormat)
                line['date_end'] = datetime.strptime(line['date_end'].split(' ')[0], dateFormat)
            elif tableType == 'r_region':
                line['id'] = str(line['id']).rstrip()
                line['name'] = str(line['name']).rstrip()
            elif tableType == 'cache_player_round':
                line['id_player'] = int(line['id_player'])
                line['id_round'] = int(line['id_round'])
                line['rank'] = int(line['rank'])
                line['points_round'] = int(line['points_round'])
                line['points_total'] = int(line['points_total'])
                line['value'] = int(line['value'])
            elif tableType == 'cache_team_round':
                line['id_team'] = int(line['id_team'])
                line['id_round'] = int(line['id_round'])
                line['points_round'] = int(line['points_round'])
                line['rank_round'] = int(line['rank_round'])
                line['points_total'] = int(line['points_total'])
                line['rank_total'] = int(line['rank_total'])
                line['value_playing_players'] = int(line['value_playing_players'])
                line['value_team_complete'] = int(line['value_team_complete'])
            elif tableType == 'cache_player_team_round':
                line['id_team'] = int(line['id_team'])
                line['id_player'] = int(line['id_player'])
                line['id_round'] = int(line['id_round'])
                line['is_playing'] = bool(line['is_playing'])
                line['default_value'] = int(line['default_value'])
            elif tableType == 'game':
                line['id'] = int(line['id'])
                line['id_home_team'] = int(line['id_home_team'])
                line['id_visitor_team'] = int(line['id_visitor_team'])
                line['goals_home_team'] = int(line['goals_home_team'])
                line['goals_visitor_team'] = int(line['goals_visitor_team'])
                line['date_start'] = datetime.strptime(line['date_start'].split(' ')[0], dateFormat)
            elif tableType == 'codigos_postais':
                line['cod_distrito'] = int(line['cod_distrito'])
                line['cod_concelho'] = int(line['cod_concelho'])
                line['cod_localidade'] = int(line['cod_localidade'])
                line['nome_localidade'] = str(line['nome_localidade']).rstrip()
                line['num_cod_postal'] = int(line['num_cod_postal'])
                ## verifies if postal code is within valid range
                if line['num_cod_postal'] > 9999 or line['num_cod_postal'] < 0:
                    raise ValueError("Invalid postal code detected.")
                
                line['ext_cod_postal'] = int(line['ext_cod_postal'])
                ## verifies if postal code is within valid range
                if line['ext_cod_postal'] > 999 or line['ext_cod_postal'] < 0:
                    raise ValueError("Invalid postal code detected.")
                
                line['desig_postal'] = str(line['desig_postal']).rstrip()
            elif tableType == 'concelhos':
                line['cod_concelho'] = int(line['cod_concelho'])
                line['nome_concelho'] = str(line['nome_concelho']).rstrip()
                line['cod_distrito'] = int(line['cod_distrito'])
            elif tableType == 'distritos':
                line['cod_distrito'] = int(line['cod_distrito'])
                line['nome_distrito'] = str(line['nome_distrito']).rstrip()
        except Exception:
            print("Something went wrong with value format parsing. Line will be removed.")
            removeSchedule.append(i)
        if primaryKey == True:
            # By default primary key is expected to be found as a candidate key on the first position
            primaryKeys.append(line.values[0])

    # cheking for duplicates with the same primary key
    if primaryKey == True:
        for i in range(len(table)):
            key = primaryKeys[i]
            if primaryKeys.count(key) > 1:
                if ignoreDuplicates == True:
                    print('Primary Key constraints do not hold up')
                    removeSchedule.append(i)
                else:
                    raise Warning('Duplicates found in file, use of proper candidate keys is highly advised!')

    # filtering table of bad lines
    for i in removeSchedule:
        table.pop(i)
    
    # everything with structure, domains, constraints ok!    
    return(table)


import json
from datetime import datetime
import sys, traceback
# Extraction
# Reading Files

def structureReader(path='TPD-CSV/relationalSchema.csv', enc='utf-8'):
    with open(path, 'r', encoding=enc) as f:
        structure = f.readlines()
        structureDict = dict()
        for line in structure:
            key, value = line.split(',')
            collumns = value.strip().split('\t')
            
            structureDict[key.rstrip()] = collumns
    return structureDict

def getStructure(header):
    for storedHeader in structureReader().values():
        try:
            if len(storedHeader) != len(header):
                raise IndexError("Header length mismatch")
            
            # length matches, checking contents.
            for line in header:
                storedHeader.index(line)
        except IndexError:
            continue
        # returning storedHeader if verything is ok.
        return storedHeader
    # if everything fails.
    raise Exception("Could not match a valid header for the given table. Please check if everything is in order.")


# returns an array containing dictionaries with keys corresponding to the given collumn label, and also the table name, ans specifications for diagostics.
def csvReader(path, ignore=False, enc='utf-8', cleanOutput=True):
    with open(path, encoding=enc) as f:
        # separates file into rows and collumns
        
        raw = []
        for row in f.readlines():
            line = row.rstrip().split('\t')
            # weird workaround for a weird bug were tab is not recognized.
            if len(line) == 1:
                line = row.rstrip().split(',')
            raw.append(line)
        
        # stores the previous element of the iteration
        previous = []
        remIndex = list()
        for i in range(len(raw)):
            line = raw[i]
            if len(previous) == 0:
                previous = line
            
            if  len(line) == 1:
                raise Exception('Unreliable number of collumns\nFile: %s\nLine: %s' % (path, i))
            
            if len(previous) != len(line):
                print('Inconsistent number of collumns\nFile: %s\nLine: %s\nRemoving Line.' % (path, i))
                remIndex.append(i)
                continue
        
            # stores the previous set for comparison
            previous = line

        # reverse sorting for correctly removing the elems from list
        remIndex.sort(reverse=True)
        for i in remIndex:
            raw.pop(i)

        print('File Structure: OK')
        print('Lines Removed: %i\nLines Added: %i' % (len(remIndex), len(raw)))
        # identifying which table we are dealing with
        try:
            # removing and returning the header for collumn identification
            header = raw.pop(0)
            #storedHeader =dict()
            #storedHeader = structureReader().get(struc)
            # cheking if the structure is correctly distributed.
            #for line in header:
            #    storedHeader.index(line)
            storedHeader = getStructure(header)
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



# output can be found in TPD-CSV/relationalSchema.csv
# first column corresponds to tabl name,  proceeded by column names.
# non-default parameters can be specified in the end of the list starting with an '>>' identifier.

def relationalSchemaConfig(path='TPD-CSV/relationalSchema.csv'):
    config = dict()
    config['user'] = ['id', 'nickname', 'birthdate', 'address', 'agegroup', 'gender', 'club', 'region', 'startdate']
    config['rounds'] = ['season', 'order', 'start_date', 'end_date', 'publish_date']
    config['rounds_teams'] = ['season', 'id_team', 'order_round', 'team_name', 'team_points_round', 'team_points_total', 'team_rank_round', 'team_rank_total', 'team_value']
    config['teams'] = ['season', 'id', 'name', 'createdate', 'origin', 'is_paid', 'round_start', 'id_user']
    config['user_details_logins'] = ['season', 'id_user', 'round_order', 'premiumdate', 'in_league', 'logins_round', 'logins_sunday', 'logins_monday','logins_tuesday', 'logins_wednesday', 'logins_thursday', 'logins_friday', 'logins_saturday']
    config['codigos_postais'] = ['cod_distrito','cod_concelho','cod_localidade','nome_localidade','cod_arteria','tipo_arteria','prep1','titulo_arteria','prep2','nome_arteria','local_arteria','troco','porta','cliente','num_cod_postal','ext_cod_postal','desig_postal']
    config['concelhos'] = ['cod_distrito', 'cod_concelho', 'nome_concelho']
    config['distritos'] = ['cod_distrito', 'nome_distrito']
    config['holidays'] = ['day', 'feriado']
    config['classicos'] = ['season', 'date', 'home', 'visitor', 'goals_home', 'goals_visitor']
    with open(path, 'w') as f:
        for key, value in config.items():
            output = str()
            output += key + '\t,\t'
            output += "\t".join(value)
            output += '\n'
            f.write(output)
# Accepts an array of multiple correctly and cleansed tables and links everything into the Dimension table.
# 
#def dimensionAssembler(tables):

# Accepts days in %Y-%m-%d format.
# Returns array containing information about weekday number and wether day corresponds to holiday.
def everyDayWizard(date, path='TPD-CSV/holidays.csv', format='%Y-%m-%d', holidays='holidays.csv', cleanOutput=True):
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

def attributeCleanup(attribute, type, dateFormat = '%Y-%m-%d', ignoreNull = False):
    # NULL é regra geral o que vem de sql se uma coluna não tiver valor. isto pode fazer sentido em algumas tabelas.
    if ignoreNull==True and attribute == 'NULL':
        return None
    elif type == 'str':
        return str(attribute).rstrip()
    elif type == 'int' and attribute == '' and ignoreNull == True:
        return None
    elif type == 'int':
        return int(attribute.replace('_x000D_', ''))
    elif type == 'date':
        return datetime.strptime(attribute.split(' ')[0], dateFormat)
    elif type == 'bool':
        return bool(attribute)

# Cleanup functions, its aims are:
#   checking and converting collumn contents
#   assigning key constraints and data types
#   validating key constraints and data types
#   checking and alerting for source structure
#   organizing data according

def tableCleanup(table, ignoreDuplicates = True, dateFormat = '%Y-%m-%d'):
    
    # detecting structure
    for structure, values in structureReader().items():
        header = list(table[0].keys())
        if values == header:
            tableType = structure
    
    # list of indexes to remove due to wrong format
    removeSchedule = list()

    # to store output 
    output = list()

    # to count erros
    err = 0

    for i in range(len(table)):
        line = table[i]
        outputLine = dict()
        try:
            if tableType == 'user':
                outputLine['id'] = attributeCleanup(line['id'], 'int')
                outputLine['nickname'] = attributeCleanup(line['nickname'], 'str')
                outputLine['birthdate'] = attributeCleanup(line['birthdate'], 'date')
                outputLine['address'] = attributeCleanup(line['address'], 'str')
                outputLine['agegroup'] = attributeCleanup(line['agegroup'], 'str')
                outputLine['gender'] = attributeCleanup(line['gender'], 'str')
                outputLine['club'] = attributeCleanup(line['club'], 'str')
                outputLine['region'] = attributeCleanup(line['region'], 'str')
                outputLine['startdate'] = attributeCleanup(line['startdate'], 'date')
            elif tableType == 'rounds':
                outputLine['season'] = attributeCleanup(line['season'], 'str')
                outputLine['order'] = attributeCleanup(line['order'], 'int')
                outputLine['start_date'] = attributeCleanup(line['start_date'], 'date')
                outputLine['end_date'] = attributeCleanup(line['end_date'], 'date')
                outputLine['publish_date'] = attributeCleanup(line['publish_date'], 'date', ignoreNull=True)
            elif tableType == 'rounds_teams':
                outputLine['season'] = attributeCleanup(line['season'], 'str')
                outputLine['id_team'] = attributeCleanup(line['id_team'], 'int')
                outputLine['order_round'] = attributeCleanup(line['order_round'], 'int')
                outputLine['team_name'] = attributeCleanup(line['team_points_round'], 'str')
                outputLine['team_points_round'] = attributeCleanup(line['team_points_round'], 'int')
                outputLine['team_points_total'] = attributeCleanup(line['team_points_total'], 'int')
                outputLine['team_rank_round'] = attributeCleanup(line['team_rank_round'], 'int')
                outputLine['team_rank_total'] = attributeCleanup(line['team_rank_total'], 'int')
                outputLine['team_value'] = attributeCleanup(line['team_value'], 'int')
            elif tableType == 'teams':
                outputLine['season'] = attributeCleanup(line['season'], 'str')
                outputLine['id'] = attributeCleanup(line['id'], 'int')
                outputLine['name'] = attributeCleanup(line['name'], 'str')
                outputLine['createdate'] = attributeCleanup(line['createdate'], 'date')
                outputLine['origin'] = attributeCleanup(line['origin'], 'str')
                outputLine['is_paid'] = attributeCleanup(line['is_paid'], 'int')
                outputLine['round_start'] = attributeCleanup(line['round_start'], 'int')
                outputLine['id_user'] = attributeCleanup(line['id_user'], 'int') 
            elif tableType == 'user_details_logins':
                outputLine['season'] = attributeCleanup(line['season'], 'str')
                outputLine['id_user'] = attributeCleanup(line['id_user'], 'int')
                outputLine['round_order'] = attributeCleanup(line['round_order'], 'int')
                outputLine['premiumdate'] = attributeCleanup(line['premiumdate'], 'date', ignoreNull = True)
                outputLine['in_league'] = attributeCleanup(line['in_league'], 'int')
                outputLine['logins_round'] = attributeCleanup(line['logins_round'], 'int')
                outputLine['logins_sunday'] = attributeCleanup(line['logins_sunday'], 'int')
                outputLine['logins_monday'] = attributeCleanup(line['logins_monday'], 'int')
                outputLine['logins_tuesday'] = attributeCleanup(line['logins_tuesday'], 'int')
                outputLine['logins_wednesday'] = attributeCleanup(line['logins_wednesday'], 'int')
                outputLine['logins_thursday'] = attributeCleanup(line['logins_thursday'], 'int')
                outputLine['logins_friday'] = attributeCleanup(line['logins_friday'], 'int')
                outputLine['logins_saturday'] = attributeCleanup(line['logins_saturday'], 'int')
            elif tableType == 'distritos':
                outputLine['cod_distrito'] = attributeCleanup(line['cod_distrito'], 'int')
                outputLine['nome_distrito'] = attributeCleanup(line['nome_distrito'], 'str')
            elif tableType == 'concelhos':
                outputLine['cod_distrito'] = attributeCleanup(line['cod_distrito'], 'int')
                outputLine['cod_concelho'] = attributeCleanup(line['cod_concelho'], 'int')
                outputLine['nome_concelho'] = attributeCleanup(line['nome_concelho'], 'str')
            elif tableType == 'codigos_postais':
                outputLine['cod_distrito'] = attributeCleanup(line['cod_distrito'], 'int')
                outputLine['cod_concelho'] = attributeCleanup(line['cod_concelho'], 'int')
                outputLine['cod_localidade'] = attributeCleanup(line['cod_localidade'], 'int')
                outputLine['nome_localidade'] = attributeCleanup(line['nome_localidade'], 'str')
                outputLine['cod_arteria'] = attributeCleanup(line['cod_arteria'], 'int', ignoreNull = True)
                outputLine['tipo_arteria'] = attributeCleanup(line['tipo_arteria'], 'str', ignoreNull = True)
                outputLine['prep1'] = attributeCleanup(line['prep1'], 'str', ignoreNull = True)
                outputLine['titulo_arteria'] = attributeCleanup(line['titulo_arteria'], 'str', ignoreNull = True)
                outputLine['prep2'] = attributeCleanup(line['prep2'], 'str', ignoreNull = True)
                outputLine['nome_arteria'] = attributeCleanup(line['nome_arteria'], 'str', ignoreNull = True)
                outputLine['local_arteria'] = attributeCleanup(line['local_arteria'], 'str', ignoreNull = True)
                outputLine['troco'] = attributeCleanup(line['troco'], 'str', ignoreNull = True)
                outputLine['porta'] = attributeCleanup(line['porta'], 'str', ignoreNull = True)
                outputLine['cliente'] = attributeCleanup(line['cliente'], 'str')
                outputLine['num_cod_postal'] = attributeCleanup(line['num_cod_postal'], 'str')
                outputLine['ext_cod_postal'] = attributeCleanup(line['ext_cod_postal'], 'str')
                outputLine['desig_postal'] = attributeCleanup(line['desig_postal'], 'str')
            elif tableType == 'classicos':
                outputLine['season'] = attributeCleanup(line['season'], 'str')
                outputLine['date'] = attributeCleanup(line['date'], 'date')
                outputLine['home'] = attributeCleanup(line['home'], 'str')
                outputLine['visitor'] = attributeCleanup(line['visitor'], 'str')
                outputLine['goals_home'] = attributeCleanup(line['goals_home'], 'int')
                outputLine['goals_visitor'] = attributeCleanup(line['goals_visitor'], 'int')
            else:
                raise Exception('Unknown structure given to function.')
            
            # attaching the new well formated line
            output.append(outputLine)

        except ValueError as e:
            print("Something went wrong with value format parsing. Line will be removed.")
            print(e.args)
            removeSchedule.append(i)
            err += 1
        except UnboundLocalError:
            print("Probably stored collumn structure/names don't match or are corrupted.")
            sys.exit(1)
    
    # measuring the ammount of errors
    print('Lines Removed: %i\nLines Correctly Read: %i' % (err, len(output)))
    # everything with structure, domains, constraints ok!    
    return(output)

relationalSchemaConfig()
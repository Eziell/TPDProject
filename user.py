import extraction as ext 
from datetime import datetime
import addressFinder as af 

def createUserDimension(path='TPD-CSV/LigaRecord/'):

    rawTable = ext.csvReader(path + 'user.csv')
    userTable = ext.tableCleanup(rawTable)
    
    rawTable = ext.csvReader(path + 'user_details_logins.csv')
    detailsTable = ext.tableCleanup(rawTable)
    
    users = list()
    
    for line in userTable:
    
        user = dict()
        user['User Natural ID'] = line['id']
        #user['User Email'] = formatTable[1]['?']
        user['User Nickname'] = line['nickname']
        user['User Birthdate'] = str(line['birthdate'])
        user['User Gender'] = line['gender']
        user['User Club'] = line['club']
        user['User Region'] = line['region']
    
        addressInfo = af.addressFinder(line['address'])
        user['User Zipcode Locality'] = addressInfo["cod_postal"]+"-"+addressInfo["ext_postal"]
        user['User Zipcode Locality Designation'] = addressInfo["desig_postal"]
        user['User Locality'] = addressInfo["nome_localidade"]
        user['User County'] = addressInfo["nome_concelho"]
        user['User District'] = addressInfo["nome_distrito"]
        #user['User Country'] = formatTable[1]['?']
    
        user['User Original Start Date'] = str(line['startdate'])
        #user['User Season Start Date'] = formatTable[1]['?']
        #user['User Premium Date'] = formatTable[1]['?']
        user['User Agegroup'] = line['agegroup']
        #user['User Is In League'] = formatTable[1]['?']
        #user['Effective Date Row'] = formatTable[1]['?']
        #user['Expiration Date Row'] = formatTable[1]['?']
        #user['Timestamp Row'] = formatTable[1]['?']
        #user['Is Current Row'] = formatTable[1]['?']
        
        users.append(user)
    
    return users

# should be used with dimension as dict from the function createUserDimension()
def assignCandidateKey(key, dimension):
    dimension['User Key (PK)'] = key

    return dimension

print(createUserDimension())
import extraction as ext 
from datetime import datetime
import addressFinder as af 

def createUserDimension(path='TPD-CSV/LigaRecord/'):

    rawTable = ext.csvReader(path + 'user.csv')
    formatTable = ext.tableCleanup(rawTable)
    
    user = dict()
    user['User Natural ID'] = formatTable[1]['id']
    user['User Email'] = formatTable[1]['?']
    user['User Nickname'] = formatTable[1]['nickname']
    user['User Birthdate'] = str(formatTable[1]['birthdate'])
    user['User Gender'] = formatTable[1]['gender']
    user['User Club'] = formatTable[1]['club']
    user['User Region'] = formatTable[1]['region']
    
    addressInfo = af.addressFinder(formatTable[1]['address'])
    user['User Zipcode Locality'] = addressInfo["cod_postal"]+"-"+addressInfo["ext_postal"]
    user['User Zipcode Locality Designation'] = addressInfo["desig_postal"]
    user['User Locality'] = addressInfo["nome_localidade"]
    user['User County'] = addressInfo["nome_concelho"]
    user['User District'] = addressInfo["nome_distrito"]
    user['User Country'] = formatTable[1]['?']
    
    user['User Original Start Date'] = str(formatTable[1]['startdate'])
    user['User Season Start Date'] = formatTable[1]['?']
    user['User Premium Date'] = formatTable[1]['?']
    user['User Agegroup'] = formatTable[1]['agegroup']
    user['User Is In League'] = formatTable[1]['?']
    user['Effective Date Row'] = formatTable[1]['?']
    user['Expiration Date Row'] = formatTable[1]['?']
    user['Timestamp Row'] = formatTable[1]['?']
    user['Is Current Row'] = formatTable[1]['?']
    
    return user

# should be used with dimension as dict from the function createUserDimension()
def assignCandidateKey(key, dimension):
    dimension['User Key (PK)'] = key

    return dimension

createUserDimension()
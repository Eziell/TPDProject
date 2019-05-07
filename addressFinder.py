import json
import re
import unidecode

def addressFinder(addressStr):
    
    with open('TPD-CSV/CTT/distritos.json', encoding="utf8") as distritos_json_file:
        distritos = json.load(distritos_json_file)
    
    with open('TPD-CSV/CTT/concelhos.json', encoding="utf8") as concelhos_json_file:  
        concelhos = json.load(concelhos_json_file)
        
    with open('TPD-CSV/CTT/codigos_postais.json', encoding="utf8") as cp_json_file:
        codigos_postais = json.load(cp_json_file)
        
    final_distrito = "nao especificado"
    final_concelho = "nao especificado"
    final_localidade = "nao especificado"
    final_designacao = "nao especificado"
    final_cod_postal = "nao especificado"
    final_ext_postal = "nao especificado"
    search_result = None
        
    match = re.search('([0-9]{4}-[0-9]{3})', addressStr)

    
    if match:
    
        split_match = match[0].split('-')
        
        final_cod_postal = split_match[0]
        final_ext_postal = split_match[1]
    
        search_result = next((item for item in codigos_postais if item["num_cod_postal"] == final_cod_postal and item["ext_cod_postal"] == final_ext_postal),None)
        
    if search_result != None:
        distrito_result = next(item for item in distritos if item["cod_distrito"] == search_result["cod_distrito"])
        concelho_result = next(item for item in concelhos if item["cod_distrito"] == search_result["cod_distrito"] and item["cod_concelho"] == search_result["cod_concelho"])
        
        if distrito_result["nome_distrito"] != '':
                final_distrito = distrito_result["nome_distrito"]
        
        if concelho_result["nome_concelho"] != '':
                final_concelho = concelho_result["nome_concelho"]
            
        if search_result["nome_localidade"] != '':
                final_localidade = search_result["nome_localidade"]
            
        if search_result["desig_postal"] != '':
                final_designacao = search_result["desig_postal"]
                
    else:
            
        print("Postal Code introduced not found in CTT data.")
        final_cod_postal = "nao especificado"
        final_ext_postal = "nao especificado"
        final_distrito_codigo = None
        final_concelho_codigo = None
        length_of_find = 0
        
        for district in distritos:
            if " " + unidecode.unidecode(district["nome_distrito"].lower()) in unidecode.unidecode(addressStr.lower()) and len(district["nome_distrito"]) >= length_of_find:
                final_distrito = district["nome_distrito"]
                final_distrito_codigo = district["cod_distrito"]
                addressStr = unidecode.unidecode(addressStr.lower()).replace(unidecode.unidecode(final_distrito.lower()), '')
                length_of_find = len(final_distrito)
        
        length_of_find = 0
        for concelho in concelhos:
            if " " + unidecode.unidecode(concelho["nome_concelho"].lower()) in unidecode.unidecode(addressStr.lower()):
                if (final_distrito_codigo == "nao especificado" or final_distrito_codigo == concelho["cod_distrito"]) and length_of_find <= len(concelho["nome_concelho"]):
                    final_concelho = concelho["nome_concelho"]
                    final_concelho_codigo = concelho["cod_concelho"]
                    addressStr = unidecode.unidecode(addressStr.lower()).replace(unidecode.unidecode(final_concelho.lower()), '')
                    length_of_find = len(final_concelho)
                    
        filtered_cps = codigos_postais
        
        if final_concelho_codigo != None and final_distrito_codigo != None:
            filtered_cps = [cp for cp in codigos_postais if cp["cod_distrito"] == final_distrito_codigo and cp["cod_concelho"] == final_concelho_codigo]
        elif final_concelho_codigo != None:
            filtered_cps = [cp for cp in codigos_postais if cp["cod_concelho"] == final_concelho_codigo]
        elif final_distrito_codigo != None:
            filtered_cps = [cp for cp in codigos_postais if cp["cod_distrito"] == final_distrito_codigo]
        
        length_of_find_loc = 0
        length_of_find_desig = 0
        for cp in filtered_cps:
            if " " + unidecode.unidecode(cp["nome_localidade"].lower()) in unidecode.unidecode(addressStr.lower()) and length_of_find_loc <= len(cp["nome_localidade"]):
                final_localidade = cp["nome_localidade"]
                length_of_find_loc = len(final_localidade)
                
            if " " + unidecode.unidecode(cp["desig_postal"].lower()) in unidecode.unidecode(addressStr.lower()) and length_of_find_desig <= len(cp["desig_postal"]):
                final_designacao = cp["desig_postal"]
                length_of_find_desig = len(final_designacao)
        
        
        
    return dict({'cod_postal': final_cod_postal, 'ext_postal': final_ext_postal, 'nome_distrito': final_distrito, 'nome_concelho': final_concelho, 'nome_localidade': final_localidade, 'desig_postal': final_designacao})
            
#print(addressFinder('Évora Bairro Lino de Carvalho VENDAS NOVAS'))
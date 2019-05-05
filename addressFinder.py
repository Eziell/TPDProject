import json
import re

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
        concelho_result = next(item for item in concelhos if item["cod_concelho"] == search_result["cod_concelho"])
        
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
        
        
    return dict({'cod_postal': final_cod_postal, 'ext_postal': final_ext_postal, 'nome_distrito': final_distrito, 'nome_concelho': final_concelho, 'nome_localidade': final_localidade, 'desig_postal': final_designacao})
            
print(addressFinder('blaBla Bla-bla 5555 5555-555 bla'))
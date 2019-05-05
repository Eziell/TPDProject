import ETL as e
e.relationalSchemaConfig()
#print(e.csvReader('TPD-CSV/csv_teste.csv', 'teamLeaguePrivate'))
#print(e.csvReader('holidays.csv', 'holidays'))
#print(e.everyDayWizard('2019-1-1'))
#print(e.structureReader())
for l in e.tableCleanup(e.csvReader('TPD-CSV/CTT/codigos_postais.csv', 'codigos_postais')):
    True
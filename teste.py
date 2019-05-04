import ETL as e
e.relationalSchemaConfig()
#print(e.csvReader('TPD-CSV/csv_teste.csv', 'teamLeaguePrivate'))
#print(e.csvReader('holidays.csv', 'holidays'))
print(e.everyDayWizard('2019-1-1'))
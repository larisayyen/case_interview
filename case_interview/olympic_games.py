
import csv

COUNTRIES_FILEPATH = "raw_data/olympics/dictionary.csv"
MEDALS_FILEPATH = "raw_data/olympics/winter.csv"

# test
with open(MEDALS_FILEPATH,mode='r') as csv_file:
        csv_reader=csv.DictReader(csv_file)
        for row in csv_reader:
            print(row)

def most_decorated_athlete_ever():

    athletes = {}

    with open(MEDALS_FILEPATH,mode = 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # linear search 1st round
        for r in csv_reader:
            if row['Athlete'] not in athletes:
                athletes[row['Athlete']] = 1
            else:
                athletes[row['Athlete']] += 1

    best_athlete = None
    medal_count = 0

    # linear search 2nd round
    for athlete,medal in athletes.items():
        if medal > medal_count:
            best_athlete = athlete
            medal_count = medal

    return best_athlete

def country_with_most_gold_medals(min_year, max_year):

    country_won_gold = {}

    with open(MEDALS_FILEPATH,mode='r') as csv_file:
        csv_reader=csv.DictReader(csv_file)

        for row in csv_reader:
            year = int(row['Year'])
            if min_year <= year <= max_year and row['Medal'] == 'Gold':
                if row['Country'] not in country_won_gold:
                    country_won_gold[row['Country']] =1
                else:
                    country_won_gold[row['Country']] +=1

    best_country = None
    medal_count = 0
    for country,medal in country_won_gold.items():
        if medal > medal_count:
            best_country = country
            medal_count = medal

    with open(COUNTRIES_FILEPATH,mode='r') as csv_file:
        csv_reader=csv.DictReader(csv_file)
        for row in csv_file:
            #print(row):Country,Code,Population,GDP per Capita
            row = row.split(',')
            if row[1] == best_country:
                return row[0]
    return best_country

def top_three_women_in_five_thousand_meters():
    with open(MEDALS_FILEPATH,mode='r') as csv_file:
        csv_reader=csv.DictReader(csv_file,skipinitialspace=True)
        women_won_medal={}
        for row in csv_reader:
            if row['Event']=='5000M' and row['Gender']=='Women':
                if row['Athlete'] not in women_won_medal:
                    women_won_medal[row['Athlete']] =1
                else:
                    women_won_medal[row['Athlete']] +=1

        # sort by medals
        women_won_medal=sorted(women_won_medal.items(),key=lambda k:k[1],reverse=True)

        return list(map(lambda woman: woman[0],women_won_medal[:3]))

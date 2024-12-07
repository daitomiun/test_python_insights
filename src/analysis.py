import requests
import csv
import random
import json
import sys
import os
# I could'nt find a groceries api that was able to do the requests needed in the timefrima of 2 minutes and many were blocked for use after just 20 request, so I'm doing the following

# This is a Pokemon battle insights where it reports the effectiveness of your pokemon against random pokemon from the pokeAPI

battle_insights_url = "https://pokeapi.co/api/v2/pokemon/"

pokemons_to_battle = [
    "pikachu",
    "ditto",
    "charmander",
    "bulbasaur",
    "venusaur",
    "charizard",
    "wartortle",
    "kakuna",
    "beedrill",
    "pidgey"
]

orig_stdout = sys.stdout
csv_args = sys.argv[1]

report = open(os.getcwd() + '//report.md', "w")
sys.stdout = report


print("# Battle Insights!!")

with open(csv_args, mode='r') as file:
    pokemons = csv.DictReader(file)
    for pokemon in pokemons:
        our_pokemon_weight = int(float(pokemon["weight"]))
        our_pokemon_base_stat_hp = int(pokemon["base_stat_hp"])
        our_pokemon_base_stat_attack = int(pokemon["base_stat_attack"])
        pokemon_name = pokemon["name"]

        # choose random pokemon fro request and send to see it's stats
        random_pokemon = random.randrange(len(pokemons_to_battle))
        update_url = f"{battle_insights_url}{pokemons_to_battle[random_pokemon]}"
        
        response = requests.get(update_url)

        # convert response to python object or dictionary
        pokemon_battle = json.loads(response.text)

        # organize the fetched pokemon
        pokemon_battle_hp = pokemon_battle["stats"][0]["base_stat"]
        pokemon_battle_attack = pokemon_battle["stats"][1]["base_stat"]
        pokemon_battle_weight = pokemon_battle["weight"]

        # Check pokemon weight, base hp stat and attack stat to see if our pokemon is more effective or not than the one fetch from the pokeAPI
        print("---------------------")
        report.write("\n")
        print(f"Our {pokemon_name}")
        report.write("\n")
        if our_pokemon_base_stat_hp < pokemon_battle_hp:
            print("has lower health", our_pokemon_base_stat_hp,"than", pokemon_battle["name"],pokemon_battle_hp)
        else:                                                                             
            print("has more health", our_pokemon_base_stat_hp,"than", pokemon_battle["name"],pokemon_battle_hp)
        report.write("\n")

        if our_pokemon_weight < pokemon_battle_weight:
            print("is lighter", our_pokemon_weight, "than",pokemon_battle["name"] ,pokemon_battle_weight)
        else:                                                                      
            print("is heavier", our_pokemon_weight, "than", pokemon_battle["name"] ,pokemon_battle_weight)

        report.write("\n")
        if our_pokemon_base_stat_attack < pokemon_battle_attack:
            print("has less attack", our_pokemon_base_stat_attack, "than", pokemon_battle["name"], pokemon_battle_attack)
        else:
            print("has more attack", our_pokemon_base_stat_attack, "than", pokemon_battle["name"], pokemon_battle_attack)
        report.write("\n")

report.write("\n")
print("---------------------")
print("# Report Finished!")

sys.stdout = orig_stdout
report.close()

print("Report created at reports.md")


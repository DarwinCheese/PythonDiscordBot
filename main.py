import discord
import os
import requests
import json
import logging
from replit import db

logging.basicConfig(level=logging.INFO)

client = discord.Client()

def get_pokemon(pokemon):
  response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
  json_data = json.loads(response.text)
  pokemon_name_and_xp = json_data["name"].capitalize() + " - " + str(json_data["base_experience"]) + " XP"
  return pokemon_name_and_xp

def update_pokemon(new_pokemon):
  if "pokemon" in db.keys():
    pokemon = db["pokemon"]
    pokemon.append(new_pokemon)
    db["pokemon"] = pokemon
  else:
    db["pokemon"] = [new_pokemon]

def delete_pokemon(index):
  pokemon = db["pokemon"]
  if len(pokemon) > index:
    del pokemon[index]
    db["pokemon"] = pokemon

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client)+'!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('$pokemon'):
    pokemon_data = get_pokemon(msg.split()[1])
    await message.channel.send(pokemon_data)

  if msg.startswith("$new"):
    new_pokemon = msg.split()[1]
    update_pokemon(new_pokemon)
    await message.channel.send("New pokemon added.")
  
client.run(os.environ['DiscordBotToken'])
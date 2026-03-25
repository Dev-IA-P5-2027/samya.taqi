from fastapi import FastAPI, HTTPException, Path
from dataclasses import dataclass, asdict
from fastapi import FastAPI
from typing import Union
import json
import math

#===== Structure de données : Dictionnaire indexé par pokemon id =====#
with open("pokemons.json", "r") as f:
    pokemons_list = json.load(f)

list_pokemons = {k+1:v for k, v in enumerate(pokemons_list)}
#======================================================================
@dataclass
class Pokemon() :
    id: int
    name: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Union[int, None] = None
#======================================================================

app = FastAPI()


@app.get("/total_pokemons")
def get_total_pokemons() -> dict:
    return {"total_pokemons": len(list_pokemons)}

@app.get("/pokemon")
def get_all_pokemons() -> list[Pokemon]:
    res=[]
    for id in list_pokemons:
        res.append(Pokemon(**list_pokemons[id]))
    return list_pokemons
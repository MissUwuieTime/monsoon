import requests
from bs4 import BeautifulSoup
from model import BalanceModel

class LolFandom():
  def __init__(self):
    self.url = "https://leagueoflegends.fandom.com"
    self.__cache = self.__fetch_aram_balance_changes()
    self.__balances_by_key = self.__process_cache()

  def __fetch_aram_balance_changes(self):
    req = requests.get(f"{self.url}/wiki/ARAM")

    if req.status_code != 200:
      raise Exception("Failed to get ARAM balance changes from LoL Fandom")
    
    soup = BeautifulSoup(req.text, "html.parser")
    rows = soup.select("div.tabber table tbody tr")

    if len(rows) == 0:
      raise Exception("Failed to parse table from Lol Fandom; No rows found")

    return rows
  
  def __process_cache(self):
    """Process cache into a dictionary of balance changes using name as key.
    Below example indexed by raw response, NOT by the parsed response.
    tr[0] - Contains champion name
    tr[1] - Contains damage dealt
    tr[2] - Contains damage received
    tr[3] - Contains other changes
    """
    balance = {}
    for tr in self.__cache[1:]:
      champion_name = tr.contents[1].text.strip()
      balance.update({ champion_name: BalanceModel(
        damage_dealt=tr.contents[3].text.strip(),
        damage_received=tr.contents[5].text.strip(),
        other_changes=tr.contents[7].text.strip()
      )})
    
    return balance

  
  def fetch_balance_by_champion_name(self, name):
    return self.__balances_by_key.get(name)
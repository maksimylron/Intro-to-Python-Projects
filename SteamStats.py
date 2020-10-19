import os
import sys
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import json
import ssl
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# read API key from saved file
APIkey = (open(os.path.join(sys.path[0], "SteamAPIkey.txt"), "r")).read()

# input SteamID
steamID = input('Enter SteamID: ')

# parse steamID URL to get 64bit Steam bit equivalent
steamIDurl = 'https://steamcommunity.com/id/' + steamID + '/?xml=1'
reqID = urllib.request.urlopen(steamIDurl, context=ctx)
dataID = reqID.read().decode()
IDtree = ET.fromstring(dataID)
ID64 = IDtree.find('steamID64').text

# construct SteamAPI URL
apiURL = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' + \
    APIkey + '&steamid=' + ID64 + \
    '&format=json&include_appinfo=true&include_played_free_games=true'

print('Retrieving', apiURL)
uh = urllib.request.urlopen(apiURL, context=ctx)
data = uh.read().decode()
steamData = json.loads(data)

xDict = dict()
count = 0
countNonGames = 7

totalGames = steamData['response']['game_count']

# create dictionary of key, value for gameName, hoursplayed
for i in range(totalGames):
    for x in steamData['response']['games']:
        if not x['name'].startswith('True'):
            xDict[x['name']] = \
                xDict.get(x['name'], int(x['playtime_forever']/60))

# convert dictionary to list of tuples to sort
vkList = list()
for key, value in xDict.items():
    a = (value, key)
    vkList.append(a)
vkListsort = sorted(vkList)

# get values for x and y for graph
xVal = list()
for a in range(steamData['response']['game_count'] - countNonGames):
    xVal.append((vkListsort[a])[0])

yVal = list()
for b in range(steamData['response']['game_count'] - countNonGames):
    yVal.append((vkListsort[b])[1])

x = yVal
y = xVal

x_pos = [i for i, _ in enumerate(x)]

plt.barh(x_pos, y, color='green')
plt.ylabel("Steam Games")
plt.xlabel("Hours Played")
plt.title('Hours Played on Owned Steam Game, Total = ' +
          str(sum(xDict.values())) + ' Hours')

plt.yticks(x_pos, x)

# put data labels
for i, v in enumerate(y):
    plt.text(v, i, str(v), color='blue', va='center', fontweight='bold')

plt.show()

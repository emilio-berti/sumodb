import sys
import requests as re
import seaborn as sns
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt

divisions = CategoricalDtype(
	categories = [
		"Yokozuna", "Ozeki", "Sekiwake", "Komusubi", "Maegashira", "Juryo", 
		"Makushita", "Sandanme", "Jonidan", "Jonokuchi", "Mae-zumo"
	], ordered = True)

def get_rank(x):
	if x == 'Mae-zumo':
		return 0
	else:
		return int(x.split(' ')[1])

def get_data(sumoid):
	m = re.get('https://www.sumo-api.com/api/rikishi/{}/matches'.format(sumoid))
	m = m.json()['records']
	basho = []
	rank = []
	for x in m:
		if x == m[0]:
			basho.append(x['bashoId'])
			if x['eastId'] == sumoid:
				rank.append(x['eastRank'])
			else:
				rank.append(x['westRank'])
		else:
			if x['bashoId'] not in basho:
				basho.append(x['bashoId'])
				if x['eastId'] == sumoid:
					rank.append(x['eastRank'])
				else:
					rank.append(x['westRank'])
	division = list(map(lambda x: x.split(' ')[0], rank))
	rank = list(map(get_rank, rank))
	d = pd.DataFrame({'basho': basho, 'division': division, 'r': rank})
	x = [i for i in range(len(d))]
	x.reverse()
	d['id'] = x
	d.division = d.division.astype(divisions)
	return d

shikona = sys.argv[1]
# shikona='Akebono'
# shikona='Hakuho Sho'
d = re.get('https://www.sumo-api.com/api/rikishis?shikonaEn={}&intai=true'.format(shikona))
if d.json()['total'] == 0:
	sys.exit(1)
else :
	sumoid = d.json()['records'][0]['id']
	d = get_data(sumoid)

	sns.set_style("whitegrid")
	pal = sns.diverging_palette(220, 20, l = 65, center = "dark", as_cmap = True)
	g = sns.scatterplot(
		x = "id", y = "division", data = d,
		hue = "r", palette = pal, edgecolors = "dimgray"
	)
	g.set_xlabel('Basho', fontdict={'size': 15})
	g.set_ylabel('Division', fontdict={'size': 15})
	g.legend(title = "Rank")
	plt.show()

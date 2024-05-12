import sys
import requests as re
import seaborn as sns
import pandas as pd
from pandas.api.types import CategoricalDtype
from math import ceil
import matplotlib.pyplot as plt

def get_data(sumoid, basho):
	m = re.get('https://www.sumo-api.com/api/rikishi/{}/matches?bashoId={}'.format(sumoid, basho))
	m = m.json()['records']
	opponent=[]
	res=[]
	day=[]
	for x in m:
		target = 'eastShikona' if x['eastId'] == sumoid else 'westShikona'
		opponent.append(x['westShikona']) if target == 'eastShikona' else opponent.append(x['eastShikona'])
		res.append('w') if x['winnerId'] == sumoid else res.append('l')
		day.append(x['day'])
	opponent.reverse()
	res.reverse()
	day.reverse()
	d = pd.DataFrame({'day': day, 'opponent': opponent, 'result': res})
	return d

shikona = sys.argv[1]
basho = sys.argv[2]
# shikona='Kotoeko'
# basho='202305'
d = re.get('https://www.sumo-api.com/api/rikishis?shikonaEn={}&intai=true'.format(shikona))
if d.json()['total'] == 0:
	sys.exit(1)
else :
	sumoid = d.json()['records'][0]['id']
	d = get_data(sumoid, basho)

print(d)

# sns.set_style("white", {'grid.color': '#eeeeee', 'axes.grid': True})
# pal = sns.diverging_palette(220, 20, l = 65, center = "dark", as_cmap = True)
# g = sns.scatterplot(
# 	x = "id", y = "division", data = d,
# 	hue = "r", palette = pal, edgecolors = "dimgray"
# )
# sns.despine()
# g.set_xlabel('Year', fontdict={'size': 15})
# g.set_ylabel('Division', fontdict={'size': 15})
# g.legend(title = "Rank")
# plt.xticks([x * 6 for x in range(ceil(d.id.max() / 6) + 1)], [x for x in range(ceil(d.id.max() / 6) + 1)])
# plt.show()

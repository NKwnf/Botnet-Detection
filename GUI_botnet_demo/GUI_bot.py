#!/usr/local/bin/python
# coding:utf-8

import time
import networkx as nx
import matplotlib.pyplot as plt

def GUI_bot():
	i=1
	time_s=5
	G=nx.Graph()
	col_dic={'normal':'r','Sality':'b','Kelihos':'g','infected-unknown':'m','ZeroAccess':'y','Storm':'c'}
	while i<=6:
		target_name='test_H'+str(i)+'.dat'
		file = open(target_name,'r')
		next(file)
		dictionary={}
		label={}
		for line in file:
			dictionary[line.split()[0]+' '+ line.split()[1]]=line.split()[2]
			label[line.split()[0]+' '+ line.split()[1]]=line.split()[1]

		i+=1
		file.close()
		G.clear()
		color=[]
		G=nx.Graph(name='net')
		keys=dictionary.keys()
		key_label=label.keys()

		for k in range(0,len(keys)):
			G.add_node(keys[k])
			color.append(col_dic[dictionary[keys[k]]])
			
			if k>0:
				for j in range(0,k):
					G.add_edge(keys[k],keys[j])
		

		nx.draw_circular(G,node_color=color,labels=label,node_size=3500)
		plt.show(0)
		print '\n\n'
		print target_name
		for k in range(0,len(keys)):
			print key_label[k]+'   '+dictionary[keys[k]]
		plt.pause(5)

if __name__ == '__main__':
	GUI_bot()
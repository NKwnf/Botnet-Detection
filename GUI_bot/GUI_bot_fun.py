#!/usr/local/bin/python
# coding:utf-8

import time, os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backend_bases as mbb

def rtpairs(r,n):
	for i in range(len(r)):
		for j in range(n[i]):    
			yield r[i], j*(2 * np.pi / n[i])

def read_mapping(filename):
	mapping = {}
	# print os.path.join(path, filename)
	file = open(filename , 'r')
	next(file)
	# print file
	for line in file:
		# print line
		mapping [line.split()[0]] = line.split()[1]
	file.close()
	print mapping
	return mapping

def read_status(filename):
	status = {}
	file = open(os.path.join(path,filename) , 'r')
	next(file)
	for line in file:
		status [line.split()[0] + ' ' + line.split()[1]] = line.split()[-1]
	file.close()
	return status

def read_connect(filename):
	connect = []
	file = open(os.path.join(path,filename) , 'r')
	next(file)
	for line in file:
		connect.append(line)
	file.close()
	return connect

def GUI_bot():
	initial_node = {}
	detection = {}
	G=nx.Graph()
	initial_node = read_mapping('initial_node_mappings.dat')
	color = []
	# print initial_node
	keys_initial_nopes = initial_node.keys()
	# print keys_initial_nopes
	detection = read_status('detection_08-31-2017-17-00-00_3600s.dat')
	mapping = read_connect('flows_08-31-2017-17-00-00_3600s.dat')
	# print mapping
	keys_detection = detection.keys()
	sel = []
	ax = plt.gca()
	####################################################
	T = [9]
	R = [20]
	x = []
	y = []
	for r, t in rtpairs(R, T):
		x.append(r * np.cos(t))
		y.append(r * np.sin(t))
	#################################################
	for i in range(0, len(keys_detection)):
		sel.append(keys_detection[i].split()[0])
	for k in range(0,len(keys_initial_nopes)):
		if len(keys_detection) < len(keys_initial_nopes):
			for l in range(0, len(keys_detection)):
				if keys_initial_nopes[k] not in sel[l]:
					if l == len(keys_detection) - 1:
						color.append('k')
				else:
					p = keys_initial_nopes[k] + ' ' + initial_node.get(keys_initial_nopes[k])
					color.append(col_dic[detection[p]])
					break
		else:
			color.append(col_dic[detection[keys_detection[k]]])
	# print color
	keys_col = col_dic.keys()
	ied_num = 0
	hmi_num = 0
	ws_num = 0
	col_set = list(set(color))
	# print col_set
	for i in range(0, len(col_set)):
		for j in range(0, len(keys_col)):
			if col_set[i] == col_dic[keys_col[j]]:
				label = keys_col[j]
				plt.plot (x[i], y[i], marker = 'o', color = col_set[i], markersize = 8, label = label)
			# node_shape[keys_initial_nopes[k]] = 'o'
				plt.legend(loc = (-0.15, 0.7), prop = {'size': 10}, title = 'Virus(Taking IED as an Example)', edgecolor = 'white')
				# set(h,'Box','off');
				break

	for i in range(0, len(color)):
		if initial_node[keys_initial_nopes[i]] == 'IED':
			for k in range(0, len(col_dic)):
				if col_dic[keys_col[k]] == color[i]:
					l = keys_col[k]
					break

			label = keys_initial_nopes[i] + ' ' + 'IED' + ' ' + l
			plt.plot (x[i], y[i], marker = 'o', color = color[i], markersize = 8, label = label)

			pp = 'IED' + str(ied_num)
			if x[i] >= 0 and y[i] >= 0:
				ax.annotate(pp, xy = (x[i] + 0.4,y[i] + 1), xytext=(x[i] + 5,y[i] + 5), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] < 0 and y[i] > 0:
				ax.annotate(pp, xy = (x[i] - 0.2,y[i] + 1), xytext=(x[i] - 5,y[i] + 7), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] <= 0 and y[i] <= 0:
				ax.annotate(pp, xy = (x[i] - 1,y[i] - 0.5), xytext=(x[i] - 13,y[i] - 6), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] > 0 and y[i] < 0:
				ax.annotate(pp, xy = (x[i] + 1,y[i] - 1), xytext=(x[i] + 6,y[i] - 6), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			# print keys_initial_nopes[i]
			ied_num += 1
		elif initial_node[keys_initial_nopes[i]] == 'HMI':
			for k in range(0, len(col_dic)):
				if col_dic[keys_col[k]] == color[i]:
					l = keys_col[k]
					break

			label = keys_initial_nopes[i] + ' ' + 'HMI' + ' ' + l

			plt.plot (x[i], y[i], marker = '^', color = color[i], markersize = 8, label = label)

			pp = 'HMI' + str(hmi_num)
			if x[i] >= 0 and y[i] >= 0:
				ax.annotate(pp, xy = (x[i] + 0.4,y[i] + 1), xytext=(x[i] + 5,y[i] + 5), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] < 0 and y[i] > 0:
				ax.annotate(pp, xy = (x[i] - 0.2,y[i] + 1), xytext=(x[i] - 5,y[i] + 7), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] <= 0 and y[i] <= 0:
				ax.annotate(pp, xy = (x[i] - 1,y[i] - 0.5), xytext=(x[i] - 13,y[i] - 6), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] > 0 and y[i] < 0:
				ax.annotate(pp, xy = (x[i] + 1,y[i] - 1), xytext=(x[i] + 6,y[i] - 6), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))

			# print keys_initial_nopes[i]
		else:
			for k in range(0, len(col_dic)):
				if col_dic[keys_col[k]] == color[i]:
					l = keys_col[k]
					break

			label = keys_initial_nopes[i] + ' ' + 'Workstation' + ' ' + l
			plt.plot (x[i], y[i], marker = 's', color = color[i], markersize = 8, label = label)
			# print keys_initial_nopes[i]
			pp = 'WS' + str(ws_num)
			if x[i] >= 0 and y[i] >= 0:
				ax.annotate(pp, xy = (x[i] + 0.4,y[i] + 1), xytext=(x[i] + 5,y[i] + 5), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] < 0 and y[i] > 0:
				ax.annotate(pp, xy = (x[i] - 0.2,y[i] + 1), xytext=(x[i] - 5,y[i] + 7), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] <= 0 and y[i] <= 0:
				ax.annotate(pp, xy = (x[i] - 1,y[i] - 0.5), xytext=(x[i] - 13,y[i] - 6), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))
			if x[i] > 0 and y[i] < 0:
				ax.annotate(pp, xy = (x[i] + 1,y[i] - 1), xytext=(x[i] + 6,y[i] - 6), arrowprops = dict(facecolor = 'yellow', shrink = 0.05))

	##################################################edge

	t = color.index('k')
	q = keys_initial_nopes[t]

	for i in range(0, len(color)):
		if color[i] == 'k':
			continue
		else:
			p = keys_initial_nopes[i].split()[0]
			for k in range(0, len(mapping)):
				if '255' in mapping[k].split()[-1]:
					if p == mapping[k].split()[0]:
						for kk in range(0, len(keys_initial_nopes)):
							if q != keys_initial_nopes[kk]:
								plt.plot([x[i], x[kk]], [y[i], y[kk]], color = '#778899', linewidth = 0.5)

	for i in range(0, len(color)):
		if color[i] == 'k':
			continue
		else:
			p = keys_initial_nopes[i].split()[0]
			for k in range(0, len(mapping)):
				if '255' not in mapping[k].split()[-1]:
					if p == mapping[k].split()[0]:
						if mapping[k].split()[-1] != q:
							kkk = keys_initial_nopes.index(mapping[k].split()[-1])

							plt.plot([x[i], x[kkk]], [y[i], y[kkk]], 'k', linewidth = 0.5)
				# else:
				# 	if p == mapping[k].split()[0]:
				# 		for kk in range(0, len(keys_initial_nopes)):
				# 			if q != keys_initial_nopes[kk]:
				# 				# kkk = keys_initial_nopes.index(mapping[k].split()[-1])
				# 			# plt.plot([x[i],x[k]], [y[i], y[k]])
				# 				plt.plot([x[i], x[kk]], [y[i], y[kk]], color = 'k', linewidth = 0.5)
								
	my_x_ticks = np.arange(-60, 60)
	my_y_ticks = np.arange(-55, 55)
	plt.xticks(my_x_ticks)
	plt.yticks(my_y_ticks)

	ax.axes.get_yaxis().set_visible(False)

	ax.axes.get_xaxis().set_visible(False)
	ax.spines['right'].set_color('none')
	ax.spines['top'].set_color('none')
	ax.spines['left'].set_color('none')
	ax.spines['bottom'].set_color('none')
	plt.text(-55,-55, 'IP__NODE \n 192.168.1.13: IED0 \n 192.168.1.12: IED1 \n 192.168.1.11: IED2 \n 192.168.1.10: IED3 \n 192.168.1.16: IED4 \n 192.168.1.15: IED5 \n 192.168.1.14: IED6 \n 192.168.1.53: WS0 \n 192.168.1.51: HMI0', ha = 'center')
	plt.show()
# 	plt.pause(5)

if __name__ == '__main__':
	global path, col_dic
	path = './'
	col_dic={'normal':'r','Sality':'b','Kelihos':'g','infected-unknown':'m','ZeroAccess':'y','Storm':'c', 'None':'k'}
	GUI_bot()
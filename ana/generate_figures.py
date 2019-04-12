# -*- coding: utf-8 -*-
# @Author: joaopn
# @Date:   2019-03-31 18:46:04
# @Last Modified by:   joaopn
# @Last Modified time: 2019-04-12 03:45:51

import analysis
import matplotlib.pyplot as plt
import numpy as np
import h5py
import os
import argparse

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 8

def states_parameters():

	#Defines state dict
	state_dict = {
		'poisson': {'m': 0.000, 'h': 2e-3},
		'subcritical': {'m': 0.900, 'h': 2e-4},
		'reverberant': {'m': 0.980, 'h': 4e-5},
		'critical': {'m': 0.999, 'h': 2e-6},
		'critical500': {'m': 0.996, 'h': 8e-6},
	}

	return state_dict

def pS_filepath(state,datatype,d,b,reps,threshold,data_dir, bw_filter):

	#Definitions
	state_dict = states_parameters()
	if bw_filter:
		saveplot_dir = 'analyzed_filtered/'
	else:
		saveplot_dir = 'analyzed_unfiltered/'

	#Sets up filepath
	m = state_dict[state]['m']
	h = state_dict[state]['h']
	dataset = 'm{:0.5f}_h{:0.3e}_d{:02d}_th{:0.1f}_rep{:02d}/'.format(m,h,d,threshold,reps)
	datafile = 'pS_' + datatype + '_b{:02d}.tsv'.format(b)
	str_load = data_dir + saveplot_dir + dataset + datafile

	return str_load

def thresholded_filepath(state,d,threshold,data_dir,bw_filter):

	#Parameters
	state_dict = states_parameters()
	if bw_filter:
		dir_threshold = 'thresholded_filtered/'
	else:
		dir_threshold = 'thresholded_unfiltered/'

	#Sets up filepath
	m = state_dict[state]['m']
	h = state_dict[state]['h']
	filename = 'm{:0.5f}_h{:0.3e}_d{:02d}_th{:0.1f}.hdf5'.format(m,h,d,threshold)
	str_load = data_dir + dir_threshold + filename

	return str_load

def plot_compare_states(datatype,b,d,reps,threshold,data_dir,bw_filter):

	#Sets up subfigure
	plt.xlabel('Avalanche size S')
	plt.ylabel('p(S)')
	plt.yscale('log')
	plt.xscale('log')
	plt.xlim(1,100)
	plt.ylim(1e-7,1)

	#Plots guiding line
	X = np.arange(5,64)
	Y = np.power(X,-1.5)
	Y = 5*Y/np.sum(Y)
	plt.plot(X,Y,linestyle='--',color='black',label=r'$p(S) \sim S^{-1.5}$')

	#Plots states
	states = ['subcritical','reverberant', 'critical']
	colors = ['blue', 'green', 'red']
	state_dict = states_parameters()

	for i in range(len(states)):

		#Get parameters
		
		m = state_dict[states[i]]['m']
		h = state_dict[states[i]]['h']

		#Plots distributions
		analysis.plot.sim_pS(m,h,d,b,datatype,reps,None,bw_filter,data_dir,threshold,colors[i])

def parametersDefault():

	#default Parameters
	figDefault = '1'
	binsizeDefault=4
	repsDefault = 50
	dDefault = 8
	datafolderDefault = 'dat/'
	bw_filterDefault = True

	#Parse input
	parser = argparse.ArgumentParser()

	#Add single parameters
	parser.add_argument("--datafolder",type=str,nargs='?',const=1,default=datafolderDefault)
	parser.add_argument("--reps",type=int,nargs='?',const=1,default=repsDefault)
	parser.add_argument("-b",type=int,nargs='?',const=1,default=binsizeDefault)
	parser.add_argument("-d",type=int,nargs='?',const=1,default=dDefault)
	parser.add_argument("--bw_filter",type=bool,nargs='?',const=1,default=bw_filterDefault)
	parser.add_argument("--fig",type=int,nargs='?',const=1,default=figDefault)
	
	args = parser.parse_args()

	return args

def color_gradient(color,num_colors, brightness_lim=0.8):
	"""Creates gradient color RGB matrices for the basic colors.

	Supported colors: 'red', 'green', 'blue', 'grey'.
	
	Args:
		color: color string, e.g. "red" or "r"
		num_colors: number of colors to generate
		brightness_lim: maximum brightness. Setting it to 1 means the last color is white (default: {0.8})
	"""
	color_rgb = np.zeros((num_colors,3))
	v_num = np.linspace(brightness_lim,0,num=num_colors)

	if color in ['r', 'red']:
		color_rgb[:,0] = darkness
		color_rgb[:,1] = v_num
		color_rgb[:,2] = v_num

	if color in ['g', 'green']:
		color_rgb[:,0] = v_num
		color_rgb[:,1] = 1
		color_rgb[:,2] = v_num

	if color in ['b', 'blue']:
		color_rgb[:,0] = v_num
		color_rgb[:,1] = v_num
		color_rgb[:,2] = 1

	if color in ['gray', 'grey']:
		color_rgb[:,0] = 0.499 + v_num/2
		color_rgb[:,1] = 0.499 + v_num/2
		color_rgb[:,2] = 0.499 + v_num/2

	return color_rgb

def color_gradient_rgba(color,num_colors, brightness_lim=0.8, primary_index = 0.545):
	"""Creates gradient colors RGBA matrices for basic colors
	
	Args:
		color: color string, accepts both e.g. 'r' and 'red'
		num_colors: number of colors to generate
		brightness_lim: maximum brightness (default: {0.8})
		primary_index: index of the base color. Setting it to 1 generates a pure tone (default: {0.545})
	
	Returns:
		color RGBA matrix
		float: [num_colors,4]
	"""

	color_rgba = np.zeros((num_colors,4))
	color_rgba[:,3] = np.linspace((1-brightness_lim),1,num_colors)

	if color in ['r', 'red']:
		color_rgba[:,0] = primary_index

	if color in ['g', 'green']:
		color_rgba[:,1] = primary_index

	if color in ['b', 'blue']:
		color_rgba[:,2] = primary_index

	if color in ['gray', 'grey']:
		color_rgba[:,0] = 0.2
		color_rgba[:,1] = 0.2
		color_rgba[:,2] = 0.2 

	return color_rgba

def figure_mav(data_dir,b,bw_filter):

	#Parameters
	fig_size = [7,7.5]
	Xticks = [2, 4, 6, 8, 10]
	Xticklabels = np.array(Xticks)*50
	linestyles = ['-','--', ':', '-.'] #Handles up to len(b) = 4

	#Parse input
	if type(b) is not list:
		b = [b]

	#Sets path
	if bw_filter:
		str_savepath = 'figs/fig3_filtered/'
	else:
		str_savepath = 'figs/fig3_unfiltered/'
	if not os.path.exists(str_savepath):
		os.makedirs(str_savepath)

	#Sets up figure
	plt.figure(figsize=(fig_size[0]/2.54,fig_size[1]/2.54))
	plt.xlabel(r'IED d ($\mu$m)')
	plt.ylabel(r'$m_{av}$')
	plt.xlim(1,10)
	plt.ylim(0.5,1.75)
	plt.yticks([0,0.5,1.,1.5])
	plt.xticks(Xticks)	
	plt.grid(False)
	ax = plt.gca()
	ax.set_axisbelow(True)
	ax.set_xticklabels(Xticklabels)

	#Plots states
	states = ['subcritical','critical']
	colors = ['blue', 'red']


	for j in range(len(b)):
		for i in range(len(states)):

			print('Plotting Fig 3 for the ' + states[i] + ' state.')
			#Get parameters
			state_dict = states_parameters()
			m = state_dict[states[i]]['m']
			h = state_dict[states[i]]['h']

			analysis.plot.sim_mav(m,h,b[j],data_dir,
				bw_filter=bw_filter, plt_color=colors[i],
				linestyle=linestyles[j])

		if j ==1:
			plt.legend(frameon=False)

	#Saves figure
	if len(b) == 1:
		str_save = str_savepath + 'mav_b{:02d}.pdf'.format(b)
	else:
		str_save = str_savepath + 'mav_combined.pdf'
	plt.savefig(str_save,bbox_inches="tight")
	plt.close()

def figure_1(data_dir,b,d,reps,bw_filter):

	#Parameters
	N = 160000
	threshold = 3
	rep_activity = 0 #timeseries to plot the activity from
	fig_activity_size = [5,2] #in cm
	fig_pS_size = [7,7.5]

	#Sets path
	if bw_filter:
		str_savepath = 'figs/fig1_filtered/'
	else:
		str_savepath = 'figs/fig1_unfiltered/'
	if not os.path.exists(str_savepath):
		os.makedirs(str_savepath)

	"""Generates timeseries figures"""
	print('Fig1: generating timeseries figures')
	states = ['subcritical', 'reverberant', 'critical']
	colors = ['blue', 'green','red']

	for i in range(len(states)):

		#Sets up figure
		plt.figure(figsize=(fig_activity_size[0]/2.54,fig_activity_size[1]/2.54))
		plt.xlim((0,10000))
		plt.ylim((0,4))
		plt.ylabel('Hz')

		#Loads data
		str_thresholded = thresholded_filepath(states[i],d,threshold,data_dir,bw_filter)
		file = h5py.File(str_thresholded,'r')
		activity_data = file['activity'][rep_activity,:]
		file.close()

		#Gets tau
		tau_ms = analysis.fitting.tau_linear(activity_data)

		#Plots data
		str_leg = r'$\tau = {:0.1f}$ ms'.format(tau_ms)
		plt.plot(activity_data*1000/N/2,color=colors[i], linewidth=1,label=str_leg)
		plt.legend(loc=1, frameon=False)

		#Removes x labels
		fig_gca = plt.gca()
		fig_gca.axes.xaxis.set_ticklabels([])
		fig_gca.set_yticks([0,2,4])


		#Saves plot
		str_save = str_savepath + 'activity_d{:02d}_rep{:02d}_'.format(d,rep_activity) + states[i] +'.pdf'
		plt.savefig(str_save,bbox_inches="tight")
		plt.close()


	"""Generates p(S) figures"""

	#Generates subsampled figure, removes legend
	print('Fig1: generating subsampled figure')
	plt.figure(figsize=(fig_pS_size[0]/2.54,fig_pS_size[1]/2.54))
	plot_compare_states('sub',b,d,reps,threshold,data_dir,bw_filter)
	str_save = str_savepath + 'sub_b{:02d}_d{:02d}.pdf'.format(b,d)
	plt.savefig(str_save,bbox_inches="tight")
	plt.close()


	#Generates coarse sampled figure
	print('Fig1: generating coarse sampled figure')
	plt.figure(figsize=(fig_pS_size[0]/2.54,fig_pS_size[1]/2.54))
	plot_compare_states('coarse',b,d,reps,threshold,data_dir,bw_filter)
	plt.legend(loc=3, frameon=False)
	str_save = str_savepath + 'coarse_b{:02d}_d{:02d}.pdf'.format(b,d)
	plt.savefig(str_save,bbox_inches="tight")
	plt.close()

def figure_2(data_dir,d,reps,bw_filter):

	#Parameters
	b = [1,2,4,8,16]
	threshold = 3
	datatype = 'coarse'
	fig_pS_size = [6,6]
	fig_alpha_size = [3,3]
	states = ['poisson', 'subcritical', 'reverberant', 'critical']
	state_colors = {
		'poisson':'green', 
		'subcritical':'blue', 
		'reverberant': 'gray', 
		'critical':'red'}

	#Sets path
	if bw_filter:
		str_savepath = 'figs/fig2_filtered/'
	else:
		str_savepath = 'figs/fig2_unfiltered/'
	if not os.path.exists(str_savepath):
		os.makedirs(str_savepath)

	#Gets state variables
	state_dict = state_dict = states_parameters()
	
	#Plots every state
	for state in states:
		m = state_dict[state]['m']
		h = state_dict[state]['h']
		print('Fig2: generating  plots for state:' + state)

		#Gets line colors
		plt_color = color_gradient_rgba(state_colors[state],len(b))

		#Plots and fits alpha = alpha(b) for non-poisson dynamics
		if state is not 'poisson':

			#Sets up figure
			plt.figure(figsize=(fig_alpha_size[0]/2.54,fig_alpha_size[1]/2.54))
			plt.xlabel(r'$\Delta$t')
			plt.ylabel(r'$\alpha$')
			plt.xscale('log')
			plt.yscale('log')
			plt.minorticks_off() #solves tick bu... "intended changes" in pyplot
			plt.xlim(1,100)
			plt.ylim(0.8,2)			
			plt.xticks([1,10,100])
			plt.yticks([1,1.5,2],['1', '1.5', '2'])

			#Plots and fits alpha(b)
			fit_exp, fit_err = analysis.plot.plot_alpha_bs(m,h,d,datatype,reps,bw_filter,data_dir,threshold, plt_color)

			#Saves alpha vs b fit to file
			str_save = str_savepath+'alpha_fitresults_d{:02d}.txt'.format(d)
			with open(str_save,'a') as file:
				str_fitdata = state + ': {:0.3f} +- {:0.3f}\n'.format(fit_exp,fit_err)
				file.write(str_fitdata)

			#Saves plot of alpha vs b
			str_save = str_savepath + 'fit_' + state + '_d{:02d}.pdf'.format(d)
			plt.savefig(str_save,bbox_inches="tight")
			plt.close()

		#Sets up pS figure
		plt.figure(figsize=(fig_pS_size[0]/2.54,fig_pS_size[1]/2.54))
		plt.xlabel('Avalanche size S')
		plt.ylabel('p(S)')
		plt.yscale('log')
		plt.xscale('log')
		plt.xlim(1,100)
		plt.ylim(1e-7,1)

		#Calculates tau
		tau_rep = analysis.fitting.tau_sim_dataset(m,h,int(d),threshold,data_dir,bw_filter)
		str_title = r'$\tau$ = {:0.1f}$\pm${:0.1f} ms'.format(np.mean(tau_rep),np.std(tau_rep))
		plt.title(str_title)

		#Plots it
		for i in range(len(b)):

			bs_leg = r"$\Delta$t = {:d} ms".format(2*b[i])

			analysis.plot.sim_pS(m,h,d,b[i],datatype,reps,
				label_plot=bs_leg,
				bw_filter=bw_filter,
				data_dir=data_dir,
				plt_color=plt_color[i,:],
				plt_std=False)		

		if state == 'poisson':
			plt.legend(frameon=False)

		#Saves plot
		str_save = str_savepath + 'coarse_' + state + '_d{:02d}.pdf'.format(d)
		plt.savefig(str_save,bbox_inches="tight")
		plt.close()

def figure_3(data_dir,reps,bw_filter):

	#Sets path
	if bw_filter:
		str_savepath = 'figs/fig3_filtered/'
	else:
		str_savepath = 'figs/fig3_unfiltered/'
	if not os.path.exists(str_savepath):
		os.makedirs(str_savepath)

	#Parameters
	fig_size = [7,7.5]
	b_mav = [2,4]
	b_ps = [2,2,2]
	d_ps = [1,4,10]
	threshold = 3
	
	#Saves (m_av vs d) figure
	figure_mav(data_dir,b_mav,bw_filter)

	#Plots comparison of different (b,d) configurations
	#Sets up figure
	plt.figure(figsize=(fig_size[0]/2.54,fig_size[1]/2.54))
	plt.xlabel('Avalanche size S')
	plt.ylabel('p(S)')
	plt.yscale('log')
	plt.xscale('log')
	plt.xlim(1,100)
	plt.ylim(1e-10,1)

	#Plots states
	states = ['subcritical', 'critical']
	colors = ['blue', 'red']
	offset_list = [1,1e-2,1e-4]
	state_dict = states_parameters()

	for j in range(len(b_ps)):
		for i in range(len(states)):

			#Get parameters		
			m = state_dict[states[i]]['m']
			h = state_dict[states[i]]['h']

			#Plots distributions
			analysis.plot.sim_pS(m,h,d_ps[j],b_ps[j],'coarse',reps,None,bw_filter,data_dir,threshold,colors[i],True,offset_list[j])	

	str_save = str_savepath + 'ps_comparison.pdf'
	plt.savefig(str_save,bbox_inches="tight")
	plt.close()

if __name__ == "__main__":

	parameters = parametersDefault()

	#Plots selected figures
	if parameters.fig == 1:
		figure_1(
			data_dir=parameters.datafolder,
			b=parameters.b,
			d=parameters.d,
			bw_filter=parameters.bw_filter, 
			reps=parameters.reps)

	if parameters.fig == 2:
		figure_2(
			data_dir=parameters.datafolder,
			d=parameters.d,
			bw_filter=parameters.bw_filter, 
			reps=parameters.reps)

	if parameters.fig == 3:
		figure_3(
			data_dir=parameters.datafolder,
			reps=parameters.reps,
			bw_filter = parameters.bw_filter)

#!/usr/bin/python


from ipywidgets import FloatSlider, IntSlider, interactive

def draw_my_plot(xstart, xstop, nbins,  n=70, p=50, jpower = 0):
	print xstart, xstop, nbins
	print n, p 
	print jpower


def draw_evrything():
	xstart_slider = IntSlider(value = 30, min=0, max=100, step=1)
	xstop_slider = IntSlider(value = 90, min=0, max=200, step=1)
	nbins_slider = IntSlider(value = 60, min=0, max=200, step=1)
	n_slider = FloatSlider(value = 70, min=0, max=100, step=0.1)
	p_slider = FloatSlider(value = 0.5, min=0, max=1, step=0.01)
	j_slider = IntSlider(value = 0, min = -6, max = 6, step = 1)
	w = interactive(draw_my_plot, xstart=xstart_slider, xstop=xstop_slider, nbins=nbins_slider, n=n_slider, p=p_slider, jpower=j_slider)
	return w

if __name__ == '__main__':
	main()
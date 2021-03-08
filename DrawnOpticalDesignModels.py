import numpy as np
import pandas as pd
#import OpticalDesign as OD
import ModelDesign as MODEL
import matplotlib.pyplot as plt

def vertices(Center, params, edge="external"):# Q eh o ponto central do hexagono estudado
    if edge=="external":
        V1 = Center+np.array([ -params['B']/2,-params['DV']/2])
        V2 = Center+np.array([-params['DH']/2,             +0])
        V3 = Center+np.array([ -params['B']/2,+params['DV']/2])
        V4 = Center+np.array([ +params['B']/2,+params['DV']/2])
        V5 = Center+np.array([+params['DH']/2,             +0])
        V6 = Center+np.array([ +params['B']/2,-params['DV']/2])
    elif edge=="internal":
        V1 = Center+np.array([ -params['b']/2,-params['dv']/2])
        V2 = Center+np.array([-params['dh']/2,             +0])
        V3 = Center+np.array([ -params['b']/2,+params['dv']/2])
        V4 = Center+np.array([ +params['b']/2,+params['dv']/2])
        V5 = Center+np.array([+params['dh']/2,             +0])
        V6 = Center+np.array([ +params['b']/2,-params['dv']/2])

    return np.array([V1,V2,V3,V4,V5,V6])
                    

def drawHexag(PC, params = None, Np = 0, dd = 21, 
              colorhexag ="red", colorcircle = "red", 
              plot_circle = True, 
              lshexag = "-", lscircle="-"):#PC = Ponto Central. De o ponto central e eh retornado o hexagonoBINGO
     
    PC = np.array([PC.y,PC.x]).T
     
    fillhexag  = False
    fillcircle = False
    if not colorhexag:
        colorhexag ="red"
    else:
        fillhexag  = True
    if not colorcircle:
        colorcircle ="red"
    else:
        fillcircle  = True
        
    for pc in PC:
        Pc=vertices(pc,params,edge="external")
        hexa = plt.Polygon(Pc, fill=fillhexag, edgecolor='black',facecolor=colorhexag,ls=lshexag)
        plt.gca().add_patch(hexa)
        Pc=vertices(pc,params,edge="internal")
        hexa = plt.Polygon(Pc, fill=fillhexag, edgecolor='black',facecolor=colorhexag,ls=lshexag)
        plt.gca().add_patch(hexa)        
        if plot_circle:
            for np_ in range(Np+1):
                if np==0:
                    circle = plt.Circle((pc[0], pc[1]+np_*dd), radius=params["horn diam"]/2.,fill=fillcircle, facecolor=colorcircle,ls=lscircle)
                    plt.gca().add_patch(circle)
                else:
                    circle = plt.Circle((pc[0], pc[1]+np_*dd), radius=params["horn diam"]/2.,fill=fillcircle, facecolor=colorcircle,ls=lscircle)
                    plt.gca().add_patch(circle)
                    circle = plt.Circle((pc[0], pc[1]-np_*dd), radius=params["horn diam"]/2.,fill=fillcircle, facecolor=colorcircle,ls=lscircle)
                    plt.gca().add_patch(circle)        


def draw(model=None):
	#model: hexagonal, rectangular, double rectangular, triple rectangular
	
	if model=="hexagonal":
		MODEL.Hexagonal()
	elif model=="rectangular":
		MODEL.Rectangular()
	elif model=="double rectangular":
		MODEL.DoubleRectangular()
	elif model=="triple rectangular":
		MODEL.TripleRectangular()
	else:
		raise Exception
		
def Rectangular(ax, shiftx=0, shifty=30., Np=0, displacement=15.,
                plot_circle  = False,
                colorhexag1  = False,colorhexag2  = False, lshexag  = "-",
                colorcircle1 = False,colorcircle2 = False, lscircle = "-"):

    params = MODEL.parameters("R")
    datas = MODEL.Rectangular(shiftx,shifty, Np, displacement)
	
    drawHexag(datas.col1, params, Np, displacement, colorhexag1, colorcircle1, plot_circle, lshexag, lscircle)
    drawHexag(datas.col2, params, Np, displacement, colorhexag1, colorcircle1, plot_circle, lshexag, lscircle)
    drawHexag(datas.col3, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
    drawHexag(datas.col4, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
    drawHexag(datas.col5, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
	

    plt.scatter(  0, 0, s=1,color="black")
    ax.set_xlabel('y (cm)' , fontsize=20)
    ax.set_ylabel('x (cm)' , fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.tick_params(axis='both', which='minor', labelsize=18)
    plt.gca().invert_yaxis()
    plt.grid(True)    

def DoubleRectangular(ax, shiftx=0,shifty=30., Np=0, displacement=15., 
            including_add_horns = True, plot_circle=False,
            colorhexag1    = False,colorhexag2     = False, lshexag      ="-",
            colorcircle1   = False,colorcircle2    = False, lscircle     ="-",
            colorhexag_add = False,colorcircle_add = False, lshexag_add  ="--", lscircle_add ="--"):
	params = MODEL.parameters("DR")
	
	datas  = MODEL.DoubleRectangular(shiftx,shifty, Np, displacement, including_add_horns=including_add_horns)
	drawHexag(datas.col1, params, Np, displacement, colorhexag1, colorcircle1, plot_circle, lshexag, lscircle)
	drawHexag(datas.col2, params, Np, displacement, colorhexag1, colorcircle1, plot_circle, lshexag, lscircle)
	drawHexag(datas.col3, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
	drawHexag(datas.col4, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
	
	if including_add_horns:
		X = []
		Y = []
		for j in [1,2,3,4]:
			x = datas["col"+str(j)].x[-1]
			X = np.hstack((X,x))
			y = datas["col"+str(j)].y[0]
			Y = np.hstack((Y,y))
		add = MODEL.DisplacementHorns({"x": X,"y":Y}, Np=Np, displacement=displacement)
		add = pd.DataFrame(add)
		drawHexag(add, params, Np, displacement, colorhexag_add, colorcircle_add, plot_circle, lshexag_add, lscircle_add )
	plt.scatter(  0, 0, s=1,color="black")
	ax.set_xlabel('y (cm)' , fontsize=20)
	ax.set_ylabel('x (cm)' , fontsize=20)
	ax.tick_params(axis='both', which='major', labelsize=20)
	ax.tick_params(axis='both', which='minor', labelsize=18)
	plt.gca().invert_yaxis()
	plt.grid(True)

def TripleRectangular(ax, shiftx=+131.25375, shifty=0., Np=0, displacement=15., 
            plot_circle=False,
            colorhexag1  = False, colorhexag2  = False, colorhexag3  = False, lshexag = "-",
            colorcircle1 = False, colorcircle2 = False, colorcircle3 = False, lscircle= "-"):
    
    params = MODEL.parameters("TR")
    
    datas  = MODEL.TripleRectangular(shiftx,shifty, Np, displacement)
    drawHexag(datas.col1, params, Np, displacement, colorhexag1, colorcircle1, plot_circle, lshexag, lscircle)
    drawHexag(datas.col2, params, Np, displacement, colorhexag1, colorcircle1, plot_circle, lshexag, lscircle)
    drawHexag(datas.col3, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
    drawHexag(datas.col4, params, Np, displacement, colorhexag2, colorcircle2, plot_circle, lshexag, lscircle)
    drawHexag(datas.col5, params, Np, displacement, colorhexag3, colorcircle3, plot_circle, lshexag, lscircle)
    drawHexag(datas.col6, params, Np, displacement, colorhexag3, colorcircle3, plot_circle, lshexag, lscircle)
    
    plt.scatter(0,0,s=1,color="black")
    ax.set_xlabel('y (cm)' , fontsize=20)
    ax.set_ylabel('x (cm)' , fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.tick_params(axis='both', which='minor', labelsize=18)
    plt.gca().invert_yaxis()
    plt.grid(True)



def Hexagonal(ax,plot_circle=False,colorhexag =False,colorcircle =False, lshexag = "-", lscircle = "-"):
    params = MODEL.parameters("French")
    datas = MODEL.Hexagonal()
    
    
    ##
    fillhexag  = False
    fillcircle = False
    if not colorhexag:
        colorhexag ="red"
    else:
        fillhexag  = True
    if not colorcircle:
        colorcircle ="red"
    else:
        fillcircle  = True
    ##
    
    for ix,iy in zip(datas.x,datas.y):
        C = np.array([iy,ix])
        verts= vertices(C,params, edge="external")
        hexa = plt.Polygon(verts, fill=fillhexag, edgecolor='black',facecolor=colorhexag,ls=lshexag)
        plt.gca().add_patch(hexa)
        verts= vertices(C,params, edge="internal")
        hexa = plt.Polygon(verts, fill=fillhexag, edgecolor='black',facecolor=colorhexag,ls=lshexag)
        plt.gca().add_patch(hexa)
        
        if plot_circle:
            circle = plt.Circle((iy, ix), radius=70, fc='y',fill=False,ls=lscircle)
            plt.gca().add_patch(circle)
    
    plt.scatter(0,0,s=1,color="black")
    ax.set_xlabel('y (cm)' , fontsize=20)
    ax.set_ylabel('x (cm)' , fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.tick_params(axis='both', which='minor', labelsize=18)
    plt.gca().invert_yaxis()
    plt.grid(True)

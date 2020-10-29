import numpy as np
import pandas as pd

def FrenchModel_positions_horn():
    x = np.array([-422., -232.,  -42.,  148., -517., -327., -137.,   53.,  243.,    -612., -422., -232.,  -42.,  148.,  338., -707., -517., -327.,
         -137.,   53.,  243., -802., -612., -422., -232.,  -42.,  148.,     338., -707., -517., -327., -137.,   53.,  243., -612., -422.,
         -232.,  -42.,  148.,  338., -517., -327., -137.,   53.,  243.,    -422., -232.,  -42.,  148.])

    y = np.array([-660., -660., -660., -660., -495., -495., -495., -495., -495.,       -330., -330., -330., -330., -330., -330., -165., -165., -165.,
         -165., -165., -165.,    0.,    0.,    0.,    0.,    0.,    0.,        0.,  165.,  165.,  165.,  165.,  165.,  165.,  330.,  330.,
          330.,  330.,  330.,  330.,  495.,  495.,  495.,  495.,  495.,      660.,  660.,  660.,  660.])
    return x,y

def parameters(design="DR"):
    if design=="R":
        DH = 249.44
        DV = 240.
        B  = 138.57
        dh = 233.2
        dv = 225.2
        b  = 129.08
        horn_diam=190.
        x  = (DH-B)/2.
        return {"DH":DH,"DV":DV,"dh":dh,"dv":dv,"B":B,"b":b,"horn diam":horn_diam,'x':x}    
    
    elif design=="DR":
        DH = 249.44
        DV = 240.
        B  = 138.57
        dh = 233.2
        dv = 225.2
        b  = 129.08
        horn_diam=190.
        x  = (DH-B)/2.
        return {"DH":DH,"DV":DV,"dh":dh,"dv":dv,"B":B,"b":b,"horn diam":horn_diam,'x':x}
        
    elif design=="TR":
        DH = 249.44
        DV = 240.
        B  = 138.57
        dh = 233.2
        dv = 225.2
        b  = 129.08
        horn_diam=190.
        x  = (DH-B)/2.
        return {"DH":DH,"DV":DV,"dh":dh,"dv":dv,"B":B,"b":b,"horn diam":horn_diam,'x':x}
    
    elif design=="French":
        DH = 192. #249.44
        DV = 190. #240.
        B  = DH/2.+40#138.57
        dh = DH-10#138.564 #233.2
        dv = DV-10
        b  = B-10.
        horn_diam=190.
        x  = (DH-B)/2.
        return {"DH":DH,"DV":DV,"dh":dh,"dv":dv,"B":B,"b":b,"horn diam":horn_diam,'x':x}
    
    else:
        raise NameError
        
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

def drawHexag(PC,params=None, Np=0,dd=21,colorhexag ="red",colorcircle ="red",plot_circle=True, lshexag="-", lscircle="-"):#PC = Ponto Central. De o ponto central e eh retornado o hexagonoBINGO

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
                    
                    
def PCcolfeeds(PCHref,params,nup,ndown):#PCref = Central Point of the reference hexagon, nsup = feeds above of the reference, ndown = feeds bellow of the reference
                                        #Function will return central horn of the column
    PCcol   = PCHref                    #Central points of the column
    UPfeeds = np.arange(1,1+nup)
    DOfeeds = np.arange(1,1+ndown)
    
    for n in UPfeeds:
        PCUn   = PCHref+np.array([0,+n*params['DV']])
        PCcol  = np.vstack([PCUn,PCcol])
    for n in DOfeeds:
        PCDn   = PCHref+np.array([0,-n*params['DV']])
        PCcol  = np.vstack([PCcol,PCDn])
    return PCcol

def AdditionHorns(colhorns=None, params=None, up=False, down=False , type_="dashed"):
    i1 = np.intersect1d(a[0][:],b[0][:])
    i2 = np.intersect1d(a[1][:],b[1][:])
    np.intersect1d(i1,i2)
    return None

def DisplacementHorns(col, Np=1., displacement=15.):
	newx = []
	for c in col["x"]:
		for j in np.arange(-Np,Np+1,1):
			c0 = c - j*displacement
			newx = np.hstack((newx,c0))
	newy = col['y'][0]*np.ones(len(newx))
	return {"x":newx,"y":newy}
	

def Rectangular(shiftx=0,shifty=30., Np=0, displacement=15.):
    params = parameters("R")
    
    C7   = np.array([0.,0.])
    C7_1 = C7 + np.array([-1*(params['DH']+params['B']),0])
    C7_2 = C7 + np.array([+1*(params['DH']+params['B']),0])
    C6_1 = C7 + np.array([-1*(params[ 'x']+params['B']),-params['DV']/2.])
    C6_2 = C7 + np.array([+1*(params[ 'x']+params['B']),-params['DV']/2.])

    Col1 = PCcolfeeds(C7_1,params=params,nup=2,ndown=3+1)
    Col2 = PCcolfeeds(C6_1,params=params,nup=2,ndown=3)
    Col3 = PCcolfeeds(C7  ,params=params,nup=2,ndown=3+1)
    Col4 = PCcolfeeds(C6_2,params=params,nup=2,ndown=3)
    Col5 = PCcolfeeds(C7_2,params=params,nup=2,ndown=3+1)

    col1 = DisplacementHorns({"x": Col1.T[1],"y":Col1.T[0]}, Np=Np, displacement=displacement)
    col2 = DisplacementHorns({"x": Col2.T[1],"y":Col2.T[0]}, Np=Np, displacement=displacement)
    col3 = DisplacementHorns({"x": Col3.T[1],"y":Col3.T[0]}, Np=Np, displacement=displacement)
    col4 = DisplacementHorns({"x": Col4.T[1],"y":Col4.T[0]}, Np=Np, displacement=displacement)
    col5 = DisplacementHorns({"x": Col5.T[1],"y":Col5.T[0]}, Np=Np, displacement=displacement)    
    
    return pd.DataFrame({"col1":col1,"col2":col2,"col3":col3,"col4":col4,"col5":col5})

def DoubleRectangular(shiftx=0,shifty=30., Np=0, displacement=15.,including_addition_horns=True):
    params = parameters("DR")
    
    shift  = 0      + np.array([                       shiftx,          shifty]) 
    P      = 0      + np.array([              -params['DH']/2, +params['DV']/2]) + shift
    Pshift = P      + np.array([              +params[ 'x']/4,            -0/1])
    Qshift = np.array([-Pshift[0],Pshift[1]]) + np.array([0,-params['DV']/4])   
    Tshift = Pshift + np.array([-1*(params['DH']+params['B'])/2,-params['DV']/2])
    Ushift = Qshift + np.array([ 1*(params['DH']+params['B'])/2,-params['DV']/2])
    
    if including_addition_horns:
        Col1 = PCcolfeeds(Tshift,params=params,nup=2,ndown=3+2)
        Col2 = PCcolfeeds(Pshift,params=params,nup=1,ndown=3+3)
        Col3 = PCcolfeeds(Qshift,params=params,nup=1,ndown=3+3)
        Col4 = PCcolfeeds(Ushift,params=params,nup=2,ndown=3+2)
    else:
		Col1 = PCcolfeeds(Tshift,params=params,nup=2,ndown=3+1)
		Col2 = PCcolfeeds(Pshift,params=params,nup=1,ndown=3+2)
		Col3 = PCcolfeeds(Qshift,params=params,nup=1,ndown=3+2)
		Col4 = PCcolfeeds(Ushift,params=params,nup=2,ndown=3+1)
    
    col1 = DisplacementHorns({"x": Col1.T[1],"y":Col1.T[0]}, Np=Np, displacement=displacement)
    col2 = DisplacementHorns({"x": Col2.T[1],"y":Col2.T[0]}, Np=Np, displacement=displacement)
    col3 = DisplacementHorns({"x": Col3.T[1],"y":Col3.T[0]}, Np=Np, displacement=displacement)
    col4 = DisplacementHorns({"x": Col4.T[1],"y":Col4.T[0]}, Np=Np, displacement=displacement)
    return pd.DataFrame({"col1":col1,"col2":col2,"col3":col3,"col4":col4})            

    
def TripleRectangular(shiftx=+131.25375, shifty=0., Np=0, displacement=15.):
    params = parameters("TR")

    shift    = 0 + np.array([         shiftx,          shifty])
    shiftALL = np.array([params['x']/3 -params['x'] -params['DH'] -2*params['x']/3, 0])+shift
    P        = 0 + np.array([-params['DH']/2, +params['DV']/2])
    Pshift = P + shiftALL + np.array([+params['x']/4,-0])
    Qshift = Pshift + np.array([    params['DH']+params['B'], 0]) + np.array([ params['x']/3., params['DV']/6.])
    Vshift = Pshift + np.array([2*(params['DH']+params['B']), 0]) + np.array([ 2*params['x']/3., 2*params['DV']/6.])

    Tshift = Pshift + np.array([-1*(params['DH']+params['B'])/2,-params['DV']/2])
    Ushift = Qshift + np.array([-1*(params['DH']+params['B'])/2,-params['DV']/2])
    Xshift = Vshift + np.array([-1*(params['DH']+params['B'])/2,-params['DV']/2])

    Col1 = PCcolfeeds(Tshift, params=params, nup=2,ndown=3)
    Col2 = PCcolfeeds(Pshift, params=params, nup=2,ndown=3)
    Col3 = PCcolfeeds(Qshift, params=params, nup=1,ndown=4)
    Col4 = PCcolfeeds(Ushift, params=params, nup=2,ndown=3)
    Col5 = PCcolfeeds(Vshift, params=params, nup=1,ndown=4)
    Col6 = PCcolfeeds(Xshift, params=params, nup=2,ndown=3)
    
    col1 = DisplacementHorns({"x": Col1.T[1],"y":Col1.T[0]}, Np=Np, displacement=displacement)
    col2 = DisplacementHorns({"x": Col2.T[1],"y":Col2.T[0]}, Np=Np, displacement=displacement)
    col3 = DisplacementHorns({"x": Col3.T[1],"y":Col3.T[0]}, Np=Np, displacement=displacement)
    col4 = DisplacementHorns({"x": Col4.T[1],"y":Col4.T[0]}, Np=Np, displacement=displacement)
    col5 = DisplacementHorns({"x": Col5.T[1],"y":Col5.T[0]}, Np=Np, displacement=displacement)   
    col6 = DisplacementHorns({"x": Col6.T[1],"y":Col6.T[0]}, Np=Np, displacement=displacement)   
    return pd.DataFrame({"col1":col1,"col2":col2,"col3":col3,"col4":col4,"col5":col5,"col6":col6})    

    
def Hexagonal():
    params = parameters("French")
    DV = params['DV']
    DH = params['DH']
    dh = params['dh']
    dv  = DV/2
    x   = (DH-dh)/2.
    b   = np.sqrt(x**2 + (dv)**2)

    P   = 0+np.array([-DH/2,+dv])
    Q   = P+np.array([  +DH, +0])
    x,y = FrenchModel_positions_horn()
    
    return pd.DataFrame({"x":x,"y":y})
    

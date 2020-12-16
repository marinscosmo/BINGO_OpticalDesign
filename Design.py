import numpy as np
import ReferenceSystem as ref
import Positions as pos
import matplotlib.pyplot as plt
def constants(type_):#p=(p)araboloide, h=(h)iperboloide
    if type_=="p": 
        ae =   20.              #elipse
        be =   20.              #elipse
        xe = -226.541493021072  #elipse
        ye =    0.              #elipse
        x0 =    0.              #paraboloide
        y0 =    0.              #paraboloide
        z0 =    0.              #paraboloide
        f  =  140.              #paraboloide
        return {"ae":ae,"be":be,"xe":xe,"ye":ye,"x0":x0,"y0":y0,"z0":z0,"f":f}
    elif type_=="h":
        ae =   18.3404081  #elipse
        be =   17.7752911  #elipse
        xe =   26.28830738 #elipse
        ye =    0.         #elipse
        x0 =    0.         #hiperboloide
        y0 =    0.         #hiperboloide
        z0 =  140.         #hiperboloide
        f  =  252.         #hiperboloide
        v  = -148.2352941  #hiperboloide
        return {"ae":ae,"be":be,"xe":xe,"ye":ye,"x0":x0,"y0":y0,"z0":z0,"f":f,"v":v}
    else:
        return None

    
def Reflector_datas(type_,num=500,coord_sys_bingo=False):#p=(p)araboloide, h=(h)iperboloide
    if type_=="p":             
        ###################################
        X,Y    = ref.coord(type_,num)
        consts = constants(type_)
        ###################################
        X,Y         = np.meshgrid(X,Y)
        X           = X.flatten()
        Y           = Y.flatten()
        Z           = z_paraboloide(X,Y,consts["f"])
        index       = elipsoide(X,Y,consts["xe"],consts["ye"],consts["ae"],consts["be"])
        index       = np.where(index==True)[0]
        X           = X[index]
        Y           = Y[index]
        Z           = Z[index]
        if coord_sys_bingo:
            old_Pos = np.array([X,Y,Z])
            X,Y,Z   = ref.NewSystem(old_Pos,nsystem="cut_bingo")
        ###################################
        return {"x":X,"y":Y,"z":Z}
        ###################################
    elif type_=="h":             
        ###################################
        X,Y    = ref.coord(type_,num)
        consts = constants(type_)
        ###################################
        X,Y         = np.meshgrid(X,Y)
        X           = X.flatten()
        Y           = Y.flatten()
        Z           = z_hiperboloide(X,Y,consts["f"],consts["v"])
        index       = elipsoide(X,Y,consts["xe"],consts["ye"],consts["ae"],consts["be"])
        index       = np.where(index==True)[0]
        old_Pos     = np.array([X[index],Y[index],Z[index]])
        X,Y,Z       = ref.NewSystem(old_Pos,nsystem="hyperbolic_in_sub") #rotaciona e desloca o espelho sec para o sistema sub
        if coord_sys_bingo:
            old_Pos = np.array([X,Y,Z])
            X,Y,Z   = ref.NewSystem(old_Pos,nsystem="cut_bingo")
        ###################################
        return {"x":X,"y":Y,"z":Z}
        ###################################

def z_paraboloide(x,y,f):
    return ((x)**2 + (y)**2)/(4*f)

def z_hiperboloide(x,y,f,v):
    a = v/2
    c = f/2
    b = np.sqrt(c**2 - a**2)
    #print("eccentricity: {}".format(c/a))
    return c - (a/b)*np.sqrt(b**2 + x**2 + y**2)

def elipsoide(x,y,xe,ye,ae,be,z=None,ze=None,ce=None,type_="p"):
    if type_=="p":
        value = (((x - xe)/ae)**2 + ((y - ye)/be)**2 - 1 <= 0)
    elif type_=="h":
        value = (((x - xe)/ae)**2 + ((y - ye)/be)**2 + ((z - ze)/ce)**2 - 1 <= 0)
    else:
        raise ValueError
    return value


def FocalPlane(columns=["1","2","3","4"], horn_column=8, coord_sys_bingo=False):
    Rs       = ref.Rotation(type_="xyz", csystem="sub")
    Rf       = ref.Rotation(type_="xyz", csystem="feed")
    x0,y0,z0 = ref.ReferenceSystem(csystem="sub")
    zf0      = ref.ReferenceSystem(csystem="feed")[2]
    
    versor_x_cut = np.array([1,0,0])
    versor_y_cut = np.array([0,1,0])
    versor_z_cut = np.array([0,0,1])
    
    zv = np.dot(Rs, versor_z_cut)
    
    xf = np.dot(np.dot(Rs,Rf),versor_x_cut)
    yf = np.dot(np.dot(Rs,Rf),versor_y_cut)
    zf = np.dot(np.dot(Rs,Rf),versor_z_cut)

    point = 140*np.array([0,0,1])+252*np.array([-0.996,  0., -0.0872])
    point = np.array([x0+zf0*zv[0], y0+zf0*zv[1], z0+zf0*zv[2]])
    if horn_column<=7:
        cols  = pos.position_DR(including_addition_horns = False, including_z=True, in_m=True)
    elif horn_column==8:
        cols  = pos.position_DR(including_addition_horns = True,  including_z=True, in_m=True)
    else:
        raise ValueError
 #   print(cols["col1"])
    for ii in range(int(horn_column)):
        for ist in columns:
            loc = cols['col'+ist]['x'][ii]*xf + cols['col'+ist]['y'][ii]*yf + cols['col'+ist]['z'][ii]*zf
            loc = np.array([point[0] + loc[0], point[1] + loc[1], point[2] + loc[2]])
            if ii==0 and ist==columns[0]:
                feeds = loc
            else:
                feeds = np.vstack((feeds,loc))
    X = feeds.T[0][:]
    Y = feeds.T[1][:]
    Z = feeds.T[2][:]
    if coord_sys_bingo:
        old_Pos = np.array([X,Y,Z])
        X,Y,Z   = ref.NewSystem(old_Pos,nsystem="cut_bingo")          
    return {"x":X,"y":Y,"z":Z}


def CoordinateTransform(X,Y,Z, coord_sys_bingo=False, unit_in="cm"):
	
    if unit_in=="m":
        pass
    elif unit_in=="cm":
        X = X/100.
        Y = Y/100.
        Z = Z/100.
    else:
        raise NameError
    Rs       = ref.Rotation(type_="xyz", csystem="sub")
    Rf       = ref.Rotation(type_="xyz", csystem="feed")
    x0,y0,z0 = ref.ReferenceSystem(csystem="sub")
    zf0      = ref.ReferenceSystem(csystem="feed")[2]
    
    versor_x_cut = np.array([1,0,0])
    versor_y_cut = np.array([0,1,0])
    versor_z_cut = np.array([0,0,1])
    
    zv = np.dot(Rs, versor_z_cut)
    
    xf = np.dot(np.dot(Rs,Rf),versor_x_cut)
    yf = np.dot(np.dot(Rs,Rf),versor_y_cut)
    zf = np.dot(np.dot(Rs,Rf),versor_z_cut)
    
    point = 140*np.array([0, 0, 1]) + 252*np.array([-0.996,  0., -0.0872])
    point = np.array([x0+zf0*zv[0], y0+zf0*zv[1], z0+zf0*zv[2]])    
    
    loc = X*xf + Y*yf + Z*zf
    loc = np.array([point[0] + loc[0], point[1] + loc[1], point[2] + loc[2]])
    
    X = loc[0]
    Y = loc[1]
    Z = loc[2]
    
    if coord_sys_bingo:
        old_Pos = np.array([X,Y,Z])
        X,Y,Z   = ref.NewSystem(old_Pos,nsystem="cut_bingo")          
    return {"x":X,"y":Y,"z":Z}


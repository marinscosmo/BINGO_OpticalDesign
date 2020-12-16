import numpy as np
import Design as design
import Positions as pos
def coord(type_,num=100):
    if   type_=="p":
        X  = np.linspace(-300,-100,num=num)
        Y  = np.linspace(-30, 30,num=num)
    elif type_=="h":
        X  = np.linspace(0, 300,num=num)
        Y  = np.linspace(-20, 20,num=num)
    return X,Y       
        

def ReferenceSystem(csystem):
    if   csystem == "global":
        return np.array([0.,0.,0.])
    elif csystem == "cut" or csystem == "cut_bingo":
        return np.array([-226.541493021072, 0., 91.6447286789582])
    elif csystem == "sub":
        return np.array([0.,0.,140.])
    elif csystem == "feed":
        return np.array([0.,0.,252.])
    return None

def Rotation(type_="xyz", csystem="sub"):
    if   csystem=="cut_bingo":
        R = np.array([[ 0.990364988565043,  0. ,-0.138481729569508], 
                      [ 0.               ,  1. , 0.               ], 
                      [ 0.138481729569508,  0. , 0.990364988565043]])
        
    elif csystem=="sub":
        R = np.array([[ 0.0871557,  0. , -0.9961947], 
                      [ 0.       , -1. ,  0.       ], 
                      [-0.9961947,  0. , -0.0871557]])
    elif csystem=="feed":
        R = np.array([[ 0.89315373386595 ,  0. , 0.449751495474237], 
                      [ 0.               , -1. , 0.               ], 
                      [ 0.449751495474237,  0. ,-0.89315373386595 ]])
    elif csystem=="unit" or csystem=="cut":
        R = np.array([[ 1., 0., 0.],
                      [ 0., 1., 0.], 
                      [ 0., 0., 1.]])
    else:
        R = np.array([[ 1., 0., 0.],
                      [ 0., 1., 0.], 
                      [ 0., 0., 1.]])
        
    if   type_=="xy" or type_=="yx":
        R = np.array([[ R[0,0], R[0,1]], 
                      [ R[1,0], R[1,1]]])
    elif type_=="xz" or type_=="zx":
        R = np.array([[ R[0,0], R[0,2]], 
                      [ R[2,0], R[2,2]]])
    elif type_=="yz" or type_=="zy":        
        R = np.array([[ R[1,1], R[1,2]], 
                      [ R[2,1], R[2,2]]])
    else:
        pass
    return R


def NewSystem(old_P,nsystem="hyperbolic_in_sub"):
    if nsystem=="hyperbolic_in_sub":
        new_X = []
        new_Y = []
        new_Z = []
        cte   = design.constants('h')
        R     = Rotation(type_="xyz", csystem="sub")
        S     = np.array([cte['x0'],cte['y0'],cte['z0']])

        for x,y,z in zip(old_P[0],old_P[1],old_P[2]):
            vec = np.array([x,y,z]) 
            vec = np.dot(R,vec)
            vec+=S
            new_X.append(vec[0])
            new_Y.append(vec[1])
            new_Z.append(vec[2])
        return np.asarray(new_X),np.asarray(new_Y),np.asarray(new_Z)
    
    elif nsystem=="cut_bingo":
        new_X = []
        new_Y = []
        new_Z = []        
        R     = Rotation(type_="xyz",csystem=nsystem)
        SGC   = ReferenceSystem(csystem="cut")
        if type(old_P[0])==np.ndarray:
            for x,y,z in zip(old_P[0],old_P[1],old_P[2]):
                r0G = np.array([x,y,z]) 
                r0C = r0G - SGC
                rC  = np.dot(R,r0C)
                rG  = rC + SGC
                new_X.append(rG[0])
                new_Y.append(rG[1])
                new_Z.append(rG[2])
            return np.asarray(new_X),np.asarray(new_Y),np.asarray(new_Z)
        elif type(old_P[0])==np.float64:
            r0G = old_P 
            r0C = r0G - SGC
            rC  = np.dot(R,r0C)
            rG  = rC + SGC
            return rG
        else:
            raise NameError

import numpy as np
def elipse_parameters(sub):
    x0 = (np.min(sub['x'])+np.max(sub['x']))/2.           #x-position of the center
    y0 = (np.min(sub['y'])+np.max(sub['y']))/2.           #y-position of the center
    a  = np.absolute(np.min(sub['x'])-np.max(sub['x']))/2.#radius on the x-axis
    b  = np.absolute(np.min(sub['y'])-np.max(sub['y']))/2.#radius on the y-axis
    return {"x0":x0,"y0":y0,"a":a,"b":b}

def elipse(sub, error=0.01):
    e = elipse_parameters(sub)
    value    = ((sub['x'] - e['x0'])/e['a'])**2 + ((sub['y'] - e['y0'])/e['b'])**2
    indTrue  = np.where((value > 1.- error)*(value < 1.+ error))[0]
    #indFalse = np.setdiff1d(np.arange(len(x)),indTrue)
    return indTrue#{"True":indTrue,"False":indFalse}
    
def new_index(sub,Ngrid,nppix, error_elipse=0.01):#numero por pixel
    #timei = time.time()
    nlim = int(nppix)
    ind  = []
    xg   = np.linspace(sub['x'].min(),sub['x'].max(),endpoint=True,num=Ngrid)
    yg   = np.linspace(sub['y'].min(),sub['y'].max(),endpoint=True,num=Ngrid)
    Nx   = len(xg)
    Ny   = len(yg)
    Xd   = sub['x']
    Yd   = sub['y']
    for iy in range(Ny-1):
        for ix in range(Nx-1):
            ind_ = np.where((Xd>=xg[ix])*(Xd<=xg[ix+1])*(Yd>=yg[iy])*(Yd<=yg[iy+1]))[0]
            n    = len(ind_)
            if n>nlim:
                count = int(n-nlim)
                ind_ = np.random.permutation(ind_)[:count]
                ind  = np.concatenate([ind,ind_])
    ind       = np.unique(ind).astype(int)
    indn      = np.setdiff1d(np.arange(len(Xd)),ind)
    indElipse = elipse(sub, error=0.01)
    indn      = np.setdiff1d(indn,indElipse)
    #print("tempo: {0:.3f} sec".format(-timei + time.time()))
    #print("antes = {}, depois = {}".format(len(Xd),len(indn)))
    return indn

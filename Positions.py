import numpy as np
import Horns as horns
def position_DR(shiftx=0,shifty=30., Np=0, desl_centre=15., 
                including_addition_horns = True, including_z=True,
                in_m = False):
    
    params = horns.parameters("DR")
    
    shift  = 0      + np.array([                       shiftx,          shifty]) 
    P      = 0      + np.array([              -params['DH']/2, +params['DV']/2]) + shift
    Pshift = P      + np.array([              +params[ 'x']/4,            -0/1])
    Qshift = np.array([-Pshift[0],Pshift[1]]) + np.array([0,-params['DV']/4])   
    Tshift = Pshift + np.array([-1*(params['DH']+params['B'])/2,-params['DV']/2])
    Ushift = Qshift + np.array([ 1*(params['DH']+params['B'])/2,-params['DV']/2])
    
    Col1 = horns.PCcolfeeds(Tshift,params=params,nup=2,ndown=3+1)
    Col2 = horns.PCcolfeeds(Pshift,params=params,nup=1,ndown=3+2)
    Col3 = horns.PCcolfeeds(Qshift,params=params,nup=1,ndown=3+2)
    Col4 = horns.PCcolfeeds(Ushift,params=params,nup=2,ndown=3+1)
    if including_addition_horns:
        Col1_ = horns.PCcolfeeds(Tshift,params=params,nup=2,ndown=3+2)[-1]
        Col2_ = horns.PCcolfeeds(Pshift,params=params,nup=1,ndown=3+3)[-1]
        Col3_ = horns.PCcolfeeds(Qshift,params=params,nup=1,ndown=3+3)[-1]
        Col4_ = horns.PCcolfeeds(Ushift,params=params,nup=2,ndown=3+2)[-1]
        Col1  = np.vstack((Col1,Col1_))
        Col2  = np.vstack((Col2,Col2_))
        Col3  = np.vstack((Col3,Col3_))
        Col4  = np.vstack((Col4,Col4_))
    if including_z:
        Col1 = horns.including_z_func(Col1, type_="DR", col_="1", Np=Np,including_addition_horns=including_addition_horns)
        Col2 = horns.including_z_func(Col2, type_="DR", col_="2", Np=Np,including_addition_horns=including_addition_horns)
        Col3 = horns.including_z_func(Col3, type_="DR", col_="3", Np=Np,including_addition_horns=including_addition_horns)
        Col4 = horns.including_z_func(Col4, type_="DR", col_="4", Np=Np,including_addition_horns=including_addition_horns)
    if in_m:
        Col1["x"] = Col1["x"]/100.
        Col1["y"] = Col1["y"]/100.
        Col1["z"] = Col1["z"]/100.
        Col2["x"] = Col2["x"]/100.
        Col2["y"] = Col2["y"]/100.
        Col2["z"] = Col2["z"]/100.
        Col3["x"] = Col3["x"]/100.
        Col3["y"] = Col3["y"]/100.
        Col3["z"] = Col3["z"]/100.
        Col4["x"] = Col4["x"]/100.
        Col4["y"] = Col4["y"]/100.
        Col4["z"] = Col4["z"]/100.
    
    Col1 = {"x":Col1["y"], "y":Col1["x"], "z":Col1["z"]}
    Col2 = {"x":Col2["y"], "y":Col2["x"], "z":Col2["z"]}
    Col3 = {"x":Col3["y"], "y":Col3["x"], "z":Col3["z"]}
    Col4 = {"x":Col4["y"], "y":Col4["x"], "z":Col4["z"]}
    return {"col1":Col1,"col2":Col2,"col3":Col3,"col4":Col4}

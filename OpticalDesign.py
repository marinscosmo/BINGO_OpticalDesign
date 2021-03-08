import scipy
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d


def load_data(type_=None):
	if type_=="optimization":
		data = pd.read_csv('data-optical-design.csv', encoding='ISO-8859-1')
	elif type_=="DNN":
		data = pd.read_csv('DNN_results.csv', encoding='ISO-8859-1')

	x     = data['x'].values
	y     = data['y'].values
	z     = data['z'].values
	if type_=="optimization":
		i     = data['Amp'].values
		mark  = data['marker'].values
	theta = data['theta'].values
	phi   = data['phi'].values

	x     = x.astype(np.float)
	y     = y.astype(np.float)
	z     = z.astype(str)
	if type_=="optimization":
		i = i.astype(str)
		mark  = mark.astype(str)
	theta = theta.astype(str)
	phi   = phi.astype(str)
	
	for j in range(len(z)):
		parts = z[j].split(",")
		
		try:    z[j] = float(".".join((parts[0],parts[1])))
		except: z[j] = float(parts[0])

	for j in range(len(theta)):
		parts = theta[j].split(",")
		
		try:    theta[j] = float(".".join((parts[0],parts[1])))
		except: theta[j] = float(parts[0])

	for j in range(len(phi)):
		parts = phi[j].split(",")
		
		try:    phi[j] = float(".".join((parts[0],parts[1])))
		except: phi[j] = float(parts[0])
	
	if type_=="optimization":
		for j in range(len(i)):
			parts = i[j].split(",")
			try:    i[j] = float(".".join((parts[0],parts[1])))
			except: i[j] = float(parts[0])        

	z     = z.astype(np.float)
	theta = theta.astype(np.float)
	phi   = phi.astype(np.float)
	if type_=="optimization":
		i = i.astype(np.float)
		return pd.DataFrame({"x":x,"y":y,"z":z,"theta":theta,"phi":phi,"I":i})
	else:
		return pd.DataFrame({"x":x,"y":y,"z":z,"theta":theta,"phi":phi})


def fitting_z(X_, a, b, c, d, e,f,g,h,i,j,k,l,m,n):
    return a + b*X_[0] + c*X_[1] + d*X_[0]*X_[1]  + e*X_[0]**2 + f*X_[1]**2  + g*(X_[0]**2)*X_[1] + h*X_[0]*X_[1]**2 + i*X_[0]**3 + j*X_[1]**3 + k*X_[0]**4 + l*X_[1]**4 + m/(X_[0] + 0.00001) + n/(X_[1] + 0.00001)

def fitting_theta(X_, a, b, c, d, e,f,g,h,i,j,k,l,m,n):
    return a + b*X_[0] + c*X_[1] + d*X_[0]*X_[1]  + e*X_[0]**2 + f*X_[1]**2  + g*(X_[0]**2)*X_[1] + h*X_[0]*X_[1]**2 + i*X_[0]**3 + j*X_[1]**3 + k*X_[0]**4 + l*X_[1]**4 + m/(X_[0] + 0.00001) + n/(X_[1] + 0.00001)

def fitting_phi(X_,a,b,c,d,e,f,g,h,i,j,k,l,m,n):
    return a + b*X_[0] + c*X_[1] + d*X_[0]*X_[1]  + e*X_[0]**2 + f*X_[1]**2  + g*(X_[0]**2)*X_[1] + h*X_[0]*X_[1]**2 + i*X_[0]**3 + j*X_[1]**3 + k*X_[0]**4 + l*X_[1]**4 + m/(X_[0] + 0.00001) + n/(X_[1] + 0.00001)


def fitting_parameters_std_values():
	cte_phi   = np.array([ 8.97870969e+01,  2.18345516e-01, -4.82762097e-08, -5.29898996e-11,  4.52465952e-05, -2.31915250e-05,	6.06778735e-14, -1.94152087e-07, -3.07097833e-07,  1.91585076e-13, -2.29281473e-10, -2.55851837e-11, -9.14543501e-04,  1.66724564e-05])
	cte_z     = np.array([ 1.09691186e+00, -4.81432066e-02, -1.37879361e-08,  1.49428782e-10,  2.05169768e-04,  7.59745004e-05, 3.83307490e-13,  1.97193057e-07,  3.86247340e-08, -8.43638267e-14, -1.08155705e-10,  5.41413911e-11,  5.21249391e-05, -6.30940319e-05])
	cte_theta = np.array([ 1.60791973e+00, -2.42180634e-03, -2.58242316e-08, -8.12084759e-11,  9.74693839e-06,  9.57415916e-06,-1.38957293e-13,  4.81071426e-09,  2.06847990e-09,  1.00047361e-13, -2.79036573e-12, -4.10120869e-12, -1.41613897e-05, -1.91784061e-06])
	return pd.DataFrame({"z":cte_z,"theta":cte_theta,"phi":cte_phi})
	
    
def fit_parameters(X=None,Y=None, calculated=False):
	if (isinstance(X,float) or isinstance(X,int))*(isinstance(Y,float) or isinstance(Y,int)):
		X = [float(X)]
		X = np.array(X)
		Y = [float(Y)]
		Y = np.array(Y)
	X = np.array(X,dtype=float)
	Y = np.array(Y,dtype=float)
	
	if calculated:			
		param = load_datas()
		XX    = scipy.array(param.x,    dtype=float)
		YY    = scipy.array(param.y,    dtype=float)
		Z     = scipy.array(param.z,    dtype=float)
		THETA = scipy.array(param.theta,dtype=float)
		PHI   = scipy.array(param.phi,  dtype=float)
		XY    = scipy.array([XX,YY])
		del param
		PHI   = np.absolute(PHI)
		
		#building fit
		cte_z,     cov_z     = curve_fit(fitting_z,     XY, Z)
		cte_theta, cov_theta = curve_fit(fitting_theta, XY, THETA)
		cte_phi,   cov_phi   = curve_fit(fitting_phi,   XY, PHI)
		
		cte = pd.DataFrame({"z":cte_z,"theta":cte_theta,"phi":cte_phi})
	else:
		cte = fitting_parameters_std_values()

	#To get values
	XY   = scipy.array([X,Y])
	Zfit = fitting_z(    XY,*cte.z)
	Tfit = fitting_theta(XY,*cte.theta)
	Pfit = fitting_phi(  XY,*cte.phi)

	#Correct Y values
	indp = np.where(Y>0.)
	indn = np.where(Y<=0.)
	Pfit[indp]=-np.absolute(Pfit[indp])
	Pfit[indn]=+np.absolute(Pfit[indn])
	
	return pd.DataFrame({"x":X,"y":Y,"z":Zfit,"theta":Tfit,"phi":Pfit})


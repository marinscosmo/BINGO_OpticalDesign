import numpy as np
import ReferenceSystem as ref
import matplotlib.pyplot as plt
import Design as design
def system(system = "global", ax = None,
                Dx=10., Dy=10., Dz=10., S=200, 
                axis   = "xyz", coord_sys_bingo=False, 
                color1 = "red", color2 = "green", color3 = "blue", colordot = "purple"):
    if axis=="xyz":
        if system=="global":
            R        = ref.Rotation(type_="xyz", csystem="unit")
            x0,y0,z0 = ref.ReferenceSystem(system)
            
            versor_x_cut = np.array([1,0,0])
            versor_y_cut = np.array([0,1,0])
            versor_z_cut = np.array([0,0,1])

            xv = np.dot(R,versor_x_cut)
            yv = np.dot(R,versor_y_cut)
            zv = np.dot(R,versor_z_cut)            

            ax.quiver( x0, y0, z0, Dx*xv[0], Dx*xv[1], Dx*xv[2], color=color1)
            ax.quiver( x0, y0, z0, Dy*yv[0], Dy*yv[1], Dy*yv[2], color=color2)
            ax.quiver( x0, y0, z0, Dz*zv[0], Dz*zv[1], Dz*zv[2], color=color3)
            ax.scatter(x0, y0, z0,      s=S,                     color=colordot)
            ax.text   (x0, y0, z0, system.upper())

        elif system=="cut":
            Rb           = ref.Rotation(type_="xyz", csystem=system)
            x0,y0,z0     = ref.ReferenceSystem(csystem=system)
            versor_x_cut = np.array([1,0,0])
            versor_y_cut = np.array([0,1,0])
            versor_z_cut = np.array([0,0,1])

            xv = np.dot(Rb,versor_x_cut)
            yv = np.dot(Rb,versor_y_cut)
            zv = np.dot(Rb,versor_z_cut)            

            ax.quiver( x0, y0, z0, Dx*xv[0], Dx*xv[1], Dx*xv[2], color=color1)
            ax.quiver( x0, y0, z0, Dy*yv[0], Dy*yv[1], Dy*yv[2], color=color2)
            ax.quiver( x0, y0, z0, Dz*zv[0], Dz*zv[1], Dz*zv[2], color=color3)
            ax.scatter(x0, y0, z0,      s=S,                     color=colordot)
            ax.text(   x0,y0,z0, system.upper())                    
            
        elif system=="cut_bingo":
            Rb       = ref.Rotation(type_="xyz", csystem=system)
            x0,y0,z0 = ref.ReferenceSystem(csystem=system)

            versor_x_cut = np.array([1,0,0])
            versor_y_cut = np.array([0,1,0])
            versor_z_cut = np.array([0,0,1])

            xv = np.dot(Rb,versor_x_cut)
            yv = np.dot(Rb,versor_y_cut)
            zv = np.dot(Rb,versor_z_cut)            

            ax.quiver( x0, y0, z0, Dx*xv[0], Dx*xv[1], Dx*xv[2], color=color1)
            ax.quiver( x0, y0, z0, Dy*yv[0], Dy*yv[1], Dy*yv[2], color=color2)
            ax.quiver( x0, y0, z0, Dz*zv[0], Dz*zv[1], Dz*zv[2], color=color3)
            ax.scatter(x0, y0, z0,      s=S,                     color=colordot)
            ax.text   (x0, y0, z0, "cut BINGO".upper())
            
        elif system=="sub":
            R        = ref.Rotation(csystem=system)
            x0,y0,z0 = ref.ReferenceSystem(system)

            versor_x_cut = np.array([1,0,0])
            versor_y_cut = np.array([0,1,0])
            versor_z_cut = np.array([0,0,1])

            xv = np.dot(R,versor_x_cut)
            yv = np.dot(R,versor_y_cut)
            zv = np.dot(R,versor_z_cut)         
            
            ax.quiver( x0, y0, z0, Dx*xv[0], Dx*xv[1], Dx*xv[2], color=color1)
            ax.quiver( x0, y0, z0, Dy*yv[0], Dy*yv[1], Dy*yv[2], color=color2)
            ax.quiver( x0, y0, z0, Dz*zv[0], Dz*zv[1], Dz*zv[2], color=color3)
            ax.scatter(x0, y0, z0,      s=S,                     color=colordot)
            ax.text(   x0,y0,z0, system.upper())

        elif system=="feed":
            Rb       = ref.Rotation(type_="xyz", csystem="cut_bingo")
            Rs       = ref.Rotation(type_="xyz", csystem="sub")
            Rf       = ref.Rotation(type_="xyz", csystem="feed")
            x0,y0,z0 = ref.ReferenceSystem(csystem="sub")

            versor_x_cut = np.array([1,0,0])
            versor_y_cut = np.array([0,1,0])
            versor_z_cut = np.array([0,0,1])

            xv  = np.dot(Rs,versor_x_cut)
            yv  = np.dot(Rs,versor_y_cut)
            zv  = np.dot(Rs,versor_z_cut)

            xv_ = np.dot(np.dot(Rs,Rf),versor_x_cut)
            yv_ = np.dot(np.dot(Rs,Rf),versor_y_cut)
            zv_ = np.dot(np.dot(Rs,Rf),versor_z_cut)

            x0 = x0+252*zv[0]
            y0 = y0+252*zv[1]
            z0 = z0+252*zv[2]
            
            if coord_sys_bingo:
                old_P    = np.array([x0,y0,z0])
                x0,y0,z0 = ref.NewSystem(old_P, nsystem="cut_bingo")
            
            ax.quiver( x0, y0, z0, Dx*xv[0], Dx*xv[1], Dx*xv[2], color=color1)
            ax.quiver( x0, y0, z0, Dy*yv[0], Dy*yv[1], Dy*yv[2], color=color2)
            ax.quiver( x0, y0, z0, Dz*zv[0], Dz*zv[1], Dz*zv[2], color=color3)
            ax.scatter(x0, y0, z0,      s=S,                     color=colordot)
            #ax.text(   x0, y0, z0, system.upper())
        else:
            raise Exception
    else:
        raise Exception
    plt.grid(True)
    return None

def plot_FocalPlane(Focal = None,ax=None,S=100, color="navy", columns=["1","2","3","4"], horn_column=8, coord_sys_bingo=False):    
    if Focal==None:
		Focal = design.FocalPlane(columns=columns, horn_column=horn_column, coord_sys_bingo= coord_sys_bingo)
    ax.scatter(Focal['x'], Focal['y'], Focal['z'], s=S, color=color)


def plotHistograms(reflector=None, kind="reflector2d", grid_lin = 0, bins_1d=200,bins_2d_x=100,bins_2d_y=100,sub=None,indn=None,grid=None):
    if kind=="reflector2d":
        ax = plt.subplot(grid[grid_lin,0])
        ax.scatter( reflector['z']      ,reflector['x']      , label="Sec tot" , color="black",s=5)
        ax.scatter( reflector['z'][indn],reflector['x'][indn], label="Sec part", color="gray",s=5)
        ax.set_xlabel("z (m)",color="blue")
        ax.set_ylabel("x (m)",color="red" )
        plt.legend(frameon=False, loc='lower left')
        plt.grid(True)

        ax = plt.subplot(grid[grid_lin,1])
        ax.scatter( reflector['x']      ,reflector['y']      , label="Sec tot", color="black",s=5)
        ax.scatter( reflector['x'][indn],reflector['y'][indn], label="Sec part", color="gray",s=5)
        ax.set_xlabel("x (m)",color="red"  )
        ax.set_ylabel("y (m)",color="green")
        plt.legend(frameon=False, loc='best')
        plt.grid(True)    
    
    elif kind=="hist1d":
        ax = plt.subplot(grid[grid_lin,0])
        plt.hist(reflector['x'],      bins=bins_1d, density=True)
        plt.hist(reflector['x'][indn],bins=bins_1d, density=True)
        plt.legend()

        ax = plt.subplot(grid[grid_lin,1])
        plt.hist(reflector['y']      ,bins=bins_1d, density=True)
        plt.hist(reflector['y'][indn],bins=bins_1d, density=True)
        plt.legend()
    
    elif kind=="hist2d":
        ax = plt.subplot(grid[grid_lin,0])
        plt.hist2d(reflector['x'],reflector['y'],bins=(bins_2d_x,bins_2d_y), cmap=plt.cm.jet, normed=True)
        plt.legend()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.colorbar()

        ax = plt.subplot(grid[grid_lin,1])
        plt.hist2d(reflector['x'][indn], reflector['y'][indn], bins=(bins_2d_x,bins_2d_y), cmap=plt.cm.jet, normed=True)
        plt.legend()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.colorbar()    

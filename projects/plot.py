import matplotlib.pyplot as plt
import numpy as np

def plotter(a,n, save=False):
    '''
    function that simply plots a*sin(x)^n in a new
    plt window
    '''
    x = np.arange(0.0, 5.0, 0.01)
    func = a*np.sin(x)**n

    plt.plot(x,func)

    #plt.title(r"$f(x)=a\sin(x)^n$ with a=%d, n=%d" %(a,n))
    plt.grid(True)
    plt.show()

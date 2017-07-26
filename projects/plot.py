import matplotlib.pyplot as plt
import numpy as np

def plotter(a1,n1, a2, n2):
    '''
    function that simply plots a*sin(x)^n in a new
    plt window
    '''
    x = np.arange(0.0, 5.0, 0.01)
    func1 = a1*np.sin(x)**n1
    func2 = a2*np.sin(x)**n2

    plt.figure()

    plt.subplot(211)
    plt.plot(x,func1, 'r--')
    plt.title(r"$y=%d*\sin(x)^{%d}$" %(a1, n1))
    plt.grid(True)

    plt.subplot(212)
    plt.plot(x, func2, 'b')
    plt.title(r"$y=%d*\sin(x)^{%d}$" %(a2,n2))
    plt.grid(True)
    plt.tight_layout()
    plt.show()


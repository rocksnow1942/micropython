import numpy as np
import matplotlib.pyplot as plt

k1 = 1
k2 = 0.05
R1 = k1 * 320
R2 = 1
R0 = np.linspace(50,400,1000)

base = (1+k1)*(1+k2)*R0 + (1+k1)*R2  + (1+k2)*R1
U2 = ((1+k2)*R0+R1+R2) / base 
U1 = ((1+k1)*R0+R1+R2) / base 
dU = U2 - U1 

fig,ax = plt.subplots(figsize=(4,8))
ax.plot(R0, U2,label='U2')
ax.plot(R0, dU,label='dU')
ax.set_ylim([-1,1])
ax.set_yticks(np.arange(-1,1,0.05))
ax.grid('on')
ax.legend()













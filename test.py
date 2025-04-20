from scipy.special import *
import numpy as np
from math import *

k1=(15/(15+2*60))
def my_ellipk(x):
    return ellipk(x**2)/ellipk(k1**2)
def my_ellipkinc(t,k):
    return _my_ellipkinc(1/k/t,k)#-1j*my_ellipk((1-k**2)**0.5)
def _my_ellipkinc(t,k):
    phi = np.arcsin(t)
    return ellipkinc(phi,k**2)/ellipk(k1**2)
def my_sn(z,k):
    return ellipj(z*ellipk(k1**2),k**2)[0]

hu=my_ellipk((1-k1**2)**0.5)

ns = range(1,11)
xi_n = np.array([n*75-7.5 for n in ns])
xo_n = np.array([n*75+7.5 for n in ns])
xc_n = np.array([(n+0.5)*75 for n in ns])

fxi_n = my_ellipkinc(xi_n/(15/2), k1)
fxo_n = my_ellipkinc(xo_n/(15/2), k1)
fxc_n = my_ellipkinc(xc_n/(15/2), k1)

wu_n =  fxi_n - fxo_n
slu_n = fxo_n - fxc_n
sru_n = fxc_n[:-1] - fxi_n[1:]
sru_n = np.append(0,sru_n)

print(sum(wu_n)+sum(slu_n)+sum(sru_n))

kk1 = my_ellipk(k1)
w_n = my_sn(2*kk1*(slu_n+wu_n-sru_n)/(wu_n+slu_n+sru_n), k1)-my_sn(2*kk1*(slu_n-wu_n-sru_n)/(wu_n+slu_n+sru_n),k1)
sl_n = my_sn(2*kk1*(slu_n-wu_n-sru_n)/(wu_n+slu_n+sru_n), k1)+1/k1
sr_n = 1/k1-my_sn(2*kk1*(slu_n+wu_n-sru_n)/(slu_n*wu_n+slu_n+sru_n), k1)

print(w_n+sl_n+sr_n)

k2_n = (sl_n*sr_n/(sl_n+w_n)/(sr_n+w_n))**0.5
print(k2_n,8.85*11.7*2*my_ellipk(k2_n)/my_ellipk((1-k2_n**2)**0.5)*0.01)

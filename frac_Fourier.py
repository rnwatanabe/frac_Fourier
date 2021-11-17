import torch
import math

__version__ = '0.1.0.dev0'

def FrFT(x, a, t, dt, a0=0, N=0):
    
    ang = a0
    if torch.abs(a%1) > 1e-6:
        angfr = torch.sign(a)*(torch.abs(a)%1)
        if torch.abs(angfr) < 0.5:
            x, t, ang = fractional_Fourier_transform(x, angfr - 1,t, dt, ang, N)
            x, t, ang = fractional_Fourier_transform(x, torch.Tensor([1]), t, dt, ang, N)
        else:
            x, t, ang = fractional_Fourier_transform(x, angfr, t, dt, ang, N)
    for i in range(int(a//1)):
        x, t, ang = fractional_Fourier_transform(x,torch.Tensor([1]),t, dt, ang, N)
    return x, t, ang

def fractional_Fourier_transform(x, a, t, dt0, a0, N=0):
    dt = t[1]-t[0]
    tamax = t[-1]-t[0]
    famax = 1/dt
    s = torch.sqrt(tamax/famax)
    tfmax = torch.sqrt(torch.round(tamax*famax))
    if N == 0: N = len(x)
    anew = a + a0
    xa = torch.zeros(2*N,1, dtype=torch.complex64)
    ta = ((torch.arange(len(xa)))/len(xa)*tfmax - tfmax/2).view(-1,1)
    

    x = sincinterp(x)
    x = x.view(-1,1)
    phi = torch.Tensor([a*math.pi/2])
    alpha = 1/(torch.tan(phi)+1e-6)
    beta = 1/(torch.sin(phi)+1e-6)
    Aphi = (torch.exp(-1j*math.pi*torch.sign(torch.sin(phi))/4+1j*phi/2))/(torch.sqrt(torch.abs(torch.sin(phi)))+1e-6)
    T = Aphi/(2*tfmax)*torch.exp(1j*math.pi*(alpha-beta)*ta.T**2)*torch.exp(1j*math.pi*beta*(ta.T-ta)**2)*torch.exp(1j*math.pi*(alpha-beta)*ta**2)
    xa1 = T@x
    print(T.shape)
    for i in range(len(ta)):      
        xa[i] = Aphi/(2*tfmax)*torch.exp(1j*math.pi*(alpha-beta)*ta[i]**2)*torch.sum(torch.exp(1j*math.pi*beta*(ta[i]-ta)**2)*torch.exp(1j*math.pi*(alpha-beta)*ta**2)*x)
    print(xa.shape)
    print(xa1.shape)
    print(torch.all(torch.abs(xa-xa1)<1e-12))
    if anew%2 != 0:
        ta = ta*torch.sin(anew%2*math.pi/2)/dt0/ta[-1]/2
    else:
        ta = ta*N*dt0/ta[-1]/2
    return xa[::2,0], ta[::2,0], anew

def fftconvolve(in1, in2):
    # Convolve two N-dimensional arrays using FFT. 
    # Convolution is implemented in the frequency domain, using the
    # Fast Fourier Transform.
    sp1 = torch.fft.fft(in1)
    sp2 = torch.fft.fft(in2)

    ret = torch.fft.ifft(sp1*sp2)

    return ret

def sincinterp(x):
    N = len(x)
    sinc_signal = torch.sinc(torch.arange(-2*N, 2*N)/2)
    y = torch.zeros(len(sinc_signal), dtype=x.dtype,)
    y[:2*N:2] = x
    
    y = fftconvolve(y, sinc_signal)[2*N:]
    return y
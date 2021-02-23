import numpy as np
from matplotlib.pyplot import axes, figure, colorbar, show 
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Circle

# The parameters
T0 = 50 # Exposure time
S0 = 2e2 # The brightness of the source
sigma = 2.0 #The FWHM of the source
Dark_strength0 = 10 # Dark current intensity
Bias_strength0 = 1 # Bias
LightPollutionStrength0 = 10 # Sky background
VMAX0 = 1500 # Display colorbar maxium
VMIN0 = 1000 # Display colorbar maxium
L = 101 # Size of the image 
Show_Cir = True # Show the aperture that do photometry
r1, r2, r3 = 5, 10, 20 # The size of the aperture

#=========================#

fig = figure(figsize=(8,8))

axcolor = 'lightgoldenrodyellow'
ax     = axes([0.15, 0.250, 0.7, 0.7]) 
axT    = axes([0.15, 0.200, 0.525, 0.02], facecolor=axcolor)
axS    = axes([0.15, 0.175, 0.525, 0.02], facecolor=axcolor)
axLP   = axes([0.15, 0.150, 0.525, 0.02], facecolor=axcolor)
axD    = axes([0.15, 0.125, 0.525, 0.02], facecolor=axcolor)
axVMAX = axes([0.15, 0.100, 0.525, 0.02], facecolor=axcolor)
axVMIN = axes([0.15, 0.075, 0.525, 0.02], facecolor=axcolor)
cbaxes = axes([0.90, 0.250, 0.030, 0.70]) 
resetax = axes([0.8, 0.075, 0.125, 0.06])
showCirax = axes([0.8, 0.15, 0.125, 0.06])

sT   = Slider(axT , 'Exposure Time',   0, 100, valinit=T0)
sS   = Slider(axS , 'Source',          0, 2e3, valinit=S0)
sLP  = Slider(axLP, 'Light Pollution', 0, 100, valinit=LightPollutionStrength0)
sD   = Slider(axD,  'Dark',            0, 100, valinit=Dark_strength0)
sVMAX= Slider(axVMAX, 'VMAX',          0, 2e4, valinit=VMAX0)
sVMIN= Slider(axVMIN, 'VMIN',          0, 2e4, valinit=VMIN0)

x = np.arange(0, L)
y = np.arange(0, L)
cx, cy = int(L/2), int(L/2)
mask1 = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r1**2
mask2 = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 > r2**2
mask3 = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r3**2
ring = np.logical_and(mask2, mask3)

#=========================#

def Make_Image(T, S, Dark_strength, Bias_strength, LightPollutionStrength):
    D = np.zeros((L,L)) #The array we draw on
    mu = int(L/2) # The center of the star
    
    # Source
    # Making a 2D guassian array
    x = np.linspace(0,L,L)
    g = 1/(sigma*np.sqrt(2*np.pi))*np.exp(-1/2*(x-mu)**2/sigma**2)
    gg = np.outer(g,g)
    Star = S*T*gg
    #Source_noise = np.random.normal(size = (L,L), loc = 0, scale = Star**0.5) # Noise N ~ S**0.5
    Source_noise = np.random.poisson(size = (L,L), lam = Star**0.5) # Noise N ~ S**0.5
    
    # Dark
    Dark = np.ones((L,L))*Dark_strength*T
    #Dark_noise = np.random.normal(loc = 0, size = (L,L), scale = Dark**0.5)
    Dark_noise = np.random.poisson(size = (L,L), lam = Dark**0.5)
    
    # Bias (No pattern for now)
    Bias = np.ones((L,L))*Bias_strength
    
    # Assuming uniform sky background, actually not only light pollution, but... whatever.
    LightPollution = np.ones((L,L))*LightPollutionStrength*T
    #LP_noise = np.random.normal(loc = 0, size = (L,L), scale = LightPollution**0.5)
    LP_noise = np.random.poisson(size = (L,L), lam = LightPollution**0.5)
    
    # Add all the frames
    D += (Star + Source_noise + Dark + Dark_noise + Bias + LightPollution + LP_noise)
    return D

# Measure SNR
def Photometry(D):
    SourceCount = np.sum(D[mask1])-np.mean(D[ring])*np.sum(mask1)
    #Noise = np.std(D[ring])*np.sum(mask1)**0.5
    Noise = np.sqrt(np.sum(D[mask1])) + np.std(D[ring])/np.sum(D[ring])*np.sum(D[mask1])
    SNR = SourceCount / Noise
    return SNR

# Draw the image
img = Make_Image(T0, S0, Dark_strength0, Bias_strength0, LightPollutionStrength0)
IMAGE = ax.imshow(img, vmax=VMAX0, vmin=VMIN0, cmap = 'gray')

# Draw the aperture for reference
ax.set_title('SNR: {:.4f}'.format(Photometry(img)))
circ1 = Circle((int(L/2),int(L/2)), r1, facecolor='none', edgecolor='red', lw=2)
circ2 = Circle((int(L/2),int(L/2)), r2, facecolor='none', edgecolor='red', lw=2)
circ3 = Circle((int(L/2),int(L/2)), r3, facecolor='none', edgecolor='red', lw=2)
ax.add_patch(circ1)
ax.add_patch(circ2)
ax.add_patch(circ3)

# Changing parameters
def updatefig(val):
    T = sT.val
    S = sS.val
    LightPollutionStrength = sLP.val
    Dark_strength = sD.val
    NewD = Make_Image(T, S, Dark_strength, Bias_strength0, LightPollutionStrength)
    IMAGE.set_data(NewD)
    ax.set_title('SNR: {:.4f}'.format(Photometry(NewD)))
    fig.canvas.draw_idle()

# Changing the colorbar scale
def updateclim(val):
    VMAX = sVMAX.val
    VMIN = sVMIN.val
    IMAGE.set_clim(VMIN, VMAX)
    fig.canvas.draw_idle()

sT.on_changed(updatefig)
sS.on_changed(updatefig)
sLP.on_changed(updatefig)
sD.on_changed(updatefig)
sVMAX.on_changed(updateclim)
sVMIN.on_changed(updateclim)

# Reset and switch for the apertures
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
buttonCir = Button(showCirax, 'Aperture', color=axcolor, hovercolor='0.975')

def reset(event):
    sT.reset()
    sS.reset()
    sLP.reset()
    sD.reset()
    sVMAX.reset()
    sVMIN.reset()

def Switch_Show(event):
    global Show_Cir
    Show_Cir = not Show_Cir
    circ1.set_visible(Show_Cir)
    circ2.set_visible(Show_Cir)
    circ3.set_visible(Show_Cir)

button.on_clicked(reset)
buttonCir.on_clicked(Switch_Show)
cb = colorbar(IMAGE, cax = cbaxes, pad = 0.)

# Show the image
show()

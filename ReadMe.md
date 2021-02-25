# CCD Image Simulator
## Abstract
This program aims to provide an simple but interactive experience on how different factor would effect the resulting image quality in astrophotography.
The code has two versions:

1. AstroDemo.py:
The simpler verison which only use functions in numpy and matplotlib. In this program, we assume a gaussian PSF, no readout noise.

2. AstroDemo_Fancy.py:
The more complicated version which aims to provide a more sophisticated simulation. Currently, we use 2d airy disk for PSF.

The code is still in development and could contain bugs and mistakes.

## What is the code trying to teach the students?
One common misconception is that dark, bias and sky background are "noise" in the image. However, that is not an accurate description.
Dark, bias and sky background are the signals that we don't want to include in our image, but they are not noise. Dark, bias and sky are, to the first order, removable and does not effect the quality (SNR) of your image.

Then...does that means it is OK to have a strong dark current and light pollution?
No, apperently we don't want to have strong dark current and sky background. However, it is not because dark and sky would raise up the value of the pixels, but because the "noise" that would come along with them.


# Image-to-Image Style Transfer with CycleGANs

A Github repo for an image-to-image style transfer CycleGAN web app

Web app hosted on Heroku and can be found [here](https://style-transfer-cycle-gan.herokuapp.com/). Expect a bit of a delay after clicking the link. I am using Heroku's free dyno and (paraphrasing from Heroku here) a free dyno that doesn't receive web traffic in a 30-minute period will go to sleep. In addition to the web dyno sleeping, the worker dyno (if present) will also sleep. If a sleeping web dyno receives web traffic, it will become active again after a short delay. 

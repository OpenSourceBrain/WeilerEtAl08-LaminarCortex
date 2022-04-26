## Top-down laminar organization of the excitatory network in motor cortex

[![Continuous build using OMV](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/actions/workflows/omv-ci.yml/badge.svg)](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/actions/workflows/omv-ci.yml)

Models based on data in:  Weiler N, Wood L, Yu J, Solla SA, Shepherd GM (2008) [Top-down laminar organization of the 
excitatory network in motor cortex](http://www.nature.com/neuro/journal/v11/n3/full/nn2049.html). Nat Neurosci 11:360-6

### Python implementation

So far a version of the [original model file in MATLAB](http://senselab.med.yale.edu/ModelDB/showmodel.cshtml?model=114655) has been [converted to Python](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/Python/laminarWsimulation.py), 
for ease of integration with other Python scripts being developed to use the data from the Weiler et al., 2008 paper.

This can be run with (after installing Numpy):

    cd Python 
    python laminarWsimulation.py

![Python impl](https://raw.githubusercontent.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/master/Python/weiler.png)

The y axis bins 0-8 represent **normalised cortical depth** (yfract). Bin 0 represents a normalized cortical depth between 0.1 and 0.2; 
bin 1 between 0.2 and 0.3; and so on. Each bin represents ~140um of cortical depth, and does not correspond to classical layer boundaries.


### NeuroML implementation

A set of scripts has been created to enable generation of simple (integrate & fire or single compartment HH cell model) cortical networks 
using this connectivity data.

See [GenerateLayeredNetwork.py](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/NeuroML2/GenerateLayeredNetwork.py) 
for example, which uses [libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) to generate [NeuroML 2](https://neuroml.org/neuromlv2) 
descriptions of the [populations & projections in the network](https://neuroml.org/NeuroML2CoreTypes/Networks.html). See generated 
example [here](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/NeuroML2/LayeredCortexDemo.net.nml).

The data used is the connectivity matrix from the above Python code (based on the original Matlab file). It is visualised below:

![](https://raw.githubusercontent.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/master/Python/connectivity.png)

The network can be visualised in OSB (see [here](http://opensourcebrain.org/projects/weileretal08-laminarcortex?explorer=https%3A%2F%2Fraw.githubusercontent.com%2FOpenSourceBrain%2FWeilerEtAl08-LaminarCortex%2Fmaster%2FNeuroML2%2FLayeredCortexDemo.net.nml))

![](https://raw.githubusercontent.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/master/NeuroML2/connectivity.jpg)

Clicking on individual cells highlights the connectivity of that cell, e.g. for cells in bin 0 (top of column) there are many connections, particularly to cells in bin 3:

![](https://raw.githubusercontent.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/master/NeuroML2/connA.jpg)

but fewer connections from a cell in lower bins:

![](https://raw.githubusercontent.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/master/NeuroML2/connB.jpg)

This network has connetivity, but no spiking activity yet. [Another python script](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/NeuroML2/GenerateNetwork.py) 
produces a [spiking network model](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/NeuroML2/CortexDemoHH.net.nml) 
(which can be run with [jNeuroML](https://github.com/NeuroML/jNeuroML)). 

The layered network will soon be updated with inputs and then propagation of inputs focussed on individual laminar layers to the rest of the network can be examined.

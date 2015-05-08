## Top-down laminar organization of the excitatory network in motor cortex

Models based on data in:  Weiler N, Wood L, Yu J, Solla SA, Shepherd GM (2008) [Top-down laminar organization of the excitatory network in motor cortex](http://www.nature.com/neuro/journal/v11/n3/full/nn2049.html). Nat Neurosci 11:360-6

### Python implementation

So far a version of the [original model file in MATLAB](http://senselab.med.yale.edu/ModelDB/showmodel.cshtml?model=114655&file=\laminarWsimulation\laminarWsimulation.m) has been [converted to Python](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/Python/laminarWsimulation.py), for ease of integration with other Python scripts being developed to use the data from the Weiler et al., 2008 paper.

This can be run with (after installing Numpy):

    cd Python 
    python laminarWsimulation.py

![Python impl](https://raw.githubusercontent.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/master/Python/weiler.png)


### NeuroML implementation

A set of scripts has been created to enable generation of simple (integrate & fire or single compartment HH cell model) cortical networks using this connectivity data.

See [GenerateLayeredNetwork.py](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/NeuroML2/GenerateLayeredNetwork.py) for example, which uses [libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) to generate [NeuroML 2](https://neuroml.org/neuromlv2) descriptions of the [populations & projections in the network](https://neuroml.org/NeuroML2CoreTypes/Networks.html). See generated example [here](https://github.com/OpenSourceBrain/WeilerEtAl08-LaminarCortex/blob/master/NeuroML2/LayeredCortexDemo.net.nml).



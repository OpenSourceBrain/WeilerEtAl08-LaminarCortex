'''
This file has been converted from MATLAB (see 
http://senselab.med.yale.edu/ModelDB/showmodel.cshtml?model=114655&file=\laminarWsimulation\laminarWsimulation.m)
to Python, for ease of integration with other Python scripts being developed to use the data from the 
Weiler et al., 2008 paper

'''

import matplotlib.pyplot as pylab
import numpy

def laminarWsimulation(gain = 1, W = None, inputvector = None, iterations = 10):
    # Based on comments in original MATLAB
    # laminarWsimulation
    #
    # Simulates the flow of activity within and across laminar levels in the 
    # local pyramidal neuron network, based on a connectivity matrix (W) 
    # measured by laser scanning photostimulation.
    #
    # The simulation is a simple neural network simulation:
    #
    # p(n) ----> c * W ----> p(n+1)
    #
    # where p(n=0) is an input vector ('inputvector') representing a laminar 
    # profile of activity, c is a global scaling constant ('gain'), W is a 
    # measured connectivity matrix, and p(n+1) is an output vector, which is 
    # fed back into the network as the input vector for the next iteration.
    #
    # For further details, see Weiler et al., 2008, Nature Neuroscience.

    # 2008 Gordon Shepherd, Northwestern University
    # ---------------------------------------------------------------------

    if W == None or inputvector == None:
        W = getW('mouse somatic M1');
        inputvector = numpy.zeros((len(W[0]),iterations+1))
        inputvector[0][0] = 1 # modify to change laminar input pattern
 
    
    for I in range(iterations):
        print("Computing step %i..."%I)
        
        for J in range(len(W[0])):
            next = 0 
            for K in range(len(W[0])):
                next += (inputvector[K][I] * W[K][J]) * gain
            
            inputvector[J][I+1] = next 
            
        
        

    
    pylab.figure()
    pylab.xlabel('Post')
    pylab.ylabel('Pre')
    pylab.title('Connectivity matrix')
    pylab.imshow(W, interpolation='none')
    pylab.colorbar()
    
    pylab.figure()
    pylab.xlabel('Iteration (number)')
    pylab.ylabel('Laminar level (cortical depth)')
    pylab.title('Simulated flow of network activity')
    pylab.imshow(inputvector, interpolation='none')
    pylab.colorbar()
    
    pylab.show()

def getW(datasetname):
    if datasetname == 'mouse somatic M1':
        out = [
            [ 0.1720,   0.1036,   0.2159,    1.0000,   0.4482,   0.0710,   0.0312,   0.0147,   0.0044 ],
            [ 0.0885,   0.0937,   0.1043,   0.2385,   0.2511,   0.0431,   0.0227,   -0.0003,   0.0016 ],
            [ 0.1181,   0.1545,   0.0659,   0.0768,   0.1320,   0.0442,   0.0463,   0.0112,   -0.0050 ],
            [ 0.1193,   0.0668,   0.0520,   0.1136,   0.1011,   0.0636,   0.0574,   0.0283,   0.0039 ],
            [ 0.0344,   0.0407,   0.0347,   0.0764,   0.1104,   0.0834,   0.1087,   0.0434,   0.0053 ],
            [ 0.0021,   0.0186,   0.0142,   0.0428,   0.1195,   0.1198,   0.1328,   0.0591,   0.0113 ],
            [ -0.0028,   0.0028,   0.0182,   0.0266,   0.1068,   0.1327,   0.1074,   0.0599,   0.0247 ],
            [ 0.0007,   0.0013,   0.0198,   0.0204,   0.0621,   0.1151,   0.1268,   0.0673,   0.0321 ],
            [ 0.0067,   0.0031,   0.0071,   0.0061,   0.0249,   0.0289,   0.0409,   0.0502,   0.0384 ]
        ]
    return numpy.array(out)
    
    
if __name__ == "__main__":
    laminarWsimulation()

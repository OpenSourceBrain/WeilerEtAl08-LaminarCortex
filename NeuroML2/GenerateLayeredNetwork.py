#
#

from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import Population
from neuroml import Location
from neuroml import Instance
from neuroml import Projection
from neuroml import Connection
from neuroml import IncludeType
from neuroml import InputList
from neuroml import Input
from neuroml import PoissonFiringSynapse

from neuroml import __version__

import neuroml.writers as writers

from pyneuroml import pynml
from pyneuroml.lems.LEMSSimulation import LEMSSimulation

from random import random
from random import seed

import numpy

#TODO: check why some of these values are negative??
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




def add_connection(projection, id, pre_pop, pre_component, pre_cell_id, pre_seg_id, post_pop, post_component, post_cell_id, post_seg_id):

    connection = Connection(id=id, \
                            pre_cell_id="../%s/%i/%s"%(pre_pop, pre_cell_id, pre_component), \
                            pre_segment_id=pre_seg_id, \
                            pre_fraction_along=0.5,
                            post_cell_id="../%s/%i/%s"%(post_pop, post_cell_id, post_component), \
                            post_segment_id=post_seg_id,
                            post_fraction_along=0.5)

    projection.connections.append(connection)


def generate_layered_network(network_id,
                             numCells_exc_per_layer,
                             numCells_inh_per_layer,
                             num_layers = 10,
                             x_size = 1000,
                             layer_y_size = 100, 
                             z_size = 1000,
                             exc_group_component = "SimpleIaF",
                             inh_group_component = "SimpleIaF_inh",
                             validate = True,
                             random_seed = 1234,
                             generate_lems_simulation = False,
                             connections = True,
                             connection_probability_exc_exc =   0.4,
                             connection_probability_inh_exc =   0.4,
                             connection_probability_exc_inh =   0.4,
                             connection_probability_inh_inh =   0.4,
                             inputs = False,
                             input_firing_rate = 50, # Hz
                             num_inputs_per_exc = 4,
                             duration = 500,  # ms
                             dt = 0.05,
                             temperature="32.0 degC"):

    seed(random_seed)

    nml_doc = NeuroMLDocument(id=network_id)

    net = Network(id = network_id, 
                  type = "networkWithTemperature",
                  temperature = temperature)
                  
    net.notes = "Network generated using libNeuroML v%s"%__version__
    nml_doc.networks.append(net)
    
    for cell_comp in set([exc_group_component, inh_group_component]): # removes duplicates
        nml_doc.includes.append(IncludeType(href='%s.cell.nml'%cell_comp))

    # The names of the Exc & Inh groups/populations 
    exc_group = "Exc" 
    inh_group = "Inh" 

    # The names of the network connections 
    net_conn_exc_inh = "NetConn_Exc_Inh"
    net_conn_inh_exc = "NetConn_Inh_Exc"
    net_conn_exc_exc = "NetConn_Exc_Exc"
    net_conn_inh_inh = "NetConn_Inh_Inh"

    # The names of the synapse types (should match names at Cell Mechanism/Network tabs in neuroConstruct)
    exc_inh_syn = "AMPAR"
    inh_exc_syn = "GABAA"
    exc_exc_syn = "AMPAR"
    inh_inh_syn = "GABAA"

    for syn in [exc_inh_syn, inh_exc_syn]:
        nml_doc.includes.append(IncludeType(href='%s.synapse.nml'%syn))


    # Generate excitatory cells 
    
    for layer in range(num_layers):

        y_offset = -1 * layer * layer_y_size
        exc_pop = Population(id="%s_%i"%(exc_group, layer), component=exc_group_component, type="populationList", size=numCells_exc_per_layer)
        net.populations.append(exc_pop)

        for i in range(0, numCells_exc_per_layer) :
                index = i
                inst = Instance(id=index)
                exc_pop.instances.append(inst)
                inst.location = Location(x=str(x_size*random()), y=str(y_offset - layer_y_size*random()), z=str(z_size*random()))

        if numCells_inh_per_layer > 0:
            # Generate inhibitory cells
            inh_pop = Population(id="%s_%i"%(inh_group, layer), component=inh_group_component, type="populationList", size=numCells_inh_per_layer)
            net.populations.append(inh_pop)

            for i in range(0, numCells_inh_per_layer):
                    index = i
                    inst = Instance(id=index)
                    inh_pop.instances.append(inst)
                    inst.location = Location(x=str(x_size*random()), y=str(y_offset - layer_y_size*random()), z=str(z_size*random()))

    if connections:
        
        W = getW('mouse somatic M1')

        for pre in range(num_layers):
            for post in range(num_layers):
                
                id = "proj_%s_%s"%(pre, post)
                pre_pop = "%s_%i"%(exc_group, pre)
                post_pop = "%s_%i"%(exc_group, post)
                proj = Projection(id=id, presynaptic_population=pre_pop, postsynaptic_population=post_pop, synapse=exc_exc_syn)
                net.projections.append(proj)

                count = 0
                
                prob = W[pre][post]
                print("Connecting layer %s to layer %s with probability %s"%(pre, post, prob))

                for i in range(0, numCells_exc_per_layer):
                    for j in range(0, numCells_exc_per_layer):
                        if i != j:

                            if random() < prob:

                                add_connection(proj, count, pre_pop, exc_group_component, i, 0, post_pop, exc_group_component, j, 0)
                                count+=1



    if inputs:
        
        mf_input_syn = "AMPAR"
        if mf_input_syn!=exc_inh_syn and mf_input_syn!=inh_exc_syn:
            nml_doc.includes.append(IncludeType(href='%s.synapse.nml'%mf_input_syn))
        
        rand_spiker_id = "input_%sHz"%input_firing_rate
        
        pfs = PoissonFiringSynapse(id=rand_spiker_id,
                                   average_rate="%s per_s"%input_firing_rate,
                                   synapse=mf_input_syn,
                                   spike_target="./%s"%mf_input_syn)
                                   
        nml_doc.poisson_firing_synapses.append(pfs)
        
        input_list = InputList(id="Input_0",
                             component=rand_spiker_id,
                             populations=exc_group)
                             
        count = 0
        for i in range(0, numCells_exc_per_layer):
            
            for j in range(num_inputs_per_exc):
                input = Input(id=count, 
                              target="../%s/%i/%s"%(exc_group, i, exc_group_component), 
                              destination="synapses")  
                input_list.input.append(input)
            
            count += 1
                             
        net.input_lists.append(input_list)


    #######   Write to file  ######    

    print("Saving to file...")
    nml_file = network_id+'.net.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file)

    print("Written network file to: "+nml_file)


    if validate:

        ###### Validate the NeuroML ######    

        from neuroml.utils import validate_neuroml2
        validate_neuroml2(nml_file) 
        
    if generate_lems_simulation:
        # Create a LEMSSimulation to manage creation of LEMS file
        
        ls = LEMSSimulation("Sim_%s"%network_id, duration, dt)

        # Point to network as target of simulation
        ls.assign_simulation_target(net.id)
        
        # Include generated/existing NeuroML2 files
        ls.include_neuroml2_file('%s.cell.nml'%exc_group_component)
        ls.include_neuroml2_file('%s.cell.nml'%inh_group_component)
        ls.include_neuroml2_file(nml_file)
        

        # Specify Displays and Output Files
        disp_exc = "display_exc"
        ls.create_display(disp_exc, "Voltages Exc cells", "-80", "50")

        of_exc = 'Volts_file_exc'
        ls.create_output_file(of_exc, "v_exc.dat")
        
        disp_inh = "display_inh"
        ls.create_display(disp_inh, "Voltages Inh cells", "-80", "50")

        of_inh = 'Volts_file_inh'
        ls.create_output_file(of_inh, "v_inh.dat")

        for i in range(numCells_exc_per_layer):
            quantity = "%s_0/%i/%s/v"%(exc_group, i, exc_group_component)
            ls.add_line_to_display(disp_exc, "Exc %i: Vm"%i, quantity, "1mV", pynml.get_next_hex_color())
            ls.add_column_to_output_file(of_exc, "v_%i"%i, quantity)
            
        for i in range(numCells_inh_per_layer):
            quantity = "%s_0/%i/%s/v"%(inh_group, i, inh_group_component)
            ls.add_line_to_display(disp_inh, "Inh %i: Vm"%i, quantity, "1mV", pynml.get_next_hex_color())
            ls.add_column_to_output_file(of_inh, "v_%i"%i, quantity)

        # Save to LEMS XML file
        lems_file_name = ls.save_to_file()
        
    print "-----------------------------------"


    
if __name__ == "__main__":
    
    
    generate_layered_network("LayeredCortexDemo",
                                numCells_exc_per_layer = 20,
                                numCells_inh_per_layer = 0,
                                num_layers = 9,
                                exc_group_component = "HHCell",
                                inh_group_component = "HHCell",
                                x_size = 400,
                                layer_y_size = 100, 
                                z_size = 400,
                                connections = True,
                                connection_probability_exc_exc =   0.4,
                                connection_probability_inh_exc =   0.7,
                                connection_probability_exc_inh =   0.7,
                                connection_probability_inh_inh =   0.1,
                                inputs = False,
                                input_firing_rate = 70, # Hz
                                num_inputs_per_exc = 2,
                                generate_lems_simulation = True,
                                duration = 300 )
                                


                                     







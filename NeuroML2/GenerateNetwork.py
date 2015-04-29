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


def generate_example_network(network_id,
                             numCells_exc,
                             numCells_inh,
                             x_size = 1000,
                             y_size = 100, 
                             z_size = 1000,
                             exc_group_component = "SimpleIaF",
                             inh_group_component = "SimpleIaF",
                             validate = True,
                             random_seed = 1234,
                             generate_lems_simulation = False,
                             connections = True,
                             connection_probability_exc_inh =   0.02,
                             connection_probability_inh_exc =   0.02,
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
    

    nml_doc.includes.append(IncludeType(href='%s.cell.nml'%exc_group_component))
    nml_doc.includes.append(IncludeType(href='%s.cell.nml'%inh_group_component))

    # The names of the Exc & Inh groups/populations 
    exc_group = "Exc" 
    inh_group = "Inh" 

    # The names of the network connections 
    net_conn_exc_inh = "NetConn_Exc_Inh"
    net_conn_inh_exc = "NetConn_Inh_Exc"

    # The names of the synapse types (should match names at Cell Mechanism/Network tabs in neuroConstruct)
    exc_inh_syn = "AMPAR"
    inh_exc_syn = "GABAA"

    for syn in [exc_inh_syn, inh_exc_syn]:
        nml_doc.includes.append(IncludeType(href='%s.synapse.nml'%syn))


    # Generate excitatory cells 

    exc_pop = Population(id=exc_group, component=exc_group_component, type="populationList", size=numCells_exc)
    net.populations.append(exc_pop)

    for i in range(0, numCells_exc) :
            index = i
            inst = Instance(id=index)
            exc_pop.instances.append(inst)
            inst.location = Location(x=str(x_size*random()), y=str(y_size*random()), z=str(z_size*random()))

    # Generate inhibitory cells
    inh_pop = Population(id=inh_group, component=inh_group_component, type="populationList", size=numCells_inh)
    net.populations.append(inh_pop)

    for i in range(0, numCells_inh) :
            index = i
            inst = Instance(id=index)
            inh_pop.instances.append(inst)
            inst.location = Location(x=str(x_size*random()), y=str(y_size*random()), z=str(z_size*random()))

    if connections:

        proj_exc_inh = Projection(id=net_conn_exc_inh, presynaptic_population=exc_group, postsynaptic_population=inh_group, synapse=exc_inh_syn)
        net.projections.append(proj_exc_inh)
        proj_inh_exc = Projection(id=net_conn_inh_exc, presynaptic_population=inh_group, postsynaptic_population=exc_group, synapse=inh_exc_syn)
        net.projections.append(proj_inh_exc)

        count_exc_inh = 0
        count_inh_exc = 0

        # Generate exc -> *  connections


        def add_connection(projection, id, pre_pop, pre_component, pre_cell_id, pre_seg_id, post_pop, post_component, post_cell_id, post_seg_id):

            connection = Connection(id=id, \
                                    pre_cell_id="../%s/%i/%s"%(pre_pop, pre_cell_id, pre_component), \
                                    pre_segment_id=pre_seg_id, \
                                    pre_fraction_along=0.5,
                                    post_cell_id="../%s/%i/%s"%(post_pop, post_cell_id, post_component), \
                                    post_segment_id=post_seg_id,
                                    post_fraction_along=0.5)

            projection.connections.append(connection)


        for i in range(0, numCells_exc):
            for j in range(0, numCells_inh):
                if i != j:
                    if random()<connection_probability_exc_inh:

                            add_connection(proj_exc_inh, count_exc_inh, exc_group, exc_group_component, i, 0, inh_group, inh_group_component, j, 0)
                    count_exc_inh+=1

                    if random()<connection_probability_inh_exc:

                            add_connection(proj_inh_exc, count_inh_exc, inh_group, inh_group_component, j, 0, exc_group, exc_group_component, i, 0)
                    count_inh_exc+=1

    if inputs:
        
        mf_input_syn = "AMPAR"
        nml_doc.includes.append(IncludeType(href='%s.synapse.nml'%mf_input_syn))
        
        rand_spiker_id = "input50Hz"
        
        
        #<poissonFiringSynapse id="Input_8" averageRate="50.0 per_s" synapse="MFSpikeSyn" spikeTarget="./MFSpikeSyn"/>
        pfs = PoissonFiringSynapse(id="input50Hz",
                                   average_rate="%s per_s"%input_firing_rate,
                                   synapse=mf_input_syn,
                                   spike_target="./%s"%mf_input_syn)
                                   
        nml_doc.poisson_firing_synapses.append(pfs)
        
        input_list = InputList(id="Input_0",
                             component=rand_spiker_id,
                             populations=exc_group)
                             
        count = 0
        for i in range(0, numCells_exc):
            
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
        ls.create_display(disp_exc, "Voltages Exc cells", "-95", "-38")

        of_exc = 'Volts_file_exc'
        ls.create_output_file(of_exc, "v_exc.dat")
        
        disp_inh = "display_inh"
        ls.create_display(disp_inh, "Voltages Inh cells", "-95", "-38")

        of_inh = 'Volts_file_inh'
        ls.create_output_file(of_inh, "v_inh.dat")

        for i in range(numCells_exc):
            quantity = "%s/%i/%s/v"%(exc_group, i, exc_group_component)
            ls.add_line_to_display(disp_exc, "Exc %i: Vm"%i, quantity, "1mV", pynml.get_next_hex_color())
            ls.add_column_to_output_file(of_exc, "v_%i"%i, quantity)
            
        for i in range(numCells_inh):
            quantity = "%s/%i/%s/v"%(inh_group, i, inh_group_component)
            ls.add_line_to_display(disp_inh, "Inh %i: Vm"%i, quantity, "1mV", pynml.get_next_hex_color())
            ls.add_column_to_output_file(of_inh, "v_%i"%i, quantity)

        # Save to LEMS XML file
        lems_file_name = ls.save_to_file()
        
    print "-----------------------------------"


    
if __name__ == "__main__":
    
    
    generate_example_network("CortexDemo",
                                numCells_exc = 40,
                                numCells_inh = 20,
                                x_size = 1000,
                                y_size = 100, 
                                z_size = 1000,
                                connections = True,
                                connection_probability_exc_inh =   0.5,
                                connection_probability_inh_exc =   0.5,
                                inputs = True,
                                input_firing_rate = 80, # Hz
                                num_inputs_per_exc = 5,
                                generate_lems_simulation = True)
                                


                                     







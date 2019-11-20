
from neuromllite import Network, Cell, InputSource, Population, Synapse
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id='PopExample')
net.notes = 'Testing...'

net.seed = 1234

net.parameters = { 'N': 10, 'fractionE': 0.8, 'weightInput': 1, 'Wei':0.01, 'Wie':0.01}


cell = Cell(id='iafcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":0}
net.cells.append(cell)


input_source = InputSource(id='poissonFiringSyn100Hz', neuroml2_source_file='inputs.nml')
net.input_sources.append(input_source)

                           
net.input_sources.append(input_source)


pE = Population(id='Epop', size='int(N*fractionE)', component=cell.id, properties={'color':'.7 0 0'})
pI = Population(id='Ipop', size='N - int(N*fractionE)', component=cell.id, properties={'color':'0 0 .7'})

net.populations.append(pE)
net.populations.append(pI)

net.synapses.append(Synapse(id='ampaSyn', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-10, 'tau_syn':2}))
                            
net.synapses.append(Synapse(id='gabaSyn', 
                            pynn_receptor_type='inhibitory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-80, 'tau_syn':10}))
                            
                            
net.projections.append(Projection(id='projEI',
                                  presynaptic=pE.id, 
                                  postsynaptic=pI.id,
                                  synapse='ampaSyn',
                                  delay=1,
                                  weight='Wei',
                                  random_connectivity=RandomConnectivity(probability=.8)))
                                  
net.projections.append(Projection(id='projIE',
                                  presynaptic=pI.id, 
                                  postsynaptic=pE.id,
                                  synapse='gabaSyn',
                                  delay=1,
                                  weight='Wie',
                                  random_connectivity=RandomConnectivity(probability=.8)))
                            
                            
net.inputs.append(Input(id='stim',
                        input_source=input_source.id,
                        population=pE.id,
                        percentage=100,
                        weight='weightInput'))

print(net)
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='Sim%s'%net.id,
                 network=new_file,
                 duration='1000',
                 seed='1111',
                 dt='0.025',
                 recordTraces={'all':'*'},
                 recordSpikes={'all':'*'})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)

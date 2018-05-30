from neuromllite import Network, Cell, InputSource, Population, Synapse,RectangularRegion,RandomLayout
from neuromllite import Projection, RandomConnectivity, Input, Simulation
from neuromllite.NetworkGenerator import generate_and_run
from neuromllite.NetworkGenerator import generate_neuroml2_from_network
import sys

################################################################################
###   Build new network

net = Network(id='Rates')
net.notes = 'Testing...'

net.parameters = { 'input':10 }

ecell = Cell(id='Ecomp', lems_source_file='SimpleExamples.xml')
icell = Cell(id='Icomp', lems_source_file='SimpleExamples.xml')


net.cells.append(ecell)
net.cells.append(icell)


input_source0 = InputSource(id='iclamp0', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':8, 'start':50., 'stop':150.})
                           
net.input_sources.append(input_source0)

r1 = RectangularRegion(id='network', x=0,y=0,z=0,width=100,height=100,depth=10)
net.regions.append(r1)

colors = [[8,48,107],         # dark-blue
          [228,26,28]]
    
color_str = {}
for i in range(len(colors)):
    color_str[i] = ''
    for c in colors[i]:
        color_str[i]+='%s '%(c/255.)
    color_str[i] = color_str[i][:-1]

pE = Population(id='Exc', size=1, component=ecell.id, properties={'color':color_str[0]},random_layout = RandomLayout(region=r1.id))
pI = Population(id='Inh', size=1, component=icell.id, properties={'color':color_str[1]},random_layout = RandomLayout(region=r1.id))

net.populations.append(pE)
net.populations.append(pI)

pops = [pE,pI]


net.synapses.append(Synapse(id='ampa', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-10, 'tau_syn':2}))
                            
net.synapses.append(Synapse(id='gaba', 
                            pynn_receptor_type='inhibitory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-80, 'tau_syn':10}))

W = [[2.4167,   -0.3329],
    [2.9706,   -3.4554]]
    
for pre in pops:
    for post in pops:
        
        weight = W[pops.index(post)][pops.index(pre)]
        print('Connection %s -> %s weight %s'%(pre.id, post.id, weight))
        if weight!=0:
            
            net.projections.append(Projection(id='proj_%s_%s'%(pre.id,post.id),
                                              presynaptic=pre.id, 
                                              postsynaptic=post.id,
                                              synapse='ampa',
                                              delay=0,
                                              weight=weight))
                               
                        
net.inputs.append(Input(id='modulation',
                        input_source=input_source0.id,
                        population=pE.id,
                        percentage=100))

print(net)
print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='Sim%s'%net.id,
                 network=new_file,
                 duration='200',
                 dt='0.025',
                 recordRates={'all':'*'})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)


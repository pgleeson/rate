from neuromllite import *

import random

################################################################################
###   Build a new network

net = Network(id='net0')
net.notes = "...."

cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":.1 }
net.cells.append(cell)

net.synapses.append(Synapse(id='ampa', 
                            pynn_receptor_type='excitatory', 
                            pynn_synapse_type='cond_alpha', 
                            parameters={'e_rev':-10, 'tau_syn':2}))
                            

vis = RectangularRegion(id='VIS', x=0,y=0,z=0,width=100,height=100,depth=100)
net.regions.append(vis)
oth = RectangularRegion(id='OTHER', x=120,y=120,z=0,width=200,height=200,depth=100)
net.regions.append(oth)

f = open('Neuron_2015_Table.csv')
all_tgts = []

for l in f:
    #print l
    w = l.split(',')
    tgt = w[0]
    src = w[1]
    if tgt!='TARGET':
        if not tgt in all_tgts:
            all_tgts.append(tgt)
        
print all_tgts
print(len(all_tgts))

f = open('Neuron_2015_Table.csv')
pop_ids = []
used_ids = {}


for l in f:
    #print l
    w = l.split(',')
    tgt = w[0]
    src = w[1]
    if tgt!='TARGET' and src in all_tgts:
        fln = float(w[2])
        print('Adding conn from %s to %s with FLN: %s'%(src,tgt,fln))
        for pop_id in [tgt,src]:
            if not pop_id in pop_ids:
                
                repl = pop_id.replace('/','_')
                
                used_ids[pop_id] = '_%s'%repl if repl[0].isdigit() else repl
                
                region = vis if 'v' in pop_id.lower() else oth
                p0 = Population(id=used_ids[pop_id], 
                                size=1, 
                                component=cell.id, 
                                properties={'color':'%s %s %s'%(random.random(),random.random(),random.random()),
                                            'radius':10},
                                random_layout = RandomLayout(region=region.id))

                net.populations.append(p0)
                pop_ids.append(pop_id)


        ################################################################################
        ###   Add a projection

        if fln>0.0:
            net.projections.append(Projection(id='proj_%s_%s'%(used_ids[src],used_ids[tgt]),
                                              presynaptic=used_ids[src], 
                                              postsynaptic=used_ids[tgt],
                                              synapse='ampa',
                                              weight=fln,
                                              random_connectivity=RandomConnectivity(probability=1)))




print(net)
net.id = 'TestNetwork'

print(net.to_json())
new_file = net.to_json_file('Example1_%s.json'%net.id)

sim = Simulation(id='SimExample',
                 network=new_file,
                 duration='100',
                 dt='0.025',
                 recordTraces={'all':'*'})


################################################################################
###   Export to some formats
###   Try:
###        python Example1.py -graph2

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite import Simulation
import sys

check_to_generate_or_run(sys.argv, sim)


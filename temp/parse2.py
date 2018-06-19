from neuromllite import *

import random

colors = {}
centres = {}
pop_ids = []
used_ids = {}

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

f = open('ABA12.tsv')
for l in f:
    w = l.split()
    print w
    id = w[0].replace('-','_').replace('/','_')
    if id != '[0]':
        colors[id] = w[1]
        scale = 100
        centres[id] = (float(w[2])*scale,float(w[3])*scale,float(w[4])*scale)


        repl = id

        p = centres[repl]
        used_ids[id] = '_%s'%repl if repl[0].isdigit() else repl

        r = RectangularRegion(id='Region_%s'%used_ids[id], x=p[0],y=p[1],z=p[2],width=1,height=1,depth=1)
        net.regions.append(r)

        p0 = Population(id=used_ids[id], 
                        size=1, 
                        component=cell.id, 
                        properties={'color':'%s %s %s'%(random.random(),random.random(),random.random()),
                                    'radius':100},
                        random_layout = RandomLayout(region=r.id))

        net.populations.append(p0)
        pop_ids.append(id)

print centres.keys()
    
                            


f = open('retrograde-directed-weighted-connectivity_matrix-figure2.csv')
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

f = open('retrograde-directed-weighted-connectivity_matrix-figure2.csv')

'''
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
                
                p = centres[repl]
                used_ids[pop_id] = '_%s'%repl if repl[0].isdigit() else repl
                
                r = RectangularRegion(id='Region_%s'%used_ids[pop_id], x=p[0],y=p[1],z=p[2],width=1,height=1,depth=1)
                net.regions.append(r)

                p0 = Population(id=used_ids[pop_id], 
                                size=1, 
                                component=cell.id, 
                                properties={'color':'%s %s %s'%(random.random(),random.random(),random.random()),
                                            'radius':1000},
                                random_layout = RandomLayout(region=r.id))

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


'''

print(net)
net.id = 'Mouse'

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


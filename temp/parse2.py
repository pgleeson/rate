from neuromllite import *

import random
import opencortex.utils.color as occ

colors = {}
centres = {}
pop_ids = []
used_ids = {}
names = {}
areas = {}

import csv
with open('nature13186-s2_1.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for w in reader:
        print w
        if w[0] != 'id':
            short = w[3].replace(', ','_')
            name = w[4].strip('"')
            names[short]=name
            
with open('nature13186-s2_2.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for w in reader:
        print w
        if w[0] != 'ID':
            short = w[2].replace(', ','_')
            area = w[4].strip('"')
            areas[short]=area
      
for n in names: print('%s: \t%s'%(n,names[n]))
for a in areas: print('%s: \t%s'%(a,areas[a]))
#exit()

################################################################################
###   Build a new network

net = Network(id='net0')
net.notes = "NOTE: this is only a quick demo!! Do not use it for your research assuming an accurate conversion of the source data!!! "

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
    pre_id = w[0].replace('-','_').replace('/','_')
    if pre_id != '[0]' :
        
        scale = 100
        x0 = float(w[2])*scale
        all = [ (pre_id, x0), ('%s_CONTRA'%pre_id, x0*-1)]
        all = [ (pre_id, x0)]
        
        for a in all:
            id = a[0]
            x = a[1]
            centres[id] = (x,float(w[3])*scale,float(w[4])*scale)
            colors[id] = w[1]

            repl = id
            name = names[w[0]]
            short_name3 = w[0][:3]
            short_name4 = w[0][:4]
            short_name5 = w[0][:5]
            short_name6 = w[0][:6]
            short_name7 = w[0][:7]
            
            if w[0] in areas:
                area = areas[w[0]]  
            elif short_name7 in areas:
                   area = areas[short_name7]  
            elif short_name6 in areas:
                   area = areas[short_name6]  
            elif short_name5 in areas:
                   area = areas[short_name5]  
            elif short_name4 in areas:
                   area = areas[short_name4]  
            elif short_name3 in areas:
                   area = areas[short_name3]  
            else:
                area = '???'

            p = centres[repl]
            used_ids[id] = '_%s'%repl if repl[0].isdigit() else repl

            region_name = name.split(',')[0].replace(' ','_')
            region_name = used_ids[id]
            r = RectangularRegion(id=region_name, x=p[0],y=p[1],z=p[2],width=1,height=1,depth=1)
            net.regions.append(r)


            color = '.8 .8 .8'
            if 'Thalamus' in area:
                color = occ.THALAMUS_2
            if 'Isocortex' in area:
                color = occ.L23_PRINCIPAL_CELL
            if 'Olfactory' in area:
                color = occ.L4_PRINCIPAL_CELL
            if 'Cerebe' in area:
                color = occ.L5_PRINCIPAL_CELL
            if 'Hippocampal' in area:
                color = occ.L6_PRINCIPAL_CELL
            '''
            if '1' in id:
                color = occ.THALAMUS_2
            if '2_3' in id:
                color = occ.L23_PRINCIPAL_CELL
            if '4' in id:
                color = occ.L4_PRINCIPAL_CELL
            if '5' in id:
                color = occ.L5_PRINCIPAL_CELL
            if '6' in id:
                color = occ.L6_PRINCIPAL_CELL'''
                
                
            
            p0 = Population(id=used_ids[id], 
                            size=1, 
                            component=cell.id, 
                            properties={'color':'%s'%(color),
                                        'radius':15,
                                        'name':name,
                                        'area':area},
                            random_layout = RandomLayout(region=r.id))

            net.populations.append(p0)
            pop_ids.append(id)

print centres.keys()
    
                            

with open('nature13186-s4_W_ipsi.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    indices = {}
    for w in reader:
        #print w
        if w[0]=='ROOT':
            for i in range(len(w)):
                indices[i]=w[i]
            print indices
        else:
            pre = w[0]
            for i in range(len(w)):
                if i!=0:
                    weight = float(w[i])
                    if weight>0:
                        post = indices[i]
                        print('Connection %s -> %s of %s'%(pre, post, weight))
            
                        if weight>0.05:

                            if pre in used_ids and post in used_ids:
                                print('Adding conn from %s -> %s of %s'%(pre, post, weight))


                                ################################################################################
                                ###   Add a projection

                                net.projections.append(Projection(id='proj_%s_%s'%(used_ids[pre],used_ids[post]),
                                                                  presynaptic=used_ids[pre], 
                                                                  postsynaptic=used_ids[post],
                                                                  synapse='ampa',
                                                                  weight=weight,
                                                                  random_connectivity=RandomConnectivity(probability=1)))




print(net)
net.id = 'MouseConns'

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


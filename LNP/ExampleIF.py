from neuromllite import Network, Cell, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, OneToOneConnector, Simulation

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.sweep.ParameterSweep import *

import sys


def generate():
    
    dt = 0.025
    simtime = 1000
    
    ################################################################################
    ###   Build new network

    net = Network(id='ExampleIF')
    net.notes = 'Example with IF'
    

    net.parameters = { 'tauMem':  20.0,
                       'tauSyn':  0.1,
                       'tauRef':  2,
                       'V0':      -70,
                       'theta':   -50.0,
                       'scale':   1,
                       'in_weight': 0.01,
                       'in_rate': 50}

    ifcell = Cell(id='ifcell', pynn_cell='IF_curr_alpha')


    ifcell.parameters = { 'tau_m':       'tauMem', 
                        'tau_refrac':  'tauRef',
                        'v_rest':      'V0',
                        'v_reset':     'V0',
                        'v_thresh':    'theta',
                        'cm':          0.001,
                        "i_offset":    0}

    net.cells.append(ifcell)

    poisson_input = Cell(id='poisson_input', pynn_cell='SpikeSourcePoisson')
    poisson_input.parameters = { 'rate':       'in_rate',
                             'start':      0,
                             'duration':   1e9}
    net.cells.append(poisson_input)

    r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(r1)

    pIF = Population(id='IFpop', 
                    size='1*scale', 
                    component=ifcell.id, 
                    properties={'color':'.9 0 0', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pIF)

    pLNP = Population(id='LNPpop', 
                    size='1*scale', 
                    component=ifcell.id, 
                    properties={'color':'.9 0.9 0', 'radius':5},
                    random_layout = RandomLayout(region=r1.id))
    net.populations.append(pLNP)
                    
    pEpoisson = Population(id='expoisson', 
                           size='10', 
                           component=poisson_input.id, 
                           properties={'color':'0.9 0.7 0.7', 'radius':3},
                           random_layout = RandomLayout(region=r1.id))

    net.populations.append(pEpoisson)


    net.synapses.append(Synapse(id='ampa', 
                                pynn_receptor_type='excitatory', 
                                pynn_synapse_type='curr_alpha', 
                                parameters={'tau_syn':0.1}))
                                
    
    net.projections.append(Projection(id='proj0',
                                      presynaptic=pEpoisson.id, 
                                      postsynaptic=pIF.id,
                                      synapse='ampa',
                                      delay=0,
                                      weight='in_weight',
                                      random_connectivity=RandomConnectivity(probability=0.7)))
    
    net.projections.append(Projection(id='proj1',
                                      presynaptic=pEpoisson.id, 
                                      postsynaptic=pLNP.id,
                                      synapse='ampa',
                                      delay=0,
                                      weight='in_weight',
                                      random_connectivity=RandomConnectivity(probability=0.7)))
    
    

    #print(net)
    #print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)


    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='SimExampleIF',
                     network=new_file,
                     duration=simtime,
                     dt=dt,
                     seed= 123,
                     recordTraces={pIF.id:'*'},
                     recordSpikes={'all':'*'})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":

    if '-sweep' in sys.argv:
        
        sim, net = generate()
        sim.recordTraces={}
        
        fixed = {'dt':0.025, 'order':5}
 
        vary = {'eta':[0.5,1,1.5,2,3,4,5,6,7,8,9,10]}
        #vary = {'eta':[1,2,5]}
        vary['seed'] = [i for i in range(10)]
        vary['seed'] = [i for i in range(5)]

        simulator = 'jNeuroML'
        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML_NEURON'
        simulator = 'jNeuroML'

        nmllr = NeuroMLliteRunner('SimExample7.json',
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=16,
                            plot_all=False, 
                            heatmap_all=False,
                            show_plot_already=False,
                            peak_threshold=0)

        report = ps.run()
        ps.print_report()

        #  ps.plotLines('weightInput','average_last_1percent',save_figure_to='average_last_1percent.png')
        #ps.plotLines('weightInput','mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        #ps.plotLines('eta','Einput[0]/spike:mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        ps.plotLines('eta','expoisson/0/poisson_input/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_ein.png')
        ps.plotLines('eta','inpoisson/0/poisson_input/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_iin.png')
        ps.plotLines('eta','Epop/0/ifcell/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_e.png')
        ps.plotLines('eta','Ipop/0/ifcell/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency_i.png')

        import matplotlib.pyplot as plt

        plt.show()
        
    if '-sweep2' in sys.argv:
        
        sim, net = generate()
        sim.recordTraces={}
        
        fixed = {'dt':0.025, 'order':5}
 
        vary = {'eta':[0.5,1,1.5,2,3]}
        vary = {'epsilon':[0.01,0.1,0.2,0.5,0.9]}
        vary = {'J':[0.01,0.1,0.2,0.5,0.9]}
        #vary = {'g':[0.5,1,1.5,2,3,20]}
        
        first = vary.keys()[0]
        
        #vary = {'eta':[1,2,5]}
        #vary['seed'] = [i for i in range(10)]
        vary['seed'] = [i for i in range(3)]

        simulator = 'jNeuroML'
        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML'
        simulator = 'jNeuroML_NEURON'

        nmllr = NeuroMLliteRunner('SimExample7.json',
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=16,
                            plot_all=False, 
                            heatmap_all=False,
                            show_plot_already=False,
                            peak_threshold=0)

        report = ps.run()
        ps.print_report()

        #  ps.plotLines('weightInput','average_last_1percent',save_figure_to='average_last_1percent.png')
        #ps.plotLines('weightInput','mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        #ps.plotLines('eta','Einput[0]/spike:mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        
        second = 'seed'
        ps.plotLines(first,'expoisson/0/poisson_input/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_ein.png')
        ps.plotLines(first,'inpoisson/0/poisson_input/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_iin.png')
        ps.plotLines(first,'Epop/0/ifcell/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_e.png')
        ps.plotLines(first,'Ipop/0/ifcell/spike:mean_spike_frequency',second_param=second,save_figure_to='mean_spike_frequency_i.png')

        import matplotlib.pyplot as plt

        plt.show()
    
    else:

        sim, net = generate()

        ################################################################################
        ###   Run in some simulators

        import sys

        check_to_generate_or_run(sys.argv, sim)


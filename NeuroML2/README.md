
**Some console commands for running simulations of this model in OSB 3D Explorer**

See [here](http://localhost:3000/projects/weileretal08-laminarcortex?explorer=https%3A%2F%2Fraw.githubusercontent.com%2FOpenSourceBrain%2FWeilerEtAl08-LaminarCortex%2Fmaster%2FNeuroML2%2FCortexDemoHH.net.nml)

CortexDemoHH.Exc_1.electrical.getSimulationTree();
CortexDemoHH.Exc_2.electrical.getSimulationTree();
CortexDemoHH.Exc_6.electrical.getSimulationTree();

CortexDemoHH.Exc_1.electrical.SimulationTree.HHCell[0].v.setWatched(true);
CortexDemoHH.Exc_2.electrical.SimulationTree.HHCell[0].v.setWatched(true);
CortexDemoHH.Exc_6.electrical.SimulationTree.HHCell[0].v.setWatched(true);

Project.getActiveExperiment().simulatorConfigurations['CortexDemoHH.electrical'].setTimeStep('0.00005');
Project.getActiveExperiment().simulatorConfigurations['CortexDemoHH.electrical'].setLength('0.5');


G.addWidget(0);
Plot1.setName("Membrane potentials");
Plot1.plotData(CortexDemoHH.Exc_1.electrical.SimulationTree.HHCell[0].v);
Plot1.plotData(CortexDemoHH.Exc_2.electrical.SimulationTree.HHCell[0].v);
Plot1.plotData(CortexDemoHH.Exc_6.electrical.SimulationTree.HHCell[0].v);


G.addBrightnessFunction(CortexDemoHH.Exc_1.electrical, CortexDemoHH.Exc_1.electrical.SimulationTree.HHCell[0].v, function(x){return (x+0.06)/0.01;});
G.addBrightnessFunction(CortexDemoHH.Exc_2.electrical, CortexDemoHH.Exc_2.electrical.SimulationTree.HHCell[0].v, function(x){return (x+0.06)/0.01;});
G.addBrightnessFunction(CortexDemoHH.Exc_6.electrical, CortexDemoHH.Exc_6.electrical.SimulationTree.HHCell[0].v, function(x){return (x+0.06)/0.01;});

Project.getActiveExperiment().play({playAll:true})

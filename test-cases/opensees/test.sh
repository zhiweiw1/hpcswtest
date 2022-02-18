cd DeveloperTestScripts
OpenSees runAll.tcl
cd ..
cd SmallMP
mpirun -n 2 OpenSeesMP Example.tcl

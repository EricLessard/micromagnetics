# micromagnetics
Repository for Micromagnetics code utilizing magnum.fd 
Requires installation of magnum.fd python package. See links at the end of the readme for installation instructions.

runSolver.py
  Builds rectangular world mesh comrised of two bodies (Box, UnitCube). Calculates stray magnetic field from magnetization in UnitCube and calculates the sum of the stray field inside the Box. 
  TODO: Get working to determine magnetization in UnitCube which maximizes the Z component of the stray magnetic field in Box
  
getObjects.py
  Runs dir() on a variety of magnum.fd objects to better understand what can be done with various components of magnum.fd
  
miscMagnumTests.py
  Builds rectangular world mesh comprised of two bodies (Box, UnitCube). Calculates stray magnetic field, saves to .omf, reads from .omf, calculates an "objective function", implements the magnum.fd built in solver, saves to .omf. These can be used to explore the affect of solver.

Information for Magnum.FD can be found:
http://micromagnetics.org/magnum.fd/index.html
https://github.com/micromagnetics/magnum.fd



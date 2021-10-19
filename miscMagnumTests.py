##########################################################################################
# A script to recreate the validation and benchmarking example from 
# A Fast Finite-Difference Algorithm for Topology Optimization of Permamnent Magnets
# arXiv:1707.0989v1 [physics.comp-ph] 31 Jul 2017
# Section 4
# Maximimzation of z - component stray magnetic field in a small box along a unit cube w/ 
# M0 = (0,0,1) that is considered for topology optimization
# 
# The script doesn't accomplish it's goal but has a few tests to troubleshoot magnum.fd
# Eric Lessard 2021

#This script ended up being a test of calculating things
#based on H_stray, initially I saved and loaded it but then
#i found VectorField.get() which made that much easier

from magnum import *
from random import *
import numpy as np
import re

#Some intialization things
p = 3 #Initial
rho = 1
M_zero =(0,0,1)
L = 1.1e-9; #Total size of world environment
nPoints = 20 #Discritation points (isotropic)

#Create our world mesh
#RectangularMesh((nx, ny, nz), (StepX, StepY, StepZ))
#Mesh size = (nx*StepX, ny*StepY, Nz*StepZ)
#In SP4.py it is RectangularMesh((200,100,1), (2.5e-9, 1.25e-9, 3.0e-9)), ...)
#and Micromagnetics Standard Problem #4 is a film of 500nm x 125 nm x 3 nm
mesh = RectangularMesh((nPoints,nPoints,nPoints), (L/nPoints,L/nPoints,L/nPoints))

#Create the bodies within our world
UnitCube = Body("UnitCube", Material.Py(), Cuboid((1e-9, 1e-9, 1e-9), (0, 0, 0)))
Box = Body("Box", Material.Py(), Cuboid((0.6e-9,.6e-9,1.1e-9), (.4e-9, .4e-9,1.05e-9)))
#Cuboid(p1,p2) <-- P1 and P2 are diagonally opposite vertices
world = World(mesh,
	UnitCube, #Our unit cube
	Box #Our box on top
	)

#Create our solver
solver = create_solver(world, [StrayField], log=True)

#Initial M0
solver.state["UnitCube"].M = M_zero

#Save our H_stray and M files to be used
writeOMF("H_stray_initial.omf", solver.state.H_stray);
writeOMF("M_initial.omf", solver.state.M)

#Load the H_Stray information
data = np.loadtxt('H_stray_initial.omf', skiprows = 28)

#We also need the multiplication factor for the values contained in our numpy array
f = open('H_stray_initial.omf')
content = f.readlines()
factor = content[7]
temp = re.findall(r'\d+', factor)
factor = map(int, temp)
factor = factor[0]
#print(factor)

#Get an array of locations which comprise our box
boxIndices = map(int, Box.shape.getCellIndices(mesh))

#This function calculates the negative magnitude of the stray field over our box
#Inputs: data - a numpy loaded .omf file of H_stray values over our world
#		 boxIndices - a list of cells that our box comprises of
def calcObjectiveFunction(data, boxIndices, factor):
	H_stray = np.empty((0))
	for i in range(len(boxIndices)):
		H_stray = np.append(H_stray, (data[boxIndices[i],2]))
	objectiveFunction = -sum(H_stray*H_stray*factor*factor)/2
	return objectiveFunction
#Calculate the objective function
obj = calcObjectiveFunction(data, boxIndices, factor)

print(obj)

#state.M.to_numpy() converts to a [nPoints, nPoints, nPoints, 3] np.array
#So, cube with Mx, My, Mz values
M_np = solver.state.M.to_numpy()
print(M_np[1,10,10,2])

#p = 0,0,1
#a_j = -100000
#solver.setMacroSpinTorque("Box", p, a_j)
solver.solve(condition.Time(20e-9))

#Save our M and H_stray post modification
writeOMF("M_postrelax.omf", solver.state.M)
writeOMF("H_stray_final.omf", solver.state.H_stray);

#Load in data + factor for our post solved H_stray information
dataPost = np.loadtxt('H_stray_final.omf', skiprows = 28)
f2 = open('H_stray_final.omf')
content2 = f2.readlines()
factor2 = content2[7]
temp2 = re.findall(r'\d+', factor2)
factor2 = map(int, temp2)
factor2 = factor2[0]
#print(factor2)
#Calculate the new objective function
objPost = calcObjectiveFunction(dataPost, boxIndices, factor2)

print(objPost)
print(solver.state.M.get(1))
print(solver.state.H_stray.get(1))
print(solver.state.M.get(boxIndices[1]))


# for i in range(len(boxIndices)):
# 	A = solver.state.H_stray.get(boxIndices[i])
# 	A += A

# print(A)

# for i in boxIndices:
# 	B = solver.state.H_stray.get(i)
# 	B += B

# print(B)
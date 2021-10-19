from magnum import *
import numpy as np
from random import *
import magnum.magneto as magneto
import scipy as sp

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

#Anything that we change over a run gets done here
#I don't think we necessarily need a run() here as we aren't
#changing anything and iterating through, and I think all we
#need is a direct minimization for the functional derivative
#but it's here in case at the moment
def run(n):
	#THis is probably overly clunky but one thing at a time here		
	def calcObjectiveFunction(HStrayBox):
		H_stray = np.empty((0))
		for i in HStrayBox:
			H_stray =np.append(H_stray, i)
			objectiveFunction = -sum(H_stray*H_stray)/2
		return objectiveFunction
	#Define our magnetization topology... I think		
	def stateFunction(field, pos):
		Mx = 0
		My = 0
		Mz = random()
		return Mx, My, Mz

	print("Running with:", n)
	

	#Create our solver
	solver = create_solver(world, [StrayField], log=True)

	#Initial M0
	solver.state["UnitCube"].M = M_zero

	#Testing just a pure minimization
	#Essentially the problem is straight forward
	#there's a couple built in mimizations
	#magneto.llge -> Landau Lifshitz Gilbert Eq.
	#minimize() -> M2 = M - h * f * (M + M2)/2 ^ H(M)
	#f1, rho = Field(mesh), Field(mesh)
	#f1.fill(1) 
	#rho.fill(1) #rho_initial = 1
	#dJ = VectorField(mesh);
	#M = solver.state.M;
	#H = solver.state.H_stray;
	#dJ = p*(rho**(p-1))
	#check = magneto.llge(f1, rho, M, H, dJ)
	#print(check)


	#Get our box indices
	boxIndices = map(int, Box.shape.getCellIndices(mesh))

	#Get the H_Stray values inside our box
	for i in boxIndices:
		HStrayBox = solver.state.H_stray.get(i)
		HStrayBox += HStrayBox

	objectiveFunction = calcObjectiveFunction(HStrayBox)	
	print(objectiveFunction)


	return objectiveFunction

#Initialize an array where we store our obj function
#This isn't used at the moment,but was when I ran multiple
#iterations of run and saved them to the numpy array
F = np.empty((0))

#Mock parameter sweep
run(1)







#Quick script to gain insight into the different classes and such

from magnum import *

print("Solver = ", dir(Solver))
print("\n")
print("Solver.state =", dir(Solver.state))
print("\n")
print("World = ", dir(World))
print("\n")
print("VectorField = ", dir(VectorField))
print("\n")
print("VectorField.randomize = ", dir(VectorField.randomize))
print("\n")
print("Field = ", dir(Field))
print("\n")
print("Material = ", dir(Material))
print("\n")
print("Shape = ", dir(Shape))
print("\n")
print("Body = ", dir(Body))
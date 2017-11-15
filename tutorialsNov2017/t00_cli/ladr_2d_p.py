from proteus.default_p import *
from proteus.Domain import RectangularDomain
from adr import LAD

name = "ladr_2d"
nd = 2; #Two dimensions

domain = RectangularDomain(L=[1.0,1.0],
                           x=[0.0,0.0])

T=1.0

coefficients=LAD(M=1.0,
                 A=[[0.001,0.0],
                    [0.0,0.001]],
                 B=[2.0,1.0])

#set boundary conditions based on coordinates
test_eps = 1.0e-8
def on_inflow(x, flag):
    if x[0] < test_eps or x[1] < test_eps:
        return True
    else:
        return False

def on_outflow(x, flag):
    if (not  on_inflow and
        (x[0] > L[0] - test_eps or
         x[1] > L[1] - test_eps)):
        return True
    else:
        return False

#set boundary conditions based on flags
# def on_inflow(x, flag):
#     if flag in [domain.boundaryTags['left'],
#                 domain.boundaryTags['bottom']]:
#         return True
#     else:
#         return False

# def on_outflow(x, flag):
#     if flag in [domain.boundaryTags['right'],
#                 domain.boundaryTags['top']]:
#         return True

def getDirichletBC(x, flag):
    if on_inflow(x, flag):
        return lambda x,t: 1.0

def getNeumannBC_advective(x, flag):
    return None

def getNeumannBC_diffusive(x, flag):
    if on_outflow(x, flag):
        return lambda x,t: 0.0

dirichletConditions = {0:getDirichletBC}
advectiveFluxBoundaryConditions = {0:getNeumannBC_advective}
diffusiveFluxBoundaryConditions = {0:{0:getNeumannBC_diffusive}}

class IC:
    def __init__(self):
        pass
    def uOfXT(self,x,t):
        if x[0] <= 0.0 or x[1] <= 0.0:
            return 1.0
        else:
            return 0.0

initialConditions  = {0:IC()}

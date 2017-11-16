from proteus import Domain, Context, Comm
from proteus.mprans import SpatialTools as st
from proteus import WaveTools as wt
from proteus.Profiling import logEvent
from proteus.mbd import ChRigidBody as crb
from math import *
import numpy as np


opts=Context.Options([
    # predefined test cases
    ("water_level", 1.5, "Height of free surface above bottom"),
    # tank
    ("tank_dim", (3.137*2, 3.,), "Dimensions of the tank"),
    ("tank_sponge", (3.137, 3.137*2), "Length of absorption zones (front/back, left/right)"),
    # waves
    ("waves", True, "Generate waves (True/False)"),
    ("wave_period", 1.4185, "Period of the waves"),
    ("wave_height", 0.07, "Height of the waves"),
    ("wave_dir", (1., 0., 0.), "Direction of the waves (from left boundary)"),
    ("wave_type", 'Linear', "type of wave"),
    # caisson
    ("caisson", True, "caisson"),
    ("caisson_dim", (0.5, 0.32), "Dimensions of the caisson"),
    ("caisson_xcoord", None, "x-coord of the caisson"),
    ("caisson_ycoord", 1.41, "y-coord of the caisson"),
    ("caisson_width", 1., "Width of the caisson"),
    ("free_x", (1.0, 1.0, 1.0), "Translational DOFs"),
    ("free_r", (1.0, 1.0, 1.0), "Rotational DOFs"),
    ("VCG", 0.135, "vertical position of the barycenter of the caisson"),
    ("caisson_mass", 125., "Mass of the caisson"),
    ("caisson_inertia", 4.05, "Inertia of the caisson"),
    ("rotation_angle", 0., "Initial rotation angle (in degrees)"),
    ("chrono_dt", 1e-5, "time step of chrono"),
    # numerical options
    ("he", 0.05, "characteristic element length"),
    ("genMesh", True, "True: generate new mesh every time. False: do not generate mesh if file exists"),
    ("use_gmsh", False, "True: use Gmsh. False: use Triangle/Tetgen"),
    ("movingDomain", True, "True/False"),
    ("T", 10.0, "Simulation time"),
    ("dt_init", 0.001, "Initial time step"),
    ("dt_fixed", None, "Fixed (maximum) time step"),
    ("timeIntegration", "backwardEuler", "Time integration scheme (backwardEuler/VBDF)"),
    ("cfl", 0.4 , "Target cfl"),
    ("nsave", 5, "Number of time steps to save per second"),
    ("useRANS", 0, "RANS model"),
    ("parallel", True ,"Run in parallel")])



# ----- CONTEXT ------ #

wavelength=1.
# general options
waterLevel = opts.water_level
rotation_angle = np.radians(opts.rotation_angle)

# waves
tank_sponge = opts.tank_sponge # overwritten if waves are generated (see below)
if opts.waves is True:
    height = opts.wave_height
    mwl = depth = opts.water_level
    direction = opts.wave_dir
    if opts.wave_type == 'Linear':
        period = opts.wave_period
        BCoeffs = np.zeros(3)
        YCoeffs = np.zeros(3)
    wave = wt.MonochromaticWaves(period=period, waveHeight=height, mwl=mwl, depth=depth,
                                 g=np.array([0., -9.81, 0.]), waveDir=direction,
                                 wavelength=wavelength,
                                 waveType=opts.wave_type,
                                 Ycoeff=YCoeffs,
                                 Bcoeff=BCoeffs,
                                 Nf=len(BCoeffs),
                                 fast=False)
    wavelength = wave.wavelength
    tank_sponge = [1.*wavelength, 2.*wavelength]


# ----- DOMAIN ----- #

domain = Domain.PlanarStraightLineGraphDomain()


# ----- SHAPES ----- #

# TANK
tank = st.Tank2D(domain, opts.tank_dim)
# Generation / Absorption zones
tank.setSponge(x_n=tank_sponge[0], x_p=tank_sponge[1])
dragAlpha = 5.*2*np.pi/1.004e-6
if tank_sponge[0] > 0: # left region
    if opts.waves is True:
        dragAlpha = 5*(2*np.pi/period)/1.004e-6 
        smoothing = opts.he*3.
        tank.setGenerationZones(x_n=True, waves=wave, smoothing=smoothing, dragAlpha=dragAlpha) # x_n is 'x-'
        tank.BC['x-'].setUnsteadyTwoPhaseVelocityInlet(wave, smoothing=smoothing, vert_axis=1)
    else:
        tank.setAbsorptionZones(x_n=True, dragAlpha=dragAlpha)
        tank.BC['x-'].setNoSlip()
else:
    tank.BC['x-'].setNoSlip()
if tank_sponge[1] > 0: # right region
    tank.setAbsorptionZones(x_p=True, dragAlpha=dragAlpha) # x_p is 'x+'

# boundary conditions
tank.BC['x+'].setNoSlip()
tank.BC['y+'].setAtmosphere()
tank.BC['y-'].setFreeSlip()
tank.BC['sponge'].setNonMaterial()
# fix nodes for moving mesh
tank.BC['x-'].setFixedNodes()
tank.BC['x+'].setFixedNodes()
tank.BC['sponge'].setFixedNodes()
tank.BC['y+'].setFixedNodes()
tank.BC['y-'].setFixedNodes()
    
    
# CAISSON
if opts.caisson is True:
    # from context options
    coords = [0, 0]
    coords[0] = opts.caisson_xcoord or opts.tank_dim[0]/2.
    coords[1] = opts.caisson_ycoord or waterLevel    
    VCG = opts.VCG
    if VCG is None:
        VCG = dim[1]/2.
    barycenter = (0, -opts.caisson_dim[1]/2.+VCG, 0.)
    width = opts.caisson_width
    inertia = opts.caisson_inertia/width

    caisson = st.Rectangle(domain, dim=opts.caisson_dim, barycenter=barycenter)
    caisson.setHoles([[0., 0.]])
    caisson.holes_ind = np.array([0])
    caisson.translate(coords)
    ang = np.radians(opts.rotation_angle)
    rotation_init = np.array([np.cos(ang/2.), 0., 0., np.sin(ang/2.)*1.])
    caisson.rotate(ang, pivot=caisson.barycenter)
    
    # CHRONO
    # system
    system = crb.ProtChSystem(np.array([0., -9.81, 0.]))
    system.setTimeStep(opts.chrono_dt)
    # rigid body
    # pass the shape as argument so proteus automaticallu knows which flag to use
    # to integrate pressure and shear forces/moments
    body = crb.ProtChBody(system=system, shape=caisson)
    from proteus.mbd import pyChronoCore as pych
    x, y, z = caisson.barycenter
    pos = pych.ChVector(x, y, z)
    e0, e1, e2, e3 = rotation_init
    rot = pych.ChQuaternion(e0, e1, e2, e3)
    inertia = pych.ChVector(1., 1., inertia)
    # chrono functions
    # some functions using Chrono syntax are available when accessing the body.ChBody
    body.ChBody.SetPos(pos)
    body.ChBody.SetRot(rot)
    body.ChBody.SetMass(opts.caisson_mass)
    body.ChBody.SetInertiaXX(inertia)
    # non-chrono functions
    # see proteus.mbd.ChRigidBody.pyx for more functions/information
    body.setConstraints(free_x=np.array(opts.free_x), free_r=np.array(opts.free_r))
    body.setRecordValues(all_values=True)
    
    # boundary conditions
    for bc in caisson.BC_list:
        bc.setNoSlip()



# options for the mesh
he = opts.he
domain.MeshOptions.he = he
domain.use_gmsh = opts.use_gmsh
domain.MeshOptions.genMesh = opts.genMesh
domain.MeshOptions.setOutputFiles(name='mesh')


# ASSEMBLE DOMAIN, always after everything is set up
st.assembleDomain(domain)





##########################################
# Numerical Options and other parameters #
##########################################


rho_0=998.2
nu_0 =1.004e-6
rho_1=1.205
nu_1 =1.500e-5
sigma_01=0.0
g = [0., -9.81]




from math import *
from proteus import MeshTools, AuxiliaryVariables
import numpy
import proteus.MeshTools
from proteus import Domain
from proteus.Profiling import logEvent
from proteus.default_n import *
from proteus.ctransportCoefficients import smoothedHeaviside
from proteus.ctransportCoefficients import smoothedHeaviside_integral


#----------------------------------------------------
# other flags
#----------------------------------------------------
movingDomain=opts.movingDomain
checkMass=False
applyCorrection=True
applyRedistancing=True
freezeLevelSet=True

#----------------------------------------------------
# Time stepping and velocity
#----------------------------------------------------
weak_bc_penalty_constant = 10./nu_0#Re
dt_init = opts.dt_init
T = opts.T
nDTout = int(opts.T*opts.nsave)
timeIntegration = opts.timeIntegration
if nDTout > 0:
    dt_out= (T-dt_init)/nDTout
else:
    dt_out = 0
runCFL = opts.cfl
dt_fixed = opts.dt_fixed

#----------------------------------------------------

#  Discretization -- input options
useOldPETSc=False
useSuperlu = not True
spaceOrder = 1
useHex     = False
useRBLES   = 0.0
useMetrics = 1.0
useVF = 1.0
useOnlyVF = False
useRANS = opts.useRANS # 0 -- None
            # 1 -- K-Epsilon
            # 2 -- K-Omega, 1998
            # 3 -- K-Omega, 1988
# Input checks
if spaceOrder not in [1,2]:
    print "INVALID: spaceOrder" + spaceOrder
    sys.exit()

if useRBLES not in [0.0, 1.0]:
    print "INVALID: useRBLES" + useRBLES
    sys.exit()

if useMetrics not in [0.0, 1.0]:
    print "INVALID: useMetrics"
    sys.exit()

#  Discretization
nd = 2
if spaceOrder == 1:
    hFactor=1.0
    if useHex:
	 basis=C0_AffineLinearOnCubeWithNodalBasis
         elementQuadrature = CubeGaussQuadrature(nd,3)
         elementBoundaryQuadrature = CubeGaussQuadrature(nd-1,3)
    else:
    	 basis=C0_AffineLinearOnSimplexWithNodalBasis
         elementQuadrature = SimplexGaussQuadrature(nd,3)
         elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,3)
         #elementBoundaryQuadrature = SimplexLobattoQuadrature(nd-1,1)
elif spaceOrder == 2:
    hFactor=0.5
    if useHex:
	basis=C0_AffineLagrangeOnCubeWithNodalBasis
        elementQuadrature = CubeGaussQuadrature(nd,4)
        elementBoundaryQuadrature = CubeGaussQuadrature(nd-1,4)
    else:
	basis=C0_AffineQuadraticOnSimplexWithNodalBasis
        elementQuadrature = SimplexGaussQuadrature(nd,4)
        elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,4)


# Numerical parameters
sc = 0.5
sc_beta = 1.5
epsFact_consrv_diffusion = 1.0
ns_forceStrongDirichlet = False
backgroundDiffusionFactor=0.01
if useMetrics:
    ns_shockCapturingFactor  = sc
    ns_lag_shockCapturing = True
    ns_lag_subgridError = True
    ls_shockCapturingFactor  = sc
    ls_lag_shockCapturing = True
    ls_sc_uref  = 1.0
    ls_sc_beta  = sc_beta
    vof_shockCapturingFactor = sc
    vof_lag_shockCapturing = True
    vof_sc_uref = 1.0
    vof_sc_beta = sc_beta
    rd_shockCapturingFactor  =sc
    rd_lag_shockCapturing = False
    epsFact_density    = 3.
    epsFact_viscosity  = epsFact_curvature  = epsFact_vof = epsFact_consrv_heaviside = epsFact_consrv_dirac = epsFact_density
    epsFact_redistance = 0.33
    epsFact_consrv_diffusion = epsFact_consrv_diffusion
    redist_Newton = True#False
    kappa_shockCapturingFactor = sc
    kappa_lag_shockCapturing = False#True
    kappa_sc_uref = 1.0
    kappa_sc_beta = sc_beta
    dissipation_shockCapturingFactor = sc
    dissipation_lag_shockCapturing = False#True
    dissipation_sc_uref = 1.0
    dissipation_sc_beta = sc_beta
else:
    ns_shockCapturingFactor  = 0.9
    ns_lag_shockCapturing = True
    ns_lag_subgridError = True
    ls_shockCapturingFactor  = 0.9
    ls_lag_shockCapturing = True
    ls_sc_uref  = 1.0
    ls_sc_beta  = 1.0
    vof_shockCapturingFactor = 0.9
    vof_lag_shockCapturing = True
    vof_sc_uref  = 1.0
    vof_sc_beta  = 1.0
    rd_shockCapturingFactor  = 0.9
    rd_lag_shockCapturing = False
    epsFact_density    = 1.5
    epsFact_viscosity  = epsFact_curvature  = epsFact_vof = epsFact_consrv_heaviside = epsFact_consrv_dirac = epsFact_density
    epsFact_redistance = 0.33
    epsFact_consrv_diffusion = 10.0
    redist_Newton = False#True
    kappa_shockCapturingFactor = 0.9
    kappa_lag_shockCapturing = True#False
    kappa_sc_uref  = 1.0
    kappa_sc_beta  = 1.0
    dissipation_shockCapturingFactor = 0.9
    dissipation_lag_shockCapturing = True#False
    dissipation_sc_uref  = 1.0
    dissipation_sc_beta  = 1.0

tolfac = 0.001
mesh_tol = 0.001
ns_nl_atol_res = max(1.0e-8,tolfac*he**2)
vof_nl_atol_res = max(1.0e-8,tolfac*he**2)
ls_nl_atol_res = max(1.0e-8,tolfac*he**2)
mcorr_nl_atol_res = max(1.0e-8,0.1*tolfac*he**2)
rd_nl_atol_res = max(1.0e-8,tolfac*he)
kappa_nl_atol_res = max(1.0e-8,tolfac*he**2)
dissipation_nl_atol_res = max(1.0e-8,tolfac*he**2)
mesh_nl_atol_res = max(1.0e-8,mesh_tol*he**2)

#turbulence
ns_closure=0 #1-classic smagorinsky, 2-dynamic smagorinsky, 3 -- k-epsilon, 4 -- k-omega

if useRANS == 1:
    ns_closure = 3
elif useRANS >= 2:
    ns_closure == 4

def twpflowPressure_init(x, t):
    p_L = 0.0
    phi_L = opts.tank_dim[nd-1] - waterLevel
    phi = x[nd-1] - waterLevel
    return p_L -g[nd-1]*(rho_0*(phi_L - phi)+(rho_1 -rho_0)*(smoothedHeaviside_integral(epsFact_consrv_heaviside*opts.he,phi_L)
                                                         -smoothedHeaviside_integral(epsFact_consrv_heaviside*opts.he,phi)))

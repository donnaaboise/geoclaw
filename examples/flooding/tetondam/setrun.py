"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

import os
import numpy as np
from pdb import *


try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must First set CLAW environment variable")

scratch_dir = os.path.join(CLAW, 'geoclaw', 'scratch')

#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2

    rundata = data.ClawRunData(claw_pkg, num_dim)

    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
    #------------------------------------------------------------------
    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    #------------------------------------------------------------------
    # User specified parameters
    #------------------------------------------------------------------


    # Time stepping
    initial_dt = 0.5  # Initial time step
    fixed_dt = False   # Take constant time step

    # Output files
    output_style = 1 #changed 10.21   

    if output_style == 1:
        # Total number of frames will be frames_per_minute*60*n_hours

        n_hours = 24              # Total number of hours in simulation, changed 10.14.2020  should be 5      
        

        frames_per_minute = 1/30   # Frames every 1/2 hour

    if output_style == 2:
        output_times = [1,2,3]    # Specify exact times to output files

    if output_style == 3:
        step_interval = 10   # Create output file every 10 steps
        total_steps = 500    # ... for a total of 500 steps (so 50 output files total)


    # ---------------------------------------------------------------------------------
    # Grid 
    # Changes when the topo file changes 
    # ---------------------------------------------------------------------------------
    # Topo info (TetonDamLatLong.topo) decimal degrees, no minutes
    m_topo = 4180
    n_topo = 1464
    xllcorner = -112.390734400000
    yllcorner = 43.581746970335
    cellsize = 0.000277729665


    #Topo info (TetonLarge.Topo) decimal degrees, no minutes
    # m_topo = 3996
    # n_topo = 2988
    # xllcorner = -112.360138888891
    # yllcorner = 43.170138888889 #copied into matlab
    # cellsize = 0.000277729665

    # Computational coarse grid

    mx = 54
    my = 19

    #Topo info (TetonLarge.Topo) decimal degrees, no minutes
    # m_topo = 3996
    # n_topo = 2988
    # xllcorner = -112.360138888891
    # yllcorner = 43.170138888889 #copied into matlab
    # cellsize = 0.000277729665

    # mx = 60
    # my = 45

    maxlevel = 4 #resolution based on levels
    ratios_x = [2,4,4,4]
    ratios_y = [2,4,4,4]
    ratios_t = [2,4,4,4] #should this be 0,0,0,0?

    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim

    # Derived info from the topo map
    mx_topo = m_topo - 1
    my_topo = n_topo - 1
    xurcorner = xllcorner + cellsize*mx_topo
    yurcorner = yllcorner + cellsize*my_topo
    ll_topo = np.array([xllcorner, yllcorner])
    ur_topo = np.array([xurcorner, yurcorner])

    dims_topo = ur_topo - ll_topo

    # Try to match aspect ratio of topo map
    clawdata.num_cells[0] = mx
    clawdata.num_cells[1] =  my

    print("Approximate aspect ratio : {0:16.8f}".format(float(clawdata.num_cells[0])/clawdata.num_cells[1]))
    print("Actual      aspect ratio : {0:16.8f}".format(dims_topo[0]/dims_topo[1]))

    dim_topo = ur_topo - ll_topo
    mdpt_topo = ll_topo + 0.5*(ur_topo-ll_topo)

    #can adjust the 0.95 to include Blackfoot :)
    dim_comp = 0.95*dim_topo   # Shrink domain inside of given bathymetry.

    clawdata.lower[0] = mdpt_topo[0] - dim_comp[0]/2.0
    clawdata.upper[0] = mdpt_topo[0] + dim_comp[0]/2.0

    clawdata.lower[1] = mdpt_topo[1] - dim_comp[1]/2.0
    clawdata.upper[1] = mdpt_topo[1] + dim_comp[1]/2.0
    print("[{0:16.8f},{1:16.8f}]".format(*clawdata.lower))
    print("[{0:16.8f},{1:16.8f}]".format(*clawdata.upper))

    dims_computed = np.array([clawdata.upper[0]-clawdata.lower[0], 
                             clawdata.upper[1]-clawdata.lower[1]])
    print("Computed aspect ratio    : {0:16.8f}".format(dims_computed[0]/dims_computed[1]))


    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2

    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0


    # Restart from checkpoint file of a previous run?
    # Note: If restarting, you must also change the Makefile to set:
    #    RESTART = True
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk00006'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = output_style

    if clawdata.output_style == 1:
        # Output nout frames at equally spaced times up to tfinal: number of output frames
        clawdata.num_output_times = int(frames_per_minute*60*n_hours)  # Plot 72 output times (every 1/2 hour), tfinal = equation
        clawdata.tfinal = 60*60*n_hours #total number of seconds
        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = output_times

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = step_interval
        clawdata.total_steps = total_steps
        clawdata.output_t0 = True
        clawdata.tfinal = total_steps*fixed_dt


    clawdata.output_format = 'ascii'      # 'ascii' or 'netcdf'

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'none'  # eta=h+B is in q
    clawdata.output_aux_onlyonce = True    # output aux arrays only at t0 (not in each frame)



    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 4



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = not fixed_dt

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = initial_dt

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 5000




    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2

    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'

    # For unsplit method, transverse_waves can be
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2

    # Number of waves in the Riemann solution:
    clawdata.num_waves = 3

    # List of limiters to use for each wave family:
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms

    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used,
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'
    clawdata.bc_upper[0] = 'extrap'

    clawdata.bc_lower[1] = 'extrap'
    clawdata.bc_upper[1] = 'extrap'

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 0

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif clawdata.checkpt_style == 1:
        # Checkpoint only at tfinal.
        pass

    elif clawdata.checkpt_style == 2:
        # Specify a list of checkpoint times.
        clawdata.checkpt_times = [0.1,0.15]

    elif clawdata.checkpt_style == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5


    # -----------------------------------------------
    # AMR parameters:
    # -----------------------------------------------
    amrdata = rundata.amrdata

    amrdata.amr_levels_max = maxlevel    # Set to 3 for best results (6 for tsunami research)
    amrdata.refinement_ratios_x = ratios_x # [3,5,4,5,6]
    amrdata.refinement_ratios_y = ratios_y # [3,5,4,5,6]
    amrdata.refinement_ratios_t = ratios_t # [1,1,1,1,1]
    # rundata.tol = -1
    # rundata.tolsp = 0.001

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft','center']


    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level (L) between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points: 
    amrdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0

    # because developing and benchmarking this for TetonDam
    # Toggle debugging print statements :
    amrdata.dprint = False # print domain flags
    amrdata.eprint = False # print err est flags
    amrdata.edebug = False # even more err est flags
    amrdata.gprint = False # grid bisection/clustering
    amrdata.nprint = False # proper nestling output
    amrdata.pprint = False # projection of the tagged points
    amrdata.rprint = False # print regridding summary
    amrdata.sprint = False # space/memory output
    amrdata.tprint = True  # time step reporting each level
    amrdata.uprint = False # update/upbnd reporting

    # More AMR parameters can be set -- see the defults in pyclaw/data.py 

    # -----------------------------------------------

    # Regions: 

    # -----------------------------------------------
  

    # To specify regions of refinement append lines of the form
    #    regions.append([minlevel,maxlevel,t1,t2,x1,x2,y1,y2])

    # -----------------------------------------------
    regions = rundata.regiondata.regions

    # Region containing initial reservoir
    regions.append([4,4, 0, 1.e10,-111.7,-111.24,43.83, 43.9881])

    # Box containing gauge location locations
    import tools

    xll = [-111.64, 43.913661]  # From email
    xur = [-111.60, 43.92]      # from email
    region_lower, region_upper,_ = tools.region_coords(xll,xur,
                                                     clawdata.num_cells,
                                                     clawdata.lower,
                                                     clawdata.upper)

    regions.append([5,5,0, 1e10, region_lower[0],region_upper[0],region_lower[1],region_upper[1]])

    # Computational domain.  With exception of region above, don't go beyond level 4
    regions.append([1,4,0, 1e10, clawdata.lower[0],clawdata.upper[0],clawdata.lower[1],clawdata.upper[1]])

    # -------------------------------------------------------

    #
    # For gauges append lines of the form  [gaugeno, x, y, t1, t2]
    # -------------------------------------------------------
    # SPERO: when coding gauges, make sure to be in degrees when retrieving that data
    rundata.gaugedata.gtype = {}

    #Stationary Gauges

    #Teton_Canyon_Spero
    xc,yc = [-111.593965, 43.934059] 
    rundata.gaugedata.gauges.append([1,xc,yc,0.,clawdata.tfinal])  # Mid Teton Canyon Spero
    rundata.gaugedata.gtype[1] = 'stationary'

    #Teton_Canyon_Mouth_Spero
    xc,yc = [-111.66637, 43.933847] 
    rundata.gaugedata.gauges.append([2,xc,yc,0.,clawdata.tfinal])  # Teton Canyon Mouth Spero
    rundata.gaugedata.gtype[2] = 'stationary'

    #Wilford_Gauge_Spero
    xc,yc = [-111.672, 43.9144]
    rundata.gaugedata.gauges.append([3,xc,yc,0.,clawdata.tfinal])  # Wilford Gauge Spero
    rundata.gaugedata.gtype[3] = 'stationary'

    #Sugar_City_Gauge_Spero
    xc,yc = [-111.743358, 43.873840]
    rundata.gaugedata.gauges.append([4,xc,yc,0.,clawdata.tfinal])  # Sugar City Gauge 2 Spero
    rundata.gaugedata.gtype[4] = 'stationary'

    #Roberts Gauge Spero
    xc,yc = [-112.126403, 43.7202] 
    rundata.gaugedata.gauges.append([5,xc,yc,0.,clawdata.tfinal])  # Roberts Gauge Spero   
    rundata.gaugedata.gtype[5] = 'stationary'

    #Rexburg_Gauge_Spero
    xc,yc = [-111.792295, 43.823048] 
    rundata.gaugedata.gauges.append([6,xc,yc,0.,clawdata.tfinal])  # Rexburg Gauge Spero
    rundata.gaugedata.gtype[6] = 'stationary'

    # or to have some of each type, use a dictionary:
    rundata.gaugedata.gtype = {}
    
    # lagrangian gauges Northeastern
    for iyg in range(0,3): #ten is the grid
        for ixg in range(0,3):
            gaugeno = 10*iyg + ixg + 100
            yg = 43.91335 + 0.01*iyg #testing
            xg = -111.6211080 + 0.012*ixg #test
            rundata.gaugedata.gauges.append([gaugeno, xg, yg, 0., 1e10])
            rundata.gaugedata.gtype[gaugeno] = 'lagrangian'
    
    # lagrangian gauges Southwestern - Menan Butte
    for iyg in range(0,3): #ten is the grid
        for ixg in range(0,3):
            gaugeno = 10*iyg + ixg + 200
            yg = 43.800575 + 0.01*iyg #testing
            xg = -111.9419740 + 0.012*ixg #test
            rundata.gaugedata.gauges.append([gaugeno, xg, yg, 0., 1e10])
            rundata.gaugedata.gtype[gaugeno] = 'lagrangian'

    # #Idaho Falls Gauge Spero
    # xc,yc = [-112.17208, 43.32496] 
    # rundata.gaugedata.gauges.append([7,xc,yc,0.,clawdata.tfinal])  # Idaho Falls Gauge Spero    
    # rundata.gaugedata.gtype[7] = 'stationary'

    # # Blackfoot Gauge Spero (potentially because right on the border)
    # xc,yc = [-112.340703, 43.187585] 
    # rundata.gaugedata.gauges.append([8,xc,yc,0.,clawdata.tfinal])  # Blackfoot Gauge Spero
    # rundata.gaugedata.gtype[8] = 'stationary'  

    #LaGrangian Gauges

    #Menan Butte North Gauge Spero
    # xg, yg = (-111.960303, 43.788554)
    # rundata.gaugedata.gauges.append([9,xg,yg,0,clawdata.tfinal])
    # rundata.gaugedata.gtype[9] = 'lagrangian'

    #Menan Butte North Gauge Spero
    # xg, yg = (-111.946528, 43.766423)
    # rundata.gaugedata.gauges.append([10,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[10] = 'lagrangian'

    # #Grid TD Canyon Entrance 1
    # xg, yg = (-111.613103, 43.936085)
    # rundata.gaugedata.gauges.append([11,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[11] = 'lagrangian'

    #Grid TD Canyon Entrance 2
    # xg, yg = (-111.613103, 43.932788)
    # rundata.gaugedata.gauges.append([12,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[12] = 'lagrangian'

    # #Grid TD Canyon Entrance 3
    # xg, yg = (-111.613103, 43.929322)
    # rundata.gaugedata.gauges.append([13,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[13] = 'lagrangian'

    #Grid TD Canyon Entrance 4
    # xg, yg = (-111.613103, 43.926584)
    # rundata.gaugedata.gauges.append([14,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[14] = 'lagrangian'

    # #Grid TD Canyon Entrance 5
    # xg, yg = (-111.613103, 43.9923232)
    # rundata.gaugedata.gauges.append([15,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[15] = 'lagrangian'

    # #Grid TD Canyon Entrance 6
    # xg, yg = (-111.20021, 43.9536721)
    # rundata.gaugedata.gauges.append([16,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[16] = 'lagrangian'

    # #Grid TD Canyon Entrance 7
    # xg, yg = (-111.20021, 43.932245)
    # rundata.gaugedata.gauges.append([17,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[17] = 'lagrangian'

    #  #Grid TD Canyon Entrance 8
    # xg, yg = (-111.20021, 43.924967)
    # rundata.gaugedata.gauges.append([18,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[18] = 'lagrangian'

    # #Grid TD Canyon Entrance 9
    # xg, yg = (-111.20021, 43.923153)
    # rundata.gaugedata.gauges.append([19,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[19] = 'lagrangian'

    # #Grid TD Canyon Entrance 10
    # xg, yg = (-111.20021, 43.918381)
    # rundata.gaugedata.gauges.append([20,xg,yg,0,clawdata.tfinal])  
    # rundata.gaugedata.gtype[20] = 'lagrangian'

    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")


    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2   # LatLong coordinates
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = True #edited 7.20 to see impact (for fun)

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0.0
    geo_data.dry_tolerance = 1.e-3
    geo_data.friction_forcing = True
    geo_data.manning_coefficient = 0.06 # changed today 10142020, to 0.08 LI Developed  - need to make variable manning_coefficient
    geo_data.friction_depth = 1.e6

    # Refinement data
    refinement_data = rundata.refinement_data
    refinement_data.wave_tolerance = 1.e-2
    refinement_data.deep_depth = 1e2
    refinement_data.max_level_deep = 3
    refinement_data.variable_dt_refinement_ratios = False    #(09/23/2020)

    # == settopo.data values ==
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #    [topotype, minlevel, maxlevel, t1, t2, fnameg500

    # topo_data.topofiles.append([2, 1, 10, 0, 1e10, 'topos/TetonDamFloodPlain.topo']);
    # topo_data.topofiles.append([2, 1, 10, 0, 1e10, 'topos/TetonDamLargeLowRes.topo'])
    # topo_data.topofiles.append([2, 1, 10, 0, 1e10, 'topos/TetonDamSmallHiRes.topo'])

    topo_data.topofiles.append([2, 1, 10, 0, 1e10, os.path.join(scratch_dir,'TetonDamLatLong.topo')]) #glues together directories (scratch_dir temp directory)
    # topo_data.topofiles.append([2, 1, 10, 0, 1e10, 'topos/TetonDamLarge.topo'])


    # == setdtopo.data values ==
    topo_data = rundata.topo_data
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]
    dtopo_data = rundata.dtopo_data

    # == setqinit.data values ==set
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]

    # == setfixedgrids.data values ==
    fixedgrids = rundata.fixed_grid_data
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    return rundata
    # end of function setgeo
    # ----------------------


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()



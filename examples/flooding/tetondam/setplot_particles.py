"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""
"""
Set up the plot figures, axes, and items to be done for each frame.

this module is imported by the plotting routines and then the
fucntion setplot is called to set the plot parameters.

"""
import sys                              #sys - Python system-specific parameters and functions, this compiles Python arguments to be used
import numpy as np                      #import numpy as np is an alias for the namespace that will be created
import matplotlib.pyplot as plt         #collection of command style functions that makes the code work like MATLAB when creating figures
from clawpack.geoclaw import topotools  #tools facilitate creating and manipulating topo/bathymetry file inputs 
from clawpack.visclaw import gaugetools

from clawpack.visclaw import particle_tools
from clawpack.visclaw import legend_tools

#--------------------------
def setplot(plotdata):                  #defining setplot command (indenting by Python)
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """
    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    from clawpack.visclaw import colormaps, geoplot #colormaps found in visclaw module geoplot
    from numpy import linspace #tool in Python for creating numeric sequences (evenly spaced numbered structures)

    plotdata.clearfigures()  # clear any old figures,axes,items data

    plotdata.verbose = False #always false 

    plotdata.format = 'ascii'                # Format of output

    #------------------------------------------------------------------
    # Setting global KML flags - NEW
    #------------------------------------------------------------------



    #------------------------------------------------------------------
    #SECTION FOR PLOTTING GAUGES - NEW
    #------------------------------------------------------------------


    print('Reading all gauges...')
    gauge_solutions = particle_tools.read_gauges(gaugenos='all', 
                                                 outdir=plotdata.outdir)

    gaugenos_lagrangian = [k for k in gauge_solutions.keys() \
                if gauge_solutions[k].gtype=='lagrangian']
    gaugenos_stationary = [k for k in gauge_solutions.keys() \
                if gauge_solutions[k].gtype=='stationary']

    print('+++ gaugenos_lagrangian: ',gaugenos_lagrangian)
    
    def add_particles(current_data):
        t = current_data.t

        # plot recent path:
        t_path_length = 60.0   # length of path trailing particle (how far in time (s))
        kwargs_plot_path = {'linewidth':1, 'color':'k'}
        particle_tools.plot_paths(gauge_solutions, 
                                  t1=t-t_path_length, t2=t, 
                                  gaugenos=gaugenos_lagrangian, 
                                  kwargs_plot=kwargs_plot_path)

        # plot current location:
        kwargs_plot_point = {'marker':'o','markersize':3,'color':'W'} #point color
        particle_tools.plot_particles(gauge_solutions, t, 
                                      gaugenos=gaugenos_lagrangian, 
                                      kwargs_plot=kwargs_plot_point)  

        # plot any stationary gauges:
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos=gaugenos_stationary, format_string='kx', add_labels=False)
        kwargs={'loc':'upper left'}
        legend_tools.add_legend(['Lagrangian particle','Stationary gauge'],
                linestyles=['',''], markers=['o','x'],
                loc='lower right', framealpha=0.5, fontsize=10)


    def speed(current_data):
        from pylab import sqrt, where, zeros
        from numpy.ma import masked_where, allequal
        q = current_data.q
        h = q[0,:,:]
        hs = sqrt(q[1,:,:]**2 + q[2,:,:]**2)
        where_hpos = (h > 1e-3)
        s = zeros(h.shape)
        s[where_hpos] = hs[where_hpos]/h[where_hpos]
        s = masked_where(h<1e-3, s) # if you want 0's masked out
        #s = s * 1.94384  # convert to knots
        return s

    speed_cmap = colormaps.make_colormap({0:[0,1,1], 0.5:[1,1,0], 1:[1,0,0]})


    #-----------------------------------------
    # Figure for pcolor plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Teton Dam', figno=0)
    plotfigure.kwargs = {'figsize': (9,4)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Speed'
    plotaxes.scaled = True
    plotaxes.xlimits = [-112.36171859324912, -111.25911793671588]
    plotaxes.ylimits = [43.591904932832371, 43.977907507732617]
    plotaxes.afteraxes = add_particles

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.depth   # Plot height field h.
    plotitem.pcolor_cmap = geoplot.googleearth_flooding
    
    cmin = 0 #color axis MATLAB scaling for water color
    cmax = 20 #color axis MATLAB scaling for water color, note this is being used for velocity
    cmap = geoplot.googleearth_flooding  # transparent --> light blue --> dark blue
    
    plotitem.pcolor_cmin = cmin #defining the minimum color using color axis
    plotitem.pcolor_cmax = cmax #defining the maximum color using color axis
    plotitem.add_colorbar = True
    plotitem.colorbar_label = 'm/s'
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0]
    plotitem.amr_patchedges_color = ['m','g','w'] #can try 

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.show = False
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]

    #-------------------------------------------------------------
    #  Set several parameters for the Teton Dam Modeling
    #-------------------------------------------------------------
    #plotdata.kml_name = "Teton Dam"
    #plotdata.kml_starttime = [1976,6,5,17,55,0]  # Date/time of event in UTC [None]
    #plotdata.kml_tz_offset = 0    # Time zone offset (in hours) of event. [None]

    #plotdata.kml_index_fname = "TetonDam"  # name for .kmz and .kml files ["_GoogleEarth"]

    # Set to a URL where KMZ file will be published.
    # plotdata.kml_publish = 'http://math.boisestate.edu/~calhoun/visclaw/GoogleEarth/kmz'

    #-----------------------------------------------------------
    # Figure for KML files
    #----------------------------------------------------------
    #plotfigure = plotdata.new_plotfigure(name='Teton Dam',figno=1) #specifying specific desired plots
    #plotfigure.show = True #showing what we plot (always on)
    #plotfigure.kwargs = {'figsize': (9,4)} #ask donna what it means kwargs?

    #plotfigure.use_for_kml = True #output as KML required true to visualize GeoClaw in Google Earth
    #plotfigure.kml_use_for_initial_view = True #no extra editing required 

    # Latlong box used for GoogleEarth
    #plotfigure.kml_xlimits = [-112.36171859324912, -111.25911793671588] #coordinates of TetonLarge.topo
    #plotfigure.kml_ylimits = [43.591904932832371, 43.977907507732617] #coordinates of TetonLarge.topo

    # Use computational coordinates for plotting
    #plotfigure.kml_use_figure_limits = True #use the xlimits and ylimits above
    #plotfigure.kml_figsize = [54,19] #width 54 inches, height 19 inches
    #plotfigure.kml_dpi = 32 #dots per inch, 32 pixels specified

    # --------------------------------------------------
    #plotfigure.kml_tile_images = False # loading / python w/ gdal installation

    # Color axis : transparency below 0.1*(cmax-cmin)
    #cmin = 0 #color axis MATLAB scaling for water color
    #cmax = 5 #color axis MATLAB scaling for water color
    #cmap = geoplot.googleearth_flooding  # transparent --> light blue --> dark blue
    #cmin, cmax = caxis #added 5.20.2020

    # Water
    # plotaxes = plotfigure.new_plotaxes('kml')
    # plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    # plotitem.plot_var = geoplot.depth   # Plot height field h.
    # plotitem.pcolor_cmap = geoplot.googleearth_flooding
    # plotitem.pcolor_cmin = cmin #defining the minimum color using color axis
    # plotitem.pcolor_cmax = cmax #defining the maximum color using color axis

    # def kml_colorbar(filename): #file name defined above
    #     geoplot.kml_build_colorbar(filename,cmap,cmin,cmax) #building the color bar

    # plotfigure.kml_colorbar = kml_colorbar #colorbar will appear when shown on Google Earth

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
   
    plotfigure = plotdata.new_plotfigure(name='Flood height', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('Teton Dam') #renamed Teton Dam
    plotaxes.title = 'Surface'
    plotaxes.scaled = False # look into this
    plotaxes.ylimits = [0,20] #20 m max (belongs to the blue section)

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0 #plot the water, keep at zero for h
    plotitem.plotstyle = 'b-' #changing line color
    plotitem.show = True

    def fix_gauge(current_data):
        from pylab import plot, title
        t = current_data.t
        plot(t, 0*t, 'k')
        gaugeno = current_data.gaugeno
        if gaugeno in gaugenos_stationary:
            title('Surface elevation at stationary gauge %s' % gaugeno)
        else:
            title('Surface elevation at lagrangian gauge %s' % gaugeno)

    plotaxes.afteraxes = fix_gauge


    # def gaugetopo(current_data):
    #     q = current_data.q
    #     h = q[0,:]
    #     eta = q[3,:]
    #     topo = eta - h # this will have it begin at 0, rather than above the topo
    #     return topo

    # plotitem.plot_var = gaugetopo
    # plotitem.plotstyle = 'g-'

    #def afterframe(current_data):
        #from pylab import plot, legend, xticks, floor, axis, xlabel, ylabel, title
        #t = current_data.t
        #gaugeno = current_data.gaugeno
        #import pdb
        #pdb.set_trace()
        #if gaugeno == 1:
        #    title('Teton Canyon')
        #elif gaugeno == 2:
            #title('Teton Canyon Mouth')
        #elif gaugeno == 3:
            #title('Wilford')
        #elif gaugeno == 4:
            #title('Sugar City')
        #elif gaugeno == 5:
            #title('Roberts')
        #elif gaugeno == 6:
            #title('Rexburg')
        #elif gaugeno == 7:
            #title('Idaho Falls')
        #elif gaugeno == 8:
            #title('Blackfoot')
        #elif gaugeno ==9:
        #    title('Menan Butte North')
        #elif gaugeno ==10:
        #    title("Menan Butte South")
        #elif gaugeno == 11:
        #    title('grid 1')
        #elif gaugeno == 12:
        #    title('grid 2')
        #elif gaugeno == 13:
        #    title('grid 3')
        #elif gaugeno == 14:
        #    title('grid 4')
        #elif gaugeno == 15:
        #    title('grid 5')
        #elif gaugeno == 16:
        #    title('grid 6')
        #elif gaugeno == 17:
        #    title('grid 7')
        #elif gaugeno == 18:
        #    title('grid 8')
        #elif gaugeno == 19:
        #    title('grid 9')
        #elif gaugeno == 20:
        #    title('grid 10')


        #xlabel('Time (hours)')
        #ylabel('Inundation Level (feet)') #does not like
        #legend()
        #print("here") ~you can use this to check here in the code by uncommenting

        # plot(t, 0*t, 'k')
        #n = int(floor(t.max()/3600.) + 2)
        #xticks([3600*i for i in range(n)], ['%i' % i for i in range(n)])

    #plotaxes.afteraxes = afterframe
    
    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.parallel = True                 #
    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = range(0,1440,1)        # list of frames to print - can try ten
    plotdata.print_gaugenos = 'all'           # list of gauges to print, linked to fignos above
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                    # create html files of plots?
    plotdata.html_movie = True                  # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    #plotdata.latex_figsperline = 2           # layout of plots
    #plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once
    plotdata.kml = False
    plotdata.html_movie_width = 700         # width used in JSAnimation
    
    return plotdata
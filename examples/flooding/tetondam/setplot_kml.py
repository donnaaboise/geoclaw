
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""

import numpy as np
import matplotlib.pyplot as plt

from clawpack.geoclaw import topotools

try:
    TG32412 = np.loadtxt('32412_notide.txt')
except:
    print "*** Could not load DART data file"

#--------------------------
def setplot(plotdata):
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """


    from clawpack.visclaw import colormaps, geoplot
    from numpy import linspace

    plotdata.clearfigures()  # clear any old figures,axes,items data

    plotdata.verbose = False


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos='all', format_string='ko', add_labels=True)


    #-----------------------------------------
    # Some global kml flags
    #-----------------------------------------
    plotdata.kml_name = "Teton Dam"
    plotdata.kml_starttime = [1976,2,27,6,34,0]  # Time of event in UTC [None]
    # plotdata.kml_tz_offset = 3    # Time zone offset (in hours) of event. [None]

    plotdata.kml_index_fname = "TetonDam"  # name for .kmz and .kml files ["_GoogleEarth"]

    # Set to a URL where KMZ file will be published.
    # plotdata.kml_publish = None

    # Colormap range
    cmin = 0
    cmax = 80
    cmap = geoplot.googleearth_transparent

    dark_blue   = [0.2, 0.2, 0.7, 1.0];
    light_blue  = [0.7, 0.7, 1.0, 1.0];
    transparent = [0.7, 0.7, 1.0, 0.0]
    flooding_colormap = colormaps.make_colormap({-1:transparent,
                                                 0.0:light_blue,
                                                 1.0:dark_blue})

    dark_blue = [0.2,0.2,0.7];
    light_blue = [0.7,0.7,1.0];
    flooding_colormap = colormaps.make_colormap({ -1.0:light_blue,
                                                 1.0:dark_blue})

    cmap = flooding_colormap

    #-----------------------------------------------------------
    # Figure for KML files
    #----------------------------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Teton Dam',figno=1)
    plotfigure.show = True

    plotfigure.use_for_kml = True
    plotfigure.kml_use_for_initial_view = True

    # These override any axes limits set below in plotaxes
    plotfigure.kml_xlimits = [-111.684952, -111.373222]
    plotfigure.kml_ylimits = [43.889109, 43.937331];

    # Resolution (should be consistent with data)
    # Refinement levels : [2,6]; max level = 3; num_cells = [30,30]
    # rcl : resolution of the coarsest level in this figure
    rcl = 4    # rcl*figsize = num_cells
    plotfigure.kml_figsize = [24.979,5.364]
    plotfigure.kml_dpi = 10         # Resolve all three levels
    plotfigure.kml_tile_images = False    # Tile images for faster loading.  Requires GDAL [False]


    # Water
    plotaxes = plotfigure.new_plotaxes('kml')
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.plot_var = geoplot.surface
    plotaxes.xlimits = [0,24990]
    plotaxes.ylimits = [0,5370]
    plotitem.pcolor_cmap = flooding_colormap
    plotitem.pcolor_cmin = 0
    plotitem.pcolor_cmax = 80

    def kml_colorbar(filename):
        geoplot.kml_build_colorbar(filename,cmap,cmin,cmax)

    plotfigure.kml_colorbar = kml_colorbar

    #-----------------------------------------------------------
    # Figure for KML files (zoom)
    #----------------------------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Power Plant (zoom)',figno=2)
    plotfigure.show = True

    plotfigure.use_for_kml = True
    plotfigure.kml_use_for_initial_view = False  # Use large plot for view

    # Set Google Earth bounding box and figure size
    ay = 43.913661
    by = 43.916382

    ax = -111.623926
    bx = -111.620150

    plotfigure.kml_xlimits = [ax,bx]
    plotfigure.kml_ylimits = [ay,by]
    plotfigure.kml_figsize = [30,30]  # inches.

    # Resolution
    plotfigure.kml_dpi = 20       # Resolve all three levels
    plotfigure.kml_tile_images = False  # Tile images for faster loading.


    plotaxes = plotfigure.new_plotaxes('kml')
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.plot_var = geoplot.surface
    plotitem.pcolor_cmap = cmap
    plotitem.pcolor_cmin = cmin
    plotitem.pcolor_cmax = cmax

    def kml_colorbar(filename):
        geoplot.kml_build_colorbar(filename,cmap,cmin,cmax)

    plotfigure.kml_colorbar = kml_colorbar


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface at gauges', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    # plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    # Plot topo as green curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = True

    def gaugetopo(current_data):
        q = current_data.q
        h = q[0,:]
        eta = q[3,:]
        topo = eta - h
        return topo

    plotitem.plot_var = gaugetopo
    plotitem.plotstyle = 'g-'

    def add_zeroline(current_data):
        from pylab import plot, legend, xticks, floor, axis, xlabel
        t = current_data.t
        gaugeno = current_data.gaugeno

        if gaugeno == 32412:
            try:
                plot(TG32412[:,0], TG32412[:,1], 'r')
                legend(['GeoClaw','Obs'],loc='lower right')
            except: pass
            axis((0,t.max(),-0.3,0.3))

        plot(t, 0*t, 'k')
        n = int(floor(t.max()/3600.) + 2)
        xticks([3600*i for i in range(n)], ['%i' % i for i in range(n)])
        xlabel('time (hours)')

    plotaxes.afteraxes = add_zeroline


    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.parallel = True
    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = range(0,4)         # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = [1,2]           # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_movie = None                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = False                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    plotdata.kml = True

    return plotdata

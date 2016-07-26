
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from clawpack.geoclaw import topotools

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


    #-----------------------------------------
    # Some global kml flags
    #-----------------------------------------
    plotdata.kml_name = "Teton Dam"
    plotdata.kml_starttime = [1976,6,5,17,55,0]  # Date/time of event in UTC [None]
    plotdata.kml_tz_offset = 6    # Time zone offset (in hours) of event. [None]

    plotdata.kml_index_fname = "TetonDam"  # name for .kmz and .kml files ["_GoogleEarth"]

    # Set to a URL where KMZ file will be published.
    # plotdata.kml_publish = 'http://math.boisestate.edu/~calhoun/visclaw/GoogleEarth/kmz'

    #-----------------------------------------------------------
    # Figure for KML files
    #----------------------------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Teton Dam',figno=1)
    plotfigure.show = True

    plotfigure.use_for_kml = True
    plotfigure.kml_use_for_initial_view = True

    # Latlong box used for GoogleEarth

    # plotfigure.kml_xlimits = [-111.96132553, -111.36256443]  #
    # plotfigure.kml_ylimits = [43.79453362, 43.95123268]
    plotfigure.kml_xlimits = [ -112.3895, -111.2400]
    plotfigure.kml_ylimits = [43.5818, 43.9881]

    # Use computational coordinates for plotting
    plotfigure.kml_use_figure_limits = True

    # --------------------------------------------------
    # Resolution (should be consistent with data)
    # Refinement levels : [4,4]; max level = 3; num_cells = [90,32]
    # Aim for 1 pixel per finest level grid cell.  Trying to increase the
    # resolution beyond this can lead to weird aliasing effects (which
    # only seem to affect the vertical resolution - possible bug in Matplotlib?)

    # If amr refinement ratios set to [4,4]; max_level = 2
    # figsize*dpi = [36,12.8]*10 = [90,32]*4 = [360,128]
    plotfigure.kml_figsize = [36.0, 12.8]
    plotfigure.kml_dpi = 2*10

    # If amr refinement ratios set to [4,4]; max_level = 3
    # figsize*dpi = [144,51.2]*10 = [90,32]*4*4 = [1440,512]
    plotfigure.kml_figsize = [144.0, 51.2]
    plotfigure.kml_dpi = 20

    # --------------------------------------------------

    plotfigure.kml_tile_images = True    # Tile images for faster loading.  Requires GDAL [False]

    # Color axis : transparency below 0.1*(cmax-cmin)
    cmin = 0
    cmax = 5
    cmap = geoplot.googleearth_flooding  # transparent --> light blue --> dark blue

    # Water
    plotaxes = plotfigure.new_plotaxes('kml')
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.depth   # Plot height field h.
    plotitem.pcolor_cmap = geoplot.googleearth_flooding
    plotitem.pcolor_cmin = cmin
    plotitem.pcolor_cmax = cmax

    def kml_colorbar(filename):
        geoplot.kml_build_colorbar(filename,cmap,cmin,cmax)

    plotfigure.kml_colorbar = kml_colorbar

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Flood height', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3  # eta?
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

    def afterframe(current_data):
        from pylab import plot, legend, xticks, floor, axis, xlabel,title
        t = current_data.t
        gaugeno = current_data.gaugeno
        if gaugeno == 1:
            title('Wilford')
        elif gaugeno == 2:
            title('Teton City')

        # plot(t, 0*t, 'k')
        n = int(floor(t.max()/3600.) + 2)
        xticks([3600*i for i in range(n)], ['%i' % i for i in range(n)])
        xlabel('time (hours)')

    plotaxes.afteraxes = afterframe


    #-----------------------------------------

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.parallel = True
    plotdata.printfigs = True               # print figures
    plotdata.print_format = 'png'           # file format
    plotdata.print_framenos = range(0,21)         # list of frames to print
    plotdata.print_gaugenos = 'all'         # list of gauges to print
    plotdata.print_fignos = [1,300]         # list of figures to print

    plotdata.html = False                     # create html files of plots?
    plotdata.html_movie = False                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index

    plotdata.latex = False                    # create latex file of plots?
    #plotdata.latex_figsperline = 2           # layout of plots
    #plotdata.latex_framesperline = 1         # layout of plots
    #plotdata.latex_makepdf = False           # also run pdflatex?

    plotdata.kml = True

    return plotdata

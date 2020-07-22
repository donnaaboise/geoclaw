% Patches
hidegridlines(1:6);
% showpatchborders(1:15);
% setpatchborderprops('linewidth',1);

colormap(flipud(parula));
colorbar;
tol = -0.8;
c1 = 0;
c2 = 30;
caxis([c1,c2]);

set(gca,'zlim',[-10,1])

% Adds gauges (doesn't replace the figure) 
add_gauges('geoclaw');
add_regions(t,'geoclaw');

fprintf('%20s %12.4e\n','qmin',qmin);
fprintf('%20s %12.4e\n','qmax',qmax);

% Axes
ax = -112.30466239;
bx = -111.30608538;
ay = 43.6;
by = 43.95823847;

axis([ax bx ay by])
daspect([1 1 1]);
set(gca,'fontsize',16);


title(sprintf('Teton Dam (%d) : t = %.2f (%.2f,%.2f)',Frame,t,qmin,qmax),'fontsize',18);

NoQuery = 0;
prt = false;
MaxFrames = 1000;
if (prt)
    filename = sprintf('tetondam_%04d_fc.png',Frame);
    fprintf('Print file %s\n',filename);
    print('-dpng',filename);
end

shg

clear afterframe;
clear mapc2m;

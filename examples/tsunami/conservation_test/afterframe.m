setviews;

% Data info
fprintf('%10s %24.16e\n','qmin',qmin);
fprintf('%10s %24.16e\n','qmax',qmax);

% AMR patch properties
showpatchborders(1:10);
setpatchborderprops('linewidth',1)

% Axis
view(2);
set(gca,'fontsize',16);
daspect([1,1,1]);

% Color axis
b = 1;  % bathymetry
dh = .1;
%caxis([b-dh,b + dh]);
colorbar


% Print PNG files
prt = false;
NoQuery = 0;
if (prt)
  MaxFrames = 8;
  axis([0 1 0 1]);
  filename = sprintf('annulus_%04d.png',Frame)
  print('-dpng',filename);
end

shg

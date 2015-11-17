function plot_tetondam()

plot_topo('teton_new_topos/TetonDamSmallHiRes.topo','g')
plot_topo('teton_new_topos/TetonDamLargeLowRes.topo','b')
plot_topo('teton_new_topos/TetonDamFloodPlain.topo','r');



end

function [ax,bx,ay,by] = plot_topo(fname,c)
% PLOT_TOPO plots the topo from file FNAME


% close all

% Top of the cinder cone.  Pass these values into plot_feature
% to get the height of the feature. 
% xp = 3.0206e+03;
% yp = 1.1689e+04;

% behind the dam
% xp =  2.6732e+03;
% yp = 1.1942e+04;

% c = 'w';  % Color of the topo
hold on;
[p,ax,bx,ay,by] = plot_feature(fname,c);
hold on;

%fprintf('Height at input location : %12.4f\n',hp);

daspect([1,1,1]);

% axis([ax bx ay by]);

camlight;
view(3);

end


function [p,ax,bx,ay,by,hpout] = plot_feature(fname,c,xp,yp)

fid = fopen(fname);

ncols = fscanf(fid,'%d',1); fscanf(fid,'%s',1);
nrows = fscanf(fid,'%d',1); fscanf(fid,'%s',1);
xll = fscanf(fid,'%g',1);   fscanf(fid,'%s',1);
yll = fscanf(fid,'%g',1);   fscanf(fid,'%s',1);
dx = fscanf(fid,'%g',1);    fscanf(fid,'%s',1);
nodata = fscanf(fid,'%g',1); fscanf(fid,'%s',1);
T = fscanf(fid,'%g',nrows*ncols);
fclose(fid);

% --------------------------------
ax = xll;
ay = yll;

bx = ax + dx*(ncols-1);
by = ay + dx*(nrows-1);

x = linspace(ax,bx,ncols);
y = linspace(ay,by,nrows);

T = reshape(T,ncols,nrows);
T = fliplr(T);

[xm,ym] = meshgrid(x,y);

p = surf(xm,ym,T');
set(p,'facecolor',c);
set(p,'edgecolor','none');

plot_water = false;
if (plot_water)
    hold on;
    % Add plane
    y0 = 11689;
    h0 = 115;
    h1 = 115;
    h(ym < y0) = nan;
    set(gcf,'renderer','opengl');
    xw = [0 5400; 0 5400; 0 5400];
    yw = [y0 y0; y0 y0; 25000 25000];
    zw = [0 0; h0 h0; h1 h1];
    
    
    water = patch(surf2patch(xw,yw,zw));
    set(water,'facecolor','b');
    set(water,'edgecolor','k','linewidth',2);
    set(water,'facealpha',0.7);
end

fprintf('Min height  : %12.4f\n',min(T(:)));
fprintf('Max height  : %12.4f\n',max(T(:)));

if (nargin > 2)
    % find height of given location (xp,yp)
    hp = interp2(xm,ym,T,xp,yp,'linear');
    if (nargout > 5)
        hpout = hp;
    end
end


end



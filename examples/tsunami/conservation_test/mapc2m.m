function [xp,yp,zp] = mapc2m(xc,yc)

global map isflat;

map = 'nomap';

R = 1;
r = 0.4;


switch map
    case 'nomap'
        isflat = true;
        xp = xc;
        yp = yc;

    case 'latlong'
        isflat = false;
        s = 0.0;
        [xc1,yc1,~] = mapc2m_brick(xc,yc,s);

        % Map into [0,1]x[0,1]
        lng = [0 360];
        lat = [-50 50];
        xc2 = lng(1) + (lng(2) - lng(1))*xc1;
        yc2 = lat(1) + (lat(2) - lat(1))*yc1;
        [xp,yp,zp] = mapc2m_latlong(xc2,yc2);
end

if (isflat)
    zp = zeros(size(xp));
end

end

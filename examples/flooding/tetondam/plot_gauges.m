function plot_gauges(plot_var)

if nargin < 1
    plot_var = 'h';
end

close all

% ------------------------------------------
geo_outdir = './_output';

% Scaling
tscale = 1/3600;       % Convert time to hours


% ----------------------------------
gdata = read_gauge_data();

t_idx = 2;
h_idx = 3;
hu_idx = 4;
hv_idx = 5;
eta_idx = 6;

switch plot_var
    case 'h'
        pvidx = 1;
        ystr = 'Flood depth';
        yla = [0, 30];
    case 'u'
        pvidx = 2;
        ystr = 'u-velocity';
        yla = [-275,275];
    case 'v'
        pvidx = 3;
        ystr = 'v-velocity';
        yla  = [-275,275];
    case 'speed'
        pvidx = 4;
        ystr = 'Speed';
        yla  = [-275,275];
    otherwise
        error('No valid plot_var was specified');
end

num_gauges = length(gdata);
for i = 1:num_gauges
    g = gdata(i);
    
    figure(100+i);
    clf;
    hold on;
    
    gname_geo = sprintf('%s/gauge%05d.txt',geo_outdir,g.id);
    if (exist(gname_geo,'file'))
        tseries_geo = importdata(gname_geo,' ',3);
        t_geo = tscale*(tseries_geo.data(:,2));  % Shift by 10 minutes
        eta_geo = tseries_geo.data(:,eta_idx);
        h_geo = tseries_geo.data(:,h_idx);
        u_geo = tseries_geo.data(:,hu_idx)./h_geo;
        v_geo = tseries_geo.data(:,hv_idx)./h_geo;
        speed_geo = sqrt(u_geo.^2 + v_geo.^2);
        pvars_geo = {eta_geo, u_geo, v_geo, speed_geo};
        
        pv_geo = pvars_geo{pvidx};
        
        hold on;
        ph = plot(t_geo,pv_geo,'r.-','linewidth',2,'markersize',8);
        lstr = 'GeoClaw';
    else
        fprintf('File %s does not exist\n',gname_geo);
    end
                        
    title(sprintf('Gauge %d',g.id),'fontsize',18);
    xlabel('t (hours)','fontsize',16);
    ylabel(ystr,'fontsize',16);
    set(gca,'fontsize',16);
    legend(ph,lstr);
    set(gca,'box','on');
        
    % set(gca,'xlim',[7.5,13]);
    set(gca,'ylim',yla);
    
    hold off;
    shg       
end



end
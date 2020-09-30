function test_topo()
xll = -1.123907344000000e+02;
yll = 43.581746970335;
xll_comp = -112.33270279;
xur_comp = -111.28813374;
yll_comp = 43.60206290;
yur_comp = 43.96774955;

topo(1) = struct('xll',xll,'yll',yll,'xur',[],'yur',[],...
    'mx',4180,'my',1464,...
    'xll_comp',xll_comp,'yll_comp',yll_comp,'xur_comp',xur_comp,...
    'yur_comp',yur_comp);

xll = -112.360138888891;
yll = 43.170138888889;
xll_comp = -112.30466239;
yll_comp = 43.21161781;
xur_comp =  -111.30608538;
yur_comp = 43.95823847;
topo(2) = struct('xll',xll,'yll',yll,'xur',[],'yur',[],...
    'mx',3996,'my',2988,...
    'xll_comp',xll_comp,'yll_comp',yll_comp,'xur_comp',xur_comp,...
    'yur_comp',yur_comp);

cellsize = 0.000277729665;


figure(1);
clf;

for i = 1:2
    t = topo(i);
    
    t.xur = t.xll + (t.mx-1)*cellsize;
    t.yur = t.yll + (t.my-1)*cellsize;
    
    
    fprintf('Area (topo) %16.8f\n',(t.xur-t.xll)*(t.yur-t.yll));
    fprintf('Area (comp) %16.8f\n',(t.xur_comp-t.xll_comp)*(t.yur_comp-t.yll_comp));
    
    xp = [t.xll_comp, t.xur_comp, t.xur_comp, t.xll_comp, t.xll_comp];
    yp = [t.yll_comp, t.yll_comp, t.yur_comp, t.yur_comp, t.yll_comp];
    plot(xp,yp,'k','linewidth',2);
    hold on;
    
    xp = [t.xll, t.xur, t.xur, t.xll, t.xll];
    yp = [t.yll, t.yll, t.yur, t.yur, t.yll];
    plot(xp,yp,'k','linewidth',1);
    
    
    daspect([1,1,1]);
    
end

axis([-112.45, -111.15, 43.1,  44.05]);

add_gauges('geoclaw')

%{
gauges = [-112.17208, 43.32496,
    -112.340703, 43.187585,
    -111.960303, 43.788554,
    -111.946528, 43.766423,
    -111.613103, 43.936085,
    -111.613103, 43.932788,
    -111.613103, 43.929322,
    -111.613103, 43.926584,
    -111.613103, 43.9923232,
    -111.20021, 43.9536721,
    -111.20021, 43.932245,
    -111.20021, 43.924967,
    -111.20021, 43.923153,
    -111.20021, 43.918381];

num_gauges = length(gauges);
for n = 1:num_gauges
    id = n + 7;
    x = gauges(n,1);
    y = gauges(n,2);
    hg = plot(x,u,'m.','linewidth',3,'markersize',95);
    h = text(x,y,zp,sprintf('%d',data(1)),'fontsize',11,'color','k');
    set(h,'HorizontalAlignment','center');
    % set(h,'backgroundcolor','none');
    gauge_handles(n) = hg;

plot(gauges(:,1), gauges(:,2),'.','markersize',20);
%}

end













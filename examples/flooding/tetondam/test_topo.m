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
    if i == 1
        p = fill(xp,yp,'r','linewidth',1);
    else
        p = fill(xp,yp,'b','linewidth',1);
    end        
    set(p,'facealpha',0.5);
    
    xp = [t.xll, t.xur, t.xur, t.xll, t.xll];
    yp = [t.yll, t.yll, t.yur, t.yur, t.yll];
    plot(xp,yp,'k','linewidth',1);
        
    
    daspect([1,1,1]);
    
end

axis([-112.45, -111.15, 43.1,  44.05]);

add_gauges('geoclaw')


end













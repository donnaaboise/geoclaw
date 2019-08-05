function fix_topo(fname,mx,my,fname_out)

% ncols        1798
% nrows        1042
% xllcorner    -121.795724838159
% yllcorner    39.364837972813
% cellsize     0.000331742455

d = load(fname);

d1 = reshape(d,my,mx)';
d2 = reshape(d1,mx*my,1);

fid = fopen(fname_out,'w');
for i = 1:mx*my,
  fprintf(fid,'%11.6f\n',d2(i));
end
fclose(fid);

end

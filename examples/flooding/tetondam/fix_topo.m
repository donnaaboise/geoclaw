function fix_topo(fname,mx,my,fname_out)

d = load(fname);

d1 = reshape(d,my,mx)';
d2 = reshape(d1,mx*my,1);

fid = fopen(fname_out,'w');
for i = 1:mx*my,
  fprintf(fid,'%11.6f\n',d2(i));
end
fclose(fid);

end

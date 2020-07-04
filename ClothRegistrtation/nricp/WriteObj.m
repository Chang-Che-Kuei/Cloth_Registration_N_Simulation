f = fopen('0525/Registration.obj','w');

for i = 1 : size(pointsTransformed,1)
    fprintf(f,"v %f %f %f\n", pointsTransformed(i,1), pointsTransformed(i,2), pointsTransformed(i,3) );
end
for i = 1 : size(source.f.v,1)
     fprintf(f,"f %d %d %d\n", source.f.v(i,1), source.f.v(i,2), source.f.v(i,3) );
end


ClothFile = ["Cloth/Small/", "Cloth/Large/", "Cloth/Extra/"];
fileName = ["LeftArm.obj", "RightArm.obj", "Front.obj", "Back.obj"];
SaveFile = ["Cloth/R_Small/", "Cloth/R_Large/", "Cloth/R_Extra/"];

LeftArm = [129,7,311,424; 204,24,424,583; 246,21,522,317; 206,631,452,571]+1;
RightArm = [135,14,307,186; 215,25,451,588; 232,33,539,455; 207,16,457,575]+1;
Front = [493,347,302,4,410,854,894,789; 676,479,410,4,837,1218,1283,1120;
    707,157,400,4,552,1644,1313,1135; 641,458,404,4,771,1084,1113,998]+1;
Back = [337,341,312,4,92,723,751,684; 663,452,401,4,798,1172,1230,1085;
    684,157,428,4,839,1235,1291,1170; 655,462,403,4,800,1106,1144,1040]+1;

for c = 3:3 % How many cloth 
    for part = 1:4 % 4 part of cloth 
        disp(append("Loading ", ClothFile(c), fileName(part) ));
        source = readObj(append('Cloth/Template/', fileName(part) ));
        target =  readObj(append(ClothFile(c), fileName(part) ));

        Source.faces = source.f.v;
        Source.vertices = source.v;
        Source.normals = source.vn;
        Target.faces = target.f.v;
        Target.vertices = target.v;
        Target.normals = target.vn;

        % Specify that surface normals are available and can be used.
        Options.useNormals = 0;

        % Specify that the source deformations should be plotted.
        Options.plot = 1;
        Options.biDirectional = 1;
        Options.rigidInit =0;
        Options.normalWeighting = 0 ;
        Options.ignoreBoundary = 0 ;

        % Perform non-rigid ICP
        landS=[];
        landT=[];
        if part == 1
            landS = LeftArm(1,:);
            landT = LeftArm(c+1,:);
        elseif	part == 2
            landS = RightArm(1,:);
            landT = RightArm(c+1,:);
        elseif	part == 3
            landS = Front(1,:);
            landT = Front(c+1,:);
        else
            landS = Back(1,:);
            landT = Back(c+1,:);
        end
        [pointsTransformed, X] = nricp(Source, Target, Options, landS, landT);
        
        savePath = append(SaveFile(c), fileName(part));
        disp(append("Saving to " ,savePath));
        f = fopen(savePath,'w');

        for i = 1 : size(pointsTransformed,1)
            fprintf(f,"v %f %f %f\n", pointsTransformed(i,1), pointsTransformed(i,2), pointsTransformed(i,3) );
        end
        for i = 1 : size(source.f.v,1)
             fprintf(f,"f %d %d %d\n", source.f.v(i,1), source.f.v(i,2), source.f.v(i,3) );
        end
        
    end
end 
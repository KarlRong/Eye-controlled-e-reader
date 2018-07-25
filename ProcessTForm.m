function [x,y] = ProcessTForm(GazePointX,GazePointY)
load('tform.mat', 'tform');
[x, y] = transformPointsForward(tform, GazePointX, GazePointY);
end


dataDir = '.\calibrateData\';
dataFileName = getlatestfile(dataDir);
calibrateData = readtable([dataDir dataFileName]);

rows_left = calibrateData(calibrateData.BallPosX == 100, :);
rows_left_top = rows_left(rows_left.BallPosY == 100, :);
rows_left_top = rows_left_top((end-15):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
rows_left_bottom = rows_left(rows_left.BallPosY == 764, :);
rows_left_bottom = rows_left_bottom((end-15):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
rows_right = calibrateData(calibrateData.BallPosX == 1436, :);
rows_right_top =  rows_right(rows_right.BallPosY == 100, :);
rows_right_top = rows_right_top((end-15):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
rows_right_bottom =  rows_right(rows_right.BallPosY == 764, :);
rows_right_bottom = rows_right_bottom((end-15):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});

mean_left_top = mean(rows_left_top{:,:},1);
mean_left_bottom = mean(rows_left_bottom{:,:},1);
mean_right_top = mean(rows_right_top{:,:},1);
mean_right_bottom = mean(rows_right_bottom{:,:},1);
GazePoint = [mean_left_top(3:4); mean_right_top(3:4);mean_right_bottom(3:4);mean_left_bottom(3:4)];
BallPos = [mean_left_top(1:2); mean_right_top(1:2);mean_right_bottom(1:2);mean_left_bottom(1:2)];
tform = fitgeotrans(GazePoint, BallPos, 'projective');
save('tform.mat', 'tform');



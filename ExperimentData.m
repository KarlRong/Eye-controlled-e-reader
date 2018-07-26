dataDir = '.\experimentData\';
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
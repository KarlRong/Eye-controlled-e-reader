function mean_error = ExperimentData()
    dataDir = '.\experimentData\';
    dataFileName = getlatestfile(dataDir);
    calibrateData = readtable([dataDir dataFileName]);

    rows_left = calibrateData(calibrateData.BallPosX == 200, :);
    rows_left_top = rows_left(rows_left.BallPosY == 200, :);
    rows_left_top = rows_left_top((end-10):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
    rows_left_bottom = rows_left(rows_left.BallPosY == 664, :);
    rows_left_bottom = rows_left_bottom((end-10):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
    rows_middle = calibrateData(calibrateData.BallPosX == 768, :);
    rows_middle = rows_middle(rows_middle.BallPosY == 432, :);
    rows_middle = rows_middle((end-10):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
    rows_right = calibrateData(calibrateData.BallPosX == 1336, :);
    rows_right_top =  rows_right(rows_right.BallPosY == 200, :);
    rows_right_top = rows_right_top((end-10):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});
    rows_right_bottom =  rows_right(rows_right.BallPosY == 664, :);
    rows_right_bottom = rows_right_bottom((end-10):end,  {'BallPosX','BallPosY','GazePointX', 'GazePointY'});

    rows = [rows_left_top; rows_left_bottom; rows_middle; rows_right_top; rows_right_bottom];
    rows = table2array(rows);
    [rows(:,3), rows(:,4)] = ProcessTForm(rows(:,3), rows(:,4));
	errors = [rows(:,3) - rows(:,1), rows(:,4) - rows(:,2)];
    mean_error = mean(sqrt(errors(:,1).^2 + errors(:,2).^2));
    fig = figure;
    scatter(rows(:,1),rows(:,2),'filled')
    hold on
    scatter(rows(:,3),rows(:,4))
    grid on
    axis equal
    
    saveas(fig, ".\experimentFigure\" + mean_error + " px " + dataFileName(1:(end-4)) + ".png")
    pause(5);
end
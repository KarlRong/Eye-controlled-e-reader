function Y = predictFromGPR_Y(data)
load('GPRModel.mat')
predictorNames = {'EyeBall0X', 'EyeBall0Y', 'EyeBall0Z', 'EyeBall1X', 'EyeBall1Y', 'EyeBall1Z', 'Pupil0X', 'Pupil0Y', 'Pupil0Z', 'Pupil1X', 'Pupil1Y', 'Pupil1Z', 'HeadPosX', 'HeadPosY', 'HeadPosZ', 'HeadAngleX', 'HeadAngleY', 'HeadAngleZ'};

% T = calibrateData(1, :);
T = cell2table(data, 'VariableNames', predictorNames);
Y = trainedModel_Y.predictFcn(T);
end


dataDir = '.\calibrateData\';
dataFileName = getlatestfile(dataDir);
calibrateData = readtable([dataDir dataFileName]);

[trainedModel_X, validationRMSE_X] = trainGPRmodelX(calibrateData);
[trainedModel_Y, validationRMSE_Y] = trainGPRmodelY(calibrateData);

validationRMSE_X
validationRMSE_Y
save('GPRModel');


dataDir = '.\calibrateData\';
dataFileName = getlatestfile(dataDir);
calibrateData = readtable([dataDir dataFileName]);

T = calibrateData(1, :);
EyeBall0 = [T.EyeBall0X T.EyeBall0Y T.EyeBall0Z];
EyeBall1 = [T.EyeBall1X T.EyeBall1Y T.EyeBall1Z];
Pupil0 = [T.Pupil0X T.Pupil0Y T.Pupil0Z];
rayDir0 = Pupil0 / norm(Pupil0);
Pupil1 = [T.Pupil1X T.Pupil1Y T.Pupil1Z];
rayDir1 = Pupil1 / norm(Pupil1);
HeadPos = [T.HeadPosX T.HeadPosY T.HeadPosZ];
HeadRot = [T.HeadAngleX T.HeadAngleY T.HeadAngleZ];
HeadRotMat = Euler2RotationMatrix(HeadRot);

offset = [0 -3.5 6]';

offset_mat = HeadRotMat * offset;
offset_mat = offset_mat';

EyeBallCenter0 = offset_mat + EyeBall0;
EyeBallCenter1 = offset_mat + EyeBall1;

gazeVecAxis0 = RaySphereIntersect([0 0 0], rayDir0, EyeBallCenter0, 12) - EyeBallCenter0;
gazeVecAxis1 = RaySphereIntersect([0 0 0], rayDir1, EyeBallCenter1, 12) - EyeBallCenter1;
gazeAbsolute0 = gazeVecAxis0 / norm(gazeVecAxis0);
gazeAbsolute1 = gazeVecAxis1 / norm(gazeVecAxis1);

EyeBallCenter0_re = [T.EyeBallCenter0X T.EyeBallCenter0Y T.EyeBallCenter0Z];
offset_openface = EyeBallCenter0_re - EyeBall0 - offset_mat
% EyeBallCenter1 = [T.EyeBallCenter1X T.EyeBallCenter1Y T.EyeBallCenter1Z];
% gazeAbsolute0 = [T.Gaze0X T.Gaze0Y T.Gaze0Z];
% gazeAbsolute1 = [T.Gaze1X T.Gaze1Y T.Gaze1Z];
screenVector = [0 0 1];
% a = sym('a')
screenPoint = [0 0 0];
gazePoint0 = PlaneLineIntersecPoint(screenVector, screenPoint, gazeAbsolute0, EyeBallCenter0);
gazePoint1 = PlaneLineIntersecPoint(screenVector, screenPoint, gazeAbsolute1, EyeBallCenter1);
gazePoint = (gazePoint0 + gazePoint1) / 2

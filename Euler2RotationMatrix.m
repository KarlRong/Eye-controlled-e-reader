function rotation_matrix = Euler2RotationMatrix(eulerAngles)
%     s1 = sin(eulerAngles(1));
%     s2 = sin(eulerAngles(2));
%     s3 = sin(eulerAngles(3));
% 
%     c1 = cos(eulerAngles(1));
%     c2 = cos(eulerAngles(2));
%     c3 = cos(eulerAngles(3));
% 
%     rotation_matrix = zeros(3,3);
%     rotation_matrix(1, 1) = c2 * c3;
%     rotation_matrix(1, 2) = -c2 *s3;
%     rotation_matrix(1, 3) = s2;
%     rotation_matrix(2, 1) = c1 * s3 + c3 * s1 * s2;
%     rotation_matrix(2, 2) = c1 * c3 - s1 * s2 * s3;
%     rotation_matrix(2, 3) = -c2 * s1;
%     rotation_matrix(3, 1) = s1 * s3 - c1 * c3 * s2;
%     rotation_matrix(3, 2) = c3 * s1 + c1 * s2 * s3;
%     rotation_matrix(3, 3) = c1 * c2
%     [x, y, z] = dcm2angle(rotation_matrix, 'XYZ');
%     a = [x, y, z]
%     Rx = [1 0 0; 0 cos(eulerAngles(1)) -sin(eulerAngles(1)); 0 sin(eulerAngles(1)) cos(eulerAngles(1))];
%     Ry = [cos(eulerAngles(2)) 0 sin(eulerAngles(2)); 0 1 0; -sin(eulerAngles(2)) 0 cos(eulerAngles(2))];
%     Rz = [cos(eulerAngles(3)) -sin(eulerAngles(3)) 0;sin(eulerAngles(3)) cos(eulerAngles(3)) 0; 0 0 1];
%     rotation_matrix = Rx * Ry * Rz
%     [x, y, z] = dcm2angle(rotation_matrix, 'XYZ');
%     a = [x, y, z]
    rotation_matrix = angle2dcm(eulerAngles(1), eulerAngles(2), eulerAngles(3), 'XYZ');
    rotation_matrix = rotation_matrix';
end


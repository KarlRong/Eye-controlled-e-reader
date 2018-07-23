function intersectPoint = PlaneLineIntersecPoint(planeVector, planePoint, lineVector, linePoint)

    vp1 = planeVector(1);
    vp2 = planeVector(2);
    vp3 = planeVector(3);
    n1 = planePoint(1);
    n2 = planePoint(2);
    n3 = planePoint(3);
    v1 = lineVector(1);
    v2 = lineVector(2);
    v3 = lineVector(3);
    m1 = linePoint(1);
    m2 = linePoint(2);
    m3 = linePoint(3);
    vpt = v1 * vp1 + v2 * vp2 + v3 * vp3;

    if vpt == 0
        intersectPoint = NULL;
    else
        t = ((n1 - m1) * vp1 + (n2 - m2) * vp2 + (n3 - m3) * vp3) / vpt;
        intersectPoint(1) = m1 + v1 * t;
        intersectPoint(2) = m2 + v2 * t;
        intersectPoint(3) = m3 + v3 * t;
    end
end


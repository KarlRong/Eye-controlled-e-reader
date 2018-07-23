function intersected = RaySphereIntersect(rayOrigin, rayDir, sphereOrigin, sphereRadius)

	dx = rayDir(1);
	dy = rayDir(2);
	dz = rayDir(3);
	x0 = rayOrigin(1);
	y0 = rayOrigin(2);
	z0 = rayOrigin(3);
	cx = sphereOrigin(1);
	cy = sphereOrigin(2);
	cz = sphereOrigin(3);
	r = sphereRadius;

	a = dx*dx + dy*dy + dz*dz;
	b = 2*dx*(x0-cx) + 2*dy*(y0-cy) + 2*dz*(z0-cz);
	c = cx*cx + cy*cy + cz*cz + x0*x0 + y0*y0 + z0*z0 + -2*(cx*x0 + cy*y0 + cz*z0) - r*r;

	disc = b*b - 4*a*c;

	t = (-b - sqrt(b*b - 4*a*c))/2*a;

    if disc < 0
		intersected = [0, 0, -1]; 
    else
	intersected = rayOrigin + rayDir * t;
    end
end


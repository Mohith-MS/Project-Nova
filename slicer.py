import math
import copy
# import numpy as np
import sys
import time

bedWidth = 150.0
extrudeWidth = 0.71
supportInfill = .5
delta = extrudeWidth / 100.0


class Point:
    def __init__(self, x_, y_, z_):
        self.x = x_
        self.y = y_
        self.z = z_

    def dotProduct(self, p):
        return self.x * p.x + self.y * p.y + self.z * p.z

    def normalize(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def toString(self):
        return "Point(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def equals(self, p2):
        if close(self.x, p2.x) and close(self.y, p2.y) and close(self.z, p2.z):
            return True
        else:
            return False


def close(f1, f2):
    comp = (max(f1, f2) - min(f1, f2))
    return (comp > -delta) and (comp < delta)


def pointInLine(p, line):
    if close(p.x, line.p0.x) and close(p.y, line.p0.y) and close(p.z, line.p0.z):
        return True
    elif close(p.x, line.p1.x) and close(p.y, line.p1.y) and close(p.z, line.p1.z):
        return True
    else:
        return False


class Line:
    def __init__(self, p0_, p1_):
        self.p0 = p0_
        self.p1 = p1_

    def toString(self):
        return "Line(" + self.p0.toString() + "," + self.p1.toString() + ")"

    def reverse(self):
        x_ = copy.copy(self.p0.x)
        y_ = copy.copy(self.p0.y)
        z_ = copy.copy(self.p0.z)
        self.p0.x = copy.copy(self.p1.x)
        self.p0.y = copy.copy(self.p1.y)
        self.p0.z = copy.copy(self.p1.z)
        self.p1.x = x_
        self.p1.y = y_
        self.p1.z = z_
        return self


def lineEqual(l1, l2):
    if ((close(l1.p0.x, l2.p0.x) and close(l1.p0.y, l2.p0.y) and
         close(l1.p1.x, l2.p1.x) and close(l1.p1.y, l2.p1.y)) or
            (close(l1.p0.x, l2.p1.x) and close(l1.p0.y, l2.p1.y) and
             close(l1.p1.x, l2.p0.x) and close(l1.p1.y, l2.p0.y))):
        return True
    else:
        return False


class Triangle:
    def __init__(self, p0_, p1_, p2_, norm_):
        self.p0 = p0_
        self.p1 = p1_
        self.p2 = p2_
        self.norm = norm_

    def toString(self):
        return "Triangle(" + self.p0.toString() + "," + self.p1.toString() + "," + self.p2.toString() + ")"


def triangleEqual(t1, t2):
    if ((t1.p0.equals(t2.p0) and t1.p1.equals(t2.p1) and t1.p2.equals(t2.p2))
            or (t1.p0.equals(t2.p0) and t1.p1.equals(t2.p2) and t1.p2.equals(t2.p1))
            or (t1.p0.equals(t2.p1) and t1.p1.equals(t2.p0) and t1.p2.equals(t2.p2))
            or (t1.p0.equals(t2.p1) and t1.p1.equals(t2.p2) and t1.p2.equals(t2.p0))
            or (t1.p0.equals(t2.p2) and t1.p1.equals(t2.p0) and t1.p2.equals(t2.p1))
            or (t1.p0.equals(t2.p2) and t1.p1.equals(t2.p1) and t1.p2.equals(t2.p0))):
        return True
    else:
        return False


class Slice:
    def __init__(self, zValue_, perimeter_, isSurface_):
        self.zValue = zValue_
        self.perimeter = perimeter_
        self.isSurface = isSurface_
        self.support = list()
        self.infill = list()


def fileToTriangles(coordinates):
    triangles = list()
    points = list()
    for value in coordinates:
        points.insert(0, Point(value[3], value[4], value[5]))
        points.insert(0, Point(value[6], value[7], value[8]))
        points.insert(0, Point(value[9], value[10], value[11]))
        points.insert(0, Point(value[0], value[1], value[2]))
        while points:
            triangles.insert(0, Triangle(points[0], points[1], points[2], points[3]))
            points = points[4:]

    return triangles


def intersectSlice(line, plane):
    if line.p0.z == line.p1.z and line.p1.z == plane:
        return line.p0
    elif line.p0.z == line.p1.z:
        return None
    else:
        slope = Point(x_=line.p1.x-line.p0.x, y_=line.p1.y-line.p0.y, z_=line.p1.z-line.p0.z)
        t = float(plane-line.p0.z)/float(slope.z)

        if 0 <= t <= 1:
            testZ = line.p0.z+t*slope.z
            if max(line.p0.z, line.p1.z) >= testZ >= min(line.p0.z, line.p1.z):
                return Point(x_=line.p0.x+t*slope.x, y_=line.p0.y+t*slope.y, z_=line.p0.z+t*slope.z)

            else:
                return None
        else:
            return None


def sign(p1, p2, p3):
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)


"""
def aboveTriangle(point, triangle):
    if (point.z > (triangle.p0.z - delta) and
            point.z > (triangle.p1.z - delta) and
            point.z > (triangle.p2.z - delta)):

        b1 = (sign(point, triangle.p0, triangle.p1) < 0.0)
        b2 = (sign(point, triangle.p1, triangle.p2) < 0.0)
        b3 = (sign(point, triangle.p2, triangle.p0) < 0.0)
        ret = ((b1 == b2) and (b2 == b3))
        return ret

    else:
        return False
"""


def findBoundaries(triangles):
    bottomZ = 500
    topZ = -500

    for triangle in triangles:
        maximum = max(triangle.p0.z, triangle.p1.z, triangle.p2.z)
        minimum = min(triangle.p0.z, triangle.p1.z, triangle.p2.z)

        if maximum > topZ:
            topZ = maximum
        if minimum < bottomZ:
            bottomZ = minimum

    return bottomZ, topZ


def separateSlices(triangles, layerThickness=0.1):
    bounds = findBoundaries(triangles)
    numSlices = int((bounds[1] - bounds[0]) / layerThickness)
    slices = [bounds[0] + z * layerThickness for z in range(0, numSlices + 1)]
    segments = list()
    current_z = 0
    for s in slices:
        current_z += 1
        currentSegment = list()
        currentSegmentSurface = False
        sys.stdout.write("\r")
        sys.stdout.write(str((current_z / len(slices)) * 100))
        for triangle in triangles:
            point1 = intersectSlice(Line(p0_=triangle.p0, p1_=triangle.p1), s)
            point2 = intersectSlice(Line(p0_=triangle.p1, p1_=triangle.p2), s)
            point3 = intersectSlice(Line(p0_=triangle.p2, p1_=triangle.p0), s)

            points_ = list({point1, point2, point3})
            points = list()

            for point in points_:
                if point is None:
                    points_.remove(None)
                    break

            for i in range(0, len(points_)):
                j = i + 1
                unique = True
                while j < len(points_):
                    if points_[i].equals(points_[j]):
                        unique = False
                    j += 1
                if unique:
                    points.insert(0, copy.deepcopy(points_[i]))

            if s <= (bounds[0] + layerThickness) or s >= (bounds[1] - layerThickness):
                currentSegmentSurface = True

            # if len(points) == 1:
            # currentSegment.append(Line(points[0], points[0]))
            if len(points) == 2:
                currentSegment.append(Line(points[0], points[1]))
            elif len(points) == 3:
                segment1 = Line(points[0], points[1])
                segment2 = Line(points[1], points[2])
                segment3 = Line(points[2], points[0])
                currentSegmentSurface = True

                currentSegment.append(segment1)
                currentSegment.append(segment2)
                currentSegment.append(segment3)

        segments.append(Slice(zValue_=s, perimeter_=copy.deepcopy(currentSegment), isSurface_=currentSegmentSurface))
        '''
        for line in currentSegment:
            print("appended "+line.toString())
        '''
    return segments


def separateSlicess(triangles_asc, triangles_desc):
    bounds = findBoundaries(triangles_asc)
    # numSlices = int((bounds[1] - bounds[0]) / layerThickness)
    # slices = [bounds[0] + z * layerThickness for z in range(0, numSlices + 1)]
    segments = list()
    current_z = bounds[0]
    heights = []
    slice_number = []
    sys.stdout.write("0")
    while current_z <= bounds[1]:
        slice_number.append(current_z)
        done = current_z - bounds[0]
        total = bounds[1] - bounds[0]
        sys.stdout.write("\r")
        sys.stdout.write(str((done/total)*100))
        currentSegment = list()
        currentSegmentSurface = False
        layer_height = 0.1
        slopes = list()
        shortlist = ten_per(triangles_asc, triangles_desc, total/10, current_z)
        for triangle in shortlist:
            point1 = intersectSlice(Line(p0_=triangle.p0, p1_=triangle.p1), current_z)
            point2 = intersectSlice(Line(p0_=triangle.p1, p1_=triangle.p2), current_z)
            point3 = intersectSlice(Line(p0_=triangle.p2, p1_=triangle.p0), current_z)

            points_ = list({point1, point2, point3})
            points = list()
            # tan_theta = list({t1, t2, t3})

            for point in points_:
                if point is None:
                    points_.remove(None)
                    break
                # else:
                #    print(point.toString())
            """
            for angle in tan_theta:
                if angle is None:
                    tan_theta.remove(None)
                    break
            """
            for i in range(0, len(points_)):
                j = i + 1
                unique = True
                while j < len(points_):
                    if points_[i].equals(points_[j]):
                        unique = False
                    j += 1
                if unique:
                    points.insert(0, copy.deepcopy(points_[i]))
                    # slopes.insert(0, copy.deepcopy(tan_theta[i]))

            if len(points) == 2:
                currentSegment.append(Line(points[0], points[1]))
            elif len(points) == 3:
                segment1 = Line(points[0], points[1])
                segment2 = Line(points[1], points[2])
                segment3 = Line(points[2], points[0])
                currentSegmentSurface = True

                currentSegment.append(segment1)
                currentSegment.append(segment2)
                currentSegment.append(segment3)

        """
        lowest = min(slopes)
        if 0 <= lowest < 0.839:
            layer_height = 0.1
            heights.append("red")  # np.array([255, 0, 0, 255]))
        elif 0.839 <= lowest < 1.73:
            layer_height = 0.2
            heights.append("orange")  # np.array([255, 127, 0, 255]))
            heights.append("orange")  # np.array([255, 127, 0, 255]))
        elif 1.73 <= lowest <= math.inf:
            layer_height = 0.3
            heights.append("yellow")  # np.array([255, 255, 0, 255]))
            heights.append("yellow")  # np.array([255, 255, 0, 255]))
            heights.append("yellow")  # np.array([255, 255, 0, 255]))
        """
        # if current_z <= (bounds[0] + layer_height) or current_z >= (bounds[1] - layer_height):
        #        currentSegmentSurface = True
        segments.append(Slice(zValue_=current_z, perimeter_=copy.deepcopy(currentSegment),
                              isSurface_=currentSegmentSurface))
        current_z += layer_height
    return segments, heights, slice_number


def ten_per(triangles_asc, triangles_desc, total, current_z):
    slot = int(math.floor(current_z / total))
    no_of_triangles = int(len(triangles_asc) / 10)
    a = slot * no_of_triangles
    b = (slot + 1) * no_of_triangles
    point1 = intersectSlice(Line(p0_=triangles_asc[b + 1].p0, p1_=triangles_asc[b + 1].p1), current_z)
    point2 = intersectSlice(Line(p0_=triangles_asc[b + 1].p1, p1_=triangles_asc[b + 1].p2), current_z)
    point3 = intersectSlice(Line(p0_=triangles_asc[b + 1].p2, p1_=triangles_asc[b + 1].p0), current_z)
    while point1 is None and point2 is None and point3 is None:
        b += no_of_triangles
        if b >= len(triangles_asc):
            b = len(triangles_asc) - 1
            break
        else:
            point1 = intersectSlice(Line(p0_=triangles_asc[b + 1].p0, p1_=triangles_asc[b + 1].p1), current_z)
            point2 = intersectSlice(Line(p0_=triangles_asc[b + 1].p1, p1_=triangles_asc[b + 1].p2), current_z)
            point3 = intersectSlice(Line(p0_=triangles_asc[b + 1].p2, p1_=triangles_asc[b + 1].p0), current_z)

    point1 = intersectSlice(Line(p0_=triangles_asc[a - 1].p0, p1_=triangles_asc[a - 1].p1), current_z)
    point2 = intersectSlice(Line(p0_=triangles_asc[a - 1].p1, p1_=triangles_asc[a - 1].p2), current_z)
    point3 = intersectSlice(Line(p0_=triangles_asc[a - 1].p2, p1_=triangles_asc[a - 1].p0), current_z)
    while point1 is None and point2 is None and point3 is None:
        a -= no_of_triangles
        if a <= 0:
            a = 0
            break
        else:
            point1 = intersectSlice(Line(p0_=triangles_asc[a - 1].p0, p1_=triangles_asc[a - 1].p1), current_z)
            point2 = intersectSlice(Line(p0_=triangles_asc[a - 1].p1, p1_=triangles_asc[a - 1].p2), current_z)
            point3 = intersectSlice(Line(p0_=triangles_asc[a - 1].p2, p1_=triangles_asc[a - 1].p0), current_z)

    asc_tris = triangles_asc[a:b+1]
    a = slot * no_of_triangles
    b = (slot + 1) * no_of_triangles
    point1 = intersectSlice(Line(p0_=triangles_desc[b + 1].p0, p1_=triangles_desc[b + 1].p1), current_z)
    point2 = intersectSlice(Line(p0_=triangles_desc[b + 1].p1, p1_=triangles_desc[b + 1].p2), current_z)
    point3 = intersectSlice(Line(p0_=triangles_desc[b + 1].p2, p1_=triangles_desc[b + 1].p0), current_z)
    while point1 is None and point2 is None and point3 is None:
        b += no_of_triangles
        if b >= len(triangles_asc):
            b = len(triangles_asc) - 1
            break
        else:
            point1 = intersectSlice(Line(p0_=triangles_desc[b + 1].p0, p1_=triangles_desc[b + 1].p1), current_z)
            point2 = intersectSlice(Line(p0_=triangles_desc[b + 1].p1, p1_=triangles_desc[b + 1].p2), current_z)
            point3 = intersectSlice(Line(p0_=triangles_desc[b + 1].p2, p1_=triangles_desc[b + 1].p0), current_z)
    point1 = intersectSlice(Line(p0_=triangles_desc[a - 1].p0, p1_=triangles_desc[a - 1].p1), current_z)
    point2 = intersectSlice(Line(p0_=triangles_desc[a - 1].p1, p1_=triangles_desc[a - 1].p2), current_z)
    point3 = intersectSlice(Line(p0_=triangles_desc[a - 1].p2, p1_=triangles_desc[a - 1].p0), current_z)
    while point1 is None and point2 is None and point3 is None:
        a -= no_of_triangles
        if a <= 0:
            a = 0
            break
        else:
            point1 = intersectSlice(Line(p0_=triangles_desc[a - 1].p0, p1_=triangles_desc[a - 1].p1), current_z)
            point2 = intersectSlice(Line(p0_=triangles_desc[a - 1].p1, p1_=triangles_desc[a - 1].p2), current_z)
            point3 = intersectSlice(Line(p0_=triangles_desc[a - 1].p2, p1_=triangles_desc[a - 1].p0), current_z)
    desc_tris = triangles_desc[a:b+1]
    return asc_tris + desc_tris


def intersection(L1, L2):
    x1 = L1.p0.x
    y1 = L1.p0.y
    x2 = L1.p1.x
    y2 = L1.p1.y
    x3 = L2.p0.x
    y3 = L2.p0.y
    x4 = L2.p1.x
    y4 = L2.p1.y

    xnum = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    xden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    ynum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    yden = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # noinspection PyBroadException
    try:
        intersect = Point(xnum / xden, ynum / yden, L1.p0.z)

        if ((intersect.x >= min(x1, x2) - delta) and (intersect.x <= max(x1, x2) + delta) and
                (intersect.y >= min(y1, y2) - delta) and (intersect.y <= max(y1, y2) + delta) and
                (intersect.x >= min(x3, x4) - delta) and (intersect.x <= max(x3, x4) + delta) and
                (intersect.y >= min(y3, y4) - delta) and (intersect.y <= max(y3, y4) + delta)):
            return intersect
        else:
            return None
    except:
        return None


"""
def infill(perimeter, percent):
    assert (percent >= 0)
    assert (percent <= 1)

    if len(perimeter) == 0:
        return []
    Z = perimeter[0].p0.z

    numLines = int(round((bedWidth * percent) / extrudeWidth))
    gap = bedWidth / numLines
    infill_ = []

    for x in range(numLines):
        fullLine = Line(Point((bedWidth / -2) + (x * gap), bedWidth / -2, Z),
                        Point((bedWidth / -2) + (x * gap), bedWidth / 2, Z))
        inters = []

        for line in perimeter:
            sect = intersection(line, fullLine)
            if sect is not None:
                new = True
                for i in inters:
                    if close(i.y, sect.y):
                        new = False
                if new:
                    inters.append(copy.deepcopy(sect))

        inters.sort(key=lambda point: point.y)

        if len(inters) % 2 == 0:
            for i in range(len(inters)):
                if i % 2 != 0:
                    overlap = False
                    newLine = Line(inters[i - 1], inters[i])
                    for l in perimeter:
                        if lineEqual(l, newLine):
                            overlap = True
                    if not overlap:
                        infill_.append(newLine)
    return infill_


def findNextPoint(point, lines):
    for i in range(0, len(lines)):
        line = lines[i]
        if pointInLine(point, line):
            return i
    return None



def cleanPerimeter(s):
    setPerimeter = copy.deepcopy(s.perimeter)
    i = 0
    while i < len(setPerimeter):
        j = i + 1
        while j < len(setPerimeter):
            if lineEqual(setPerimeter[i], setPerimeter[j]):
                setPerimeter.remove(setPerimeter[j])
            else:
                j += 1
        i += 1

    finalPerimeter = setPerimeter
    return Slice(zValue_=s.zValue, perimeter_=finalPerimeter, isSurface_=s.isSurface)



def brim(base, numOutlines, offset):
    cx = 1
    cy = 1
    area = 1
    for line in base:
        cx = cx * (line.p0.x + line.p1.x)
        cy = cy * (line.p0.y + line.p1.y)
        area *= (line.p0.x * line.p1.y - line.p1.x * line.p0.y)
    area = area / 2
    cx = cx / (6 * area)
    cy = cy / (6 * area)

    brimlines = list()
    for i in range(1, numOutlines + 1):
        for line in base:
            line_ = Line(Point(line.p0.x, line.p0.y, line.p0.z), Point(line.p1.x, line.p1.y, line.p1.z))

            if line.p0.x > cx:
                line_.p0.x += offset + extrudeWidth * i
            else:
                line_.p0.x -= offset + extrudeWidth * i
            if line.p0.y > cy:
                line_.p0.y += offset + extrudeWidth * i
            else:
                line_.p0.y -= offset + extrudeWidth * i
            if line.p1.x > cx:
                line_.p1.x += offset + extrudeWidth * i
            else:
                line_.p1.x -= offset + extrudeWidth * i
            if line.p1.y > cy:
                line_.p1.y += offset + extrudeWidth * i
            else:
                line_.p1.y -= offset + extrudeWidth * i
            brimlines.append(line_)

    return brimlines


def downward(triangles):
    trianglesDown = list()
    for triangle in triangles:
        if triangle.norm.z < 0:
            trianglesDown.insert(0, copy.deepcopy(triangle))
    return trianglesDown


def supportNeeded(triangle, triangles, bottomZ):
    if (close(triangle.p0.z, bottomZ)
            and close(triangle.p1.z, bottomZ)
            and close(triangle.p2.z, bottomZ)):
        return False

    for tri in triangles:
        if (aboveTriangle(triangle.p0, tri)
                or aboveTriangle(triangle.p1, tri)
                or aboveTriangle(triangle.p2, tri)):
            return False

    return True


def generateSupportShape(triangle, bottomZ):
    triangleTop = copy.deepcopy(triangle)
    triangleBottom = Triangle(Point(triangleTop.p0.x, triangleTop.p0.y, bottomZ),
                              Point(triangleTop.p1.x, triangleTop.p1.y, bottomZ),
                              Point(triangleTop.p2.x, triangleTop.p2.y, bottomZ), None)
    newShape = [triangleTop]
    newShape.insert(0, triangleBottom)

    newShape.insert(0, Triangle(triangleTop.p0, triangleTop.p1, triangleBottom.p0, None))
    newShape.insert(0, Triangle(triangleTop.p1, triangleTop.p2, triangleBottom.p1, None))
    newShape.insert(0, Triangle(triangleTop.p2, triangleTop.p0, triangleBottom.p2, None))
    newShape.insert(0, Triangle(triangleBottom.p0, triangleBottom.p1, triangleTop.p1, None))
    newShape.insert(0, Triangle(triangleBottom.p1, triangleBottom.p2, triangleTop.p2, None))
    newShape.insert(0, Triangle(triangleBottom.p2, triangleBottom.p0, triangleTop.p0, None))

    i = 0
    while i < len(newShape):
        j = i + 1
        while j < len(newShape):
            if triangleEqual(newShape[i], newShape[j]):
                newShape.remove(newShape[j])
            else:
                j += 1
        i += 1

    return newShape

def generateSupports(triangles, layerThickness):
    bounds = findBoundaries(triangles)

    trianglesDown = downward(triangles)

    trianglesForSupport = list()
    for tri in trianglesDown:
        if supportNeeded(tri, triangles, bounds[0]):
            trianglesForSupport.insert(0, copy.deepcopy(tri))

    supportShapes = list()
    for triangle in trianglesForSupport:
        supportShapes.insert(0, generateSupportShape(triangle, bounds[0]))

    supportSlices = list()

    for shape in supportShapes:
        supportSlices.insert(0, separateSlices(shape, layerThickness))

    return supportSlices


def writeGcode(slices, filename):
    extrudeRate = 0.05
    f = open(filename[:-3] + "gcode", 'w')
    f.write(";Start GCode\n")
    f.write("M109 S210.000000\n")
    f.write("G28 X0 Y0 Z0\n")
    f.write("G92 E0\n")
    f.write("G29\n")

    o = bedWidth / 2
    layer = 1
    E = 0
    for s in slices:

        f.write(";Layer " + str(layer) + " of " + str(len(slices)) + "\n")

        if layer == 2:
            f.write("M106 S127\n")
        if layer == 3:
            f.write("M106 S255\n")

        f.write(";perimeter\n")
        for l in s.perimeter:
            f.write("G0 F2700 X" + str(o + l.p0.x) + " Y" + str(o + l.p0.y) + " Z" + str(l.p0.z) + "\n")
            dist = math.sqrt(pow(l.p1.x - l.p0.x, 2) + pow(l.p1.y - l.p0.y, 2))
            E += dist * extrudeRate
            f.write("G1 F900 X" + str(o + l.p1.x) + " Y" + str(o + l.p1.y) + " E" + str(E) + "\n")

        if len(s.support) > 0:
            f.write(";support\n")
        for l in s.support:

            f.write("G0 F2700 X" + str(o + l.p0.x) + " Y" + str(o + l.p0.y) + " Z" + str(l.p0.z) + "\n")
            dist = math.sqrt(pow(l.p1.x - l.p0.x, 2) + pow(l.p1.y - l.p0.y, 2))
            E += dist * extrudeRate
            f.write("G1 F800 X" + str(o + l.p1.x) + " Y" + str(o + l.p1.y) + " E" + str(E) + "\n")

        if len(s.infill) > 0:
            f.write(";infill\n")
        for l in s.infill:
            f.write("G0 F2700 X" + str(o + l.p0.x) + " Y" + str(o + l.p0.y) + " Z" + str(l.p0.z) + "\n")
            dist = math.sqrt(pow(l.p1.x - l.p0.x, 2) + pow(l.p1.y - l.p0.y, 2))
            E += dist * extrudeRate
            f.write("G1 F900 X" + str(o + l.p1.x) + " Y" + str(o + l.p1.y) + " E" + str(E) + "\n")

        layer += 1

    f.write(";End GCode\n")
    f.write("M104 S0\n")
    f.write("M140 S0\n")
    f.write("G91\n")
    f.write("G1 E-1 F300\n")
    f.write("G1 Z+0.5 E-5 X-20 Y-20 F2v700\n")
    f.write("G28 X0 Y0\n")
    f.write("M84\n")
    f.write("G90\n")
"""


def slice_model(coords, rev_coords):
    # filename = sys.argv[1]
    # layerThickness = float(sys.argv[2])
    # infillPercent = float(sys.argv[3])
    triangles_asc = fileToTriangles(coords)
    triangles_desc = fileToTriangles(rev_coords)
    #slices_, heights, number = separateSlices(triangles_asc, triangles_desc)
    t1 = time.time()
    print("start time: ", t1)
    segments = separateSlices(triangles_asc)
    t2 = time.time()
    print("\ntime elapsed: ", t2 - t1)
    print("starting optimised slicing")
    t3 = time.time()
    slices_, heights, number = separateSlicess(triangles_asc, triangles_desc)
    t4 = time.time()
    print("\ntime elapsed: ", t4 - t3)
    # supportSlices = generateSupports(triangles, layerThickness)

    # slices = list()

    # for s in slices_:
    # slices += [cleanPerimeter(s)]

    """
    for s in slices:
        if s.isSurface:
            s.infill = infill(s.perimeter, 1)
        else:
            s.infill = infill(s.perimeter, infillPercent)

    for shape in supportSlices:
        for s in range(len(shape)):
            slices[s].support += infill(shape[s].perimeter, supportInfill)

    #writeGcode(slices, filename)
    """
    # return heights, number
    return [], segments

import sys
import time
import math
import itertools
from collections import Counter
import random
import os
import struct
# noinspection PyPackageRequirements
from stl.mesh import Mesh


class TakeFile:

    def __int__(self):
        return None

    @staticmethod
    def load(file):
        mesh = Mesh.from_file(file)
        return mesh

    def loadMesh(self, input_file):
        filetype = os.path.splitext(input_file)[1].lower()
        if filetype == ".stl":
            f = open(input_file, "rb")
            if "solid" in str(f.read(5).lower()):
                f = open(input_file, "r")
                objs = [{"Mesh": self.loadAsciiSTL(f)}]
                if len(objs[0]["Mesh"]) < 3:
                    f.seek(5, os.SEEK_SET)
                    objs = [{"Mesh": self.loadBinarySTL(f)}]
            else:
                objs = [{"Mesh": self.loadBinarySTL(f)}]

        else:
            print("File type is not supported.")
            sys.exit()

        return objs

    @staticmethod
    def loadAsciiSTL(f):
        mesh = list()
        for line in f:
            if "vertex" in line:
                data = line.split()[1:]
                mesh.append([float(data[0]), float(data[1]), float(data[2])])
        return mesh

    @staticmethod
    def loadBinarySTL(f):
        f.read(80 - 5)
        face_count = struct.unpack('<I', f.read(4))[0]
        mesh = list()
        for idx in range(0, face_count):
            data = struct.unpack("<ffffffffffffH", f.read(50))
            mesh.append([data[3], data[4], data[5]])
            mesh.append([data[6], data[7], data[8]])
            mesh.append([data[9], data[10], data[11]])
        return mesh

    def rotate_mesh(self, r, content):
        face = []
        mesh = []
        i = 0
        rotated_content = list(map(self.rotate_vert, content, [r] * len(content)))

        for li in rotated_content:
            face.append(li)
            i += 1
            if i % 3 == 0:
                mesh.append([face[0], face[1], face[2]])
                face = []

        mesh = map(self.calculate_normal, mesh)
        tweaked = list("solid a\n")
        temp = list(map(self.write_facett, mesh))
        for i in temp:
            tweaked.append("   facet normal {} {} {}\n".format(i[0], i[1], i[2]))
            tweaked.append("      outer loop\n")
            tweaked.append("         vertex {} {} {}\n".format(i[3], i[4], i[5]))
            tweaked.append("         vertex {} {} {}\n".format(i[6], i[7], i[8]))
            tweaked.append("         vertex {} {} {}\n".format(i[9], i[10], i[11]))
            tweaked.append("      endloop\n")
            tweaked.append("   endfacet\n")
        tweaked.append("endsolid")
        tweaked = "".join(tweaked)
        f = open("a.stl", 'w')
        f.write(tweaked)
        f.close()
        return tweaked

    @staticmethod
    def rotate_vert(content, r):
        return [content[0] * r[0][0] + content[1] * r[1][0] + content[2] * r[2][0],
                content[0] * r[0][1] + content[1] * r[1][1] + content[2] * r[2][1],
                content[0] * r[0][2] + content[1] * r[1][2] + content[2] * r[2][2]]

    @staticmethod
    def calculate_normal(face):
        v = [face[1][0] - face[0][0], face[1][1] - face[0][1], face[1][2] - face[0][2]]
        w = [face[2][0] - face[0][0], face[2][1] - face[0][1], face[2][2] - face[0][2]]
        a = [v[1] * w[2] - v[2] * w[1], v[2] * w[0] - v[0] * w[2], v[0] * w[1] - v[1] * w[0]]
        return [[a[0], a[1], a[2]], face[0], face[1], face[2]]

    @staticmethod
    def write_facett(facett):
        return (facett[0][0], facett[0][1], facett[0][2], facett[1][0],
                facett[1][1], facett[1][2], facett[2][0], facett[2][1],
                facett[2][2], facett[3][0], facett[3][1], facett[3][2])


class Tweak:
    def __init__(self, mesh, critical_angle=None):
        if critical_angle is None:
            critical_angle = 45
        content = self.arrange_mesh(mesh)
        amin = self.approach_first_vertex(content)
        bottom_a, overhang_a, line_l = self.lithograph(content=content, n=[0.0, 0.0, 1.0], amin=amin,
                                                       critical_angle=critical_angle)
        list_e = [[[0.0, 0.0, 1.0], bottom_a, overhang_a, line_l]]
        orientations = self.area_cumulation(content)

        for side in orientations:
            orientation = [float("{:6f}".format(-i)) for i in side[0]]
            amin = self.approach_vertex(content, orientation)
            bottom_a, overhang_a, line_l = self.lithograph(content, orientation, amin, critical_angle)
            list_e.append([orientation, bottom_a, overhang_a, line_l])

        unprintablility = sys.maxsize
        best_side = 0
        for orientation, bottom_a, overhang_a, line_l in list_e:
            f = self.target_function(bottom_a, overhang_a, line_l)
            if f < unprintablility - 0.05:
                unprintablility = f
                best_side = [orientation, bottom_a, overhang_a, line_l]

        if best_side:
            [self.v, self.phi, self.r] = self.euler(best_side)

        self.unprintablility = unprintablility
        self.zn = best_side

    @staticmethod
    def target_function(touching, overhang, line):
        abs_limit = 100
        re_limit = 1
        line_factor = 0.5
        touching_line = line * line_factor
        f = (overhang / abs_limit) + (overhang / (touching + touching_line) / re_limit)
        ret = float("{:f}".format(f))
        return ret

    @staticmethod
    def arrange_mesh(mesh):
        face = []
        content = []
        i = 0
        for li in mesh:
            face.append(li)
            i += 1
            if i % 3 == 0:
                v = [face[1][0] - face[0][0], face[1][1] - face[0][1], face[1][2] - face[0][2]]
                w = [face[2][0] - face[0][0], face[2][1] - face[0][1], face[2][2] - face[0][2]]
                a = [round(v[1] * w[2] - v[2] * w[1], 6), round(v[2] * w[0] - v[0] * w[2], 6),
                     round(v[0] * w[1] - v[1] * w[0], 6)]
                content.append([a, face[0], face[1], face[2]])
                face = []
            time.sleep(0)
        return content

    @staticmethod
    def approach_first_vertex(content):
        amin = sys.maxsize
        for li in content:
            z = min([li[1][2], li[2][2], li[3][2]])
            if z < amin:
                amin = z
            time.sleep(0)
        return amin

    @staticmethod
    def approach_vertex(content, n):
        amin = sys.maxsize
        for li in content:
            a1 = li[1][0] * n[0] + li[1][1] * n[1] + li[1][2] * n[2]
            a2 = li[2][0] * n[0] + li[2][1] * n[1] + li[2][2] * n[2]
            a3 = li[3][0] * n[0] + li[3][1] * n[1] + li[3][2] * n[2]
            an = min([a1, a2, a3])
            if an < amin:
                amin = an
            time.sleep(0)
        return amin

    def lithograph(self, content, n, amin, critical_angle):
        overhang = 1
        alpha = -math.cos((90 - critical_angle) * math.pi / 180)
        bottom_a = 1
        line_l = 1
        touching_height = amin + 0.15

        anti_n = [float(-i) for i in n]

        for li in content:
            time.sleep(0)
            a = li[0]
            norma = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
            if norma < 2:
                continue
            if alpha > (a[0] * n[0] + a[1] * n[1] + a[2] * n[2]) / norma:
                a1 = li[1][0] * n[0] + li[1][1] * n[1] + li[1][2] * n[2]
                a2 = li[2][0] * n[0] + li[2][1] * n[1] + li[2][2] * n[2]
                a3 = li[3][0] * n[0] + li[3][1] * n[1] + li[3][2] * n[2]
                an = min([a1, a2, a3])

                ali = float("{:1.4f}".format(abs(li[0][0] * n[0] + li[0][1] * n[1] + li[0][2] * n[2]) / 2))
                if touching_height < an:
                    if 0.00001 < math.fabs(a[0] - anti_n[0]) + math.fabs(a[1] - anti_n[1]) + math.fabs(
                            a[2] - anti_n[2]):
                        ali = 0.8 * ali
                    overhang += ali
                else:
                    bottom_a += ali
                    line_l += self.get_touching_line([a1, a2, a3], li, touching_height)
                time.sleep(0)
        return bottom_a, overhang, line_l

    @staticmethod
    def get_touching_line(a, li, touching_height):
        touch_lst = list()
        for i in range(3):
            if a[i] < touching_height:
                touch_lst.append(li[1 + i])
        combs = list(itertools.combinations(touch_lst, 2))
        if len(combs) <= 1:
            return 0
        length = 0
        for p1, p2 in combs:
            time.sleep(0)
            length += math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
                                + (p2[2] - p1[2]) ** 2)
        return length

    @staticmethod
    def area_cumulation(content):
        best_n = 5
        orient = Counter()
        for li in content:
            an = li[0]
            a = math.sqrt(an[0] * an[0] + an[1] * an[1] + an[2] * an[2])

            if a > 0:
                an = [float("{:1.6f}".format(i / a, 6)) for i in an]
                orient[tuple(an)] += a

        time.sleep(0)
        top_n = orient.most_common(best_n)
        return [[[0.0, 0.0, 1.0], 0.0]] + [[list(el[0]), float("{:2f}".format(el[1]))] for el in top_n]

    @staticmethod
    def edge_plus_vertex(self, mesh, best_n):
        v_count = len(mesh)
        if v_count < 10000:
            it = 5
        elif v_count < 25000:
            it = 2
        else:
            it = 1
        self.mesh = mesh
        lst = map(self.calc_random_normal, list(range(v_count)) * it)
        lst = filter(lambda x: x is not None, lst)

        time.sleep(0)
        orient = Counter(lst)

        top_n = orient.most_common(best_n)
        top_n = filter(lambda x: x[1] > 2, top_n)

        return [[list(el[0]), el[1]] for el in top_n]

    def calc_random_normal(self, i):
        if i % 3 == 0:
            v = self.mesh[i]
            w = self.mesh[i + 1]
        elif i % 3 == 1:
            v = self.mesh[i]
            w = self.mesh[i + 1]
        else:
            v = self.mesh[i]
            w = self.mesh[i - 2]
        r_v = random.choice(self.mesh)
        v = [v[0] - r_v[0], v[1] - r_v[1], v[2] - r_v[2]]
        w = [w[0] - r_v[0], w[1] - r_v[1], w[2] - r_v[2]]
        a = [v[1] * w[2] - v[2] * w[1], v[2] * w[0] - v[0] * w[2], v[0] * w[1] - v[1] * w[0]]
        n = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
        if n != 0:
            return tuple([round(d / n, 6) for d in a])

    @staticmethod
    def euler(best_side):
        if best_side[0] == [0, 0, -1]:
            v = [1, 0, 0]
            phi = math.pi
        elif best_side[0] == [0, 0, 1]:
            v = [1, 0, 0]
            phi = 0
        else:
            phi = float("{:2f}".format(math.pi - math.acos(-best_side[0][2])))
            v = [-best_side[0][1], best_side[0][0], 0]
            v = [i / math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) for i in v]
            v = [float("{:2f}".format(i)) for i in v]

        r = [[v[0] * v[0] * (1 - math.cos(phi)) + math.cos(phi),
              v[0] * v[1] * (1 - math.cos(phi)) - v[2] * math.sin(phi),
              v[0] * v[2] * (1 - math.cos(phi)) + v[1] * math.sin(phi)],
             [v[1] * v[0] * (1 - math.cos(phi)) + v[2] * math.sin(phi),
              v[1] * v[1] * (1 - math.cos(phi)) + math.cos(phi),
              v[1] * v[2] * (1 - math.cos(phi)) - v[0] * math.sin(phi)],
             [v[2] * v[0] * (1 - math.cos(phi)) - v[1] * math.sin(phi),
              v[2] * v[1] * (1 - math.cos(phi)) + v[0] * math.sin(phi),
              v[2] * v[2] * (1 - math.cos(phi)) + math.cos(phi)]]
        r = [[float("{:2f}".format(val)) for val in row] for row in r]
        return v, phi, r

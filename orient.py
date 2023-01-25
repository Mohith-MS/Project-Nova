import sys
import time
import math
from collections import Counter
import os
import struct
import numpy as np
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

        asc_vert = list(map(lambda y: sorted(y, key=lambda o: o[2]), mesh))
        asc_sorted = sorted(asc_vert, key=lambda p: p[0][2])
        mesh = map(self.calculate_normal, asc_sorted)
        temp = list(map(self.write_facett, mesh))
        # print("num ", len(temp))
        flat = []
        for x in temp:
            flat += list(x)
        self.write_stl(temp, 'a')
        with open("Resources/temp/asc.txt", 'w') as in_file:
            for i in flat:
                in_file.write(str(i))
                in_file.write("\n")
        in_file.close()
        # print("me",len(flat))
        return flat  # , temp2

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

    @staticmethod
    def write_stl(coordinates, m):
        file = list("solid a\n")
        for i in coordinates:
            file.append("   facet normal {} {} {}\n".format(i[0], i[1], i[2]))
            file.append("      outer loop\n")
            file.append("         vertex {} {} {}\n".format(i[3], i[4], i[5]))
            file.append("         vertex {} {} {}\n".format(i[6], i[7], i[8]))
            file.append("         vertex {} {} {}\n".format(i[9], i[10], i[11]))
            file.append("      endloop\n")
            file.append("   endfacet\n")
        file.append("endsolid")
        file = "".join(file)
        f = open(f"Resources/temp/{m}.stl", 'w')
        f.write(file)
        f.close()


class Tweak:
    def __init__(self, mesh):
        self.OV_H = 1
        self.NEGL_FACE_SIZE = 0.4928696161029859
        self.TAR_A = 0.023251193283878126
        self.TAR_B = 0.17967732044591803
        self.RELATIVE_F = 11.250931864115714
        self.CONTOUR_F = 0.219523237806102
        self.BOTTOM_F = 0.219523237806102
        self.TAR_C = -0.016564249433447253
        self.TAR_D = 1.0592490333488807
        self.TAR_E = 0.011503545133447014
        self.FIRST_LAY_H = 0.04754881938390257
        self.VECTOR_TOL = -0.0008385913582234466
        self.ASCENT = -0.07809801382985776
        self.PLAFOND_ADV = 0.059937025927212395
        self.CONTOUR_AMOUNT = 0.018242751444131886
        self.height_offset = 2.574100894603089
        self.height_log = 0.04137517666768212
        self.height_log_k = 1.9325457851679673

        z_axis = -np.array([0, 0, 1], dtype=np.float64)
        orientations = [[z_axis, 0.0]]

        self.mesh = self.preprocess(content=mesh)
        orientations += self.area_cumulation(10)
        orientations += self.death_star(12)
        orientations += self.add_supplements()
        orientations = self.remove_duplicates(orientations)

        results = list()
        for side in orientations:
            orientation = -1 * np.array(side[0], dtype=np.float64)

            self.project_vertices(orientation)
            bottom, overhang, contour = self.calc_overhang(orientation)
            unprintability = self.target_function(bottom, overhang, contour)
            results.append([orientation, bottom, overhang, contour, unprintability])

        del self.mesh

        results = np.array(results)
        best_results = list(results[results[:, 4].argsort()])

        for i, align in enumerate(best_results):
            best_results[i] = list(best_results[i])
            v, phi, matrix = self.euler(align)
            best_results[i].append([[v[0], v[1], v[2]], phi, matrix])

        if len(best_results) > 0:
            self.euler_parameter = best_results[0][5][:2]
            self.r = best_results[0][5][2]
            self.alignment = best_results[0][0]
            self.bottom_area = best_results[0][1]
            self.overhang_area = best_results[0][2]
            self.contour = best_results[0][3]
            self.unprintability = best_results[0][4]
            self.best_5 = best_results

    def project_vertices(self, orientation):
        self.mesh[:, 4, 0] = np.inner(self.mesh[:, 1, :], orientation)
        self.mesh[:, 4, 1] = np.inner(self.mesh[:, 2, :], orientation)
        self.mesh[:, 4, 2] = np.inner(self.mesh[:, 3, :], orientation)

        self.mesh[:, 5, 1] = np.max(self.mesh[:, 4, :], axis=1)
        self.mesh[:, 5, 2] = np.median(self.mesh[:, 4, :], axis=1)
        time.sleep(0)

    def calc_overhang(self, orientation):
        total_min = np.amin(self.mesh[:, 4, :])

        bottom = np.sum(self.mesh[np.where(self.mesh[:, 5, 1] < total_min + self.FIRST_LAY_H), 5, 0])

        overhangs = self.mesh[np.where(np.inner(self.mesh[:, 0, :], orientation) < self.ASCENT)]
        overhangs = overhangs[np.where(overhangs[:, 5, 1] > (total_min + self.FIRST_LAY_H))]

        plafond = np.sum(overhangs[(overhangs[:, 0, :] == -orientation).all(axis=1), 5, 0])

        if len(overhangs) > 0:

            heights = np.inner(overhangs[:, 1:4, :].mean(axis=1), orientation) - total_min

            inner = np.inner(overhangs[:, 0, :], orientation) - self.ASCENT
            overhang = np.sum((self.height_offset + self.height_log * np.log(self.height_log_k * heights + 1)) *
                              overhangs[:, 5, 0] * np.abs(inner * (inner < 0)) ** self.OV_H)

            overhang -= self.PLAFOND_ADV * plafond

        else:
            overhang = 0

        contours = self.mesh[np.where(self.mesh[:, 5, 2] < total_min + self.FIRST_LAY_H)]

        if len(contours) > 0:
            conlen = np.arange(len(contours))
            sortsc0 = np.argsort(contours[:, 4, :], axis=1)[:, 0]
            sortsc1 = np.argsort(contours[:, 4, :], axis=1)[:, 1]

            con = np.array([np.subtract(
                contours[conlen, 1 + sortsc0, :],
                contours[conlen, 1 + sortsc1, :])])

            contours = np.sum(np.power(con, 2), axis=-1) ** 0.5
            contour = np.sum(contours) + self.CONTOUR_AMOUNT * len(contours)
        else:
            contour = 0

        time.sleep(0)
        return bottom, overhang, contour

    def target_function(self, bottom, overhang, contour):
        overhang /= 25
        return (self.TAR_A * (overhang + self.TAR_B) + self.RELATIVE_F * (overhang + self.TAR_C) /
                (self.TAR_D + self.CONTOUR_F * contour + self.BOTTOM_F * bottom + self.TAR_E * overhang))

    def preprocess(self, content):
        mesh = np.array(content, dtype=np.float64)
        if mesh.shape[1] == 3:
            row_number = int(len(content) / 3)
            mesh = mesh.reshape(row_number, 3, 3)
            v0 = mesh[:, 0, :]
            v1 = mesh[:, 1, :]
            v2 = mesh[:, 2, :]
            normals = np.cross(np.subtract(v1, v0), np.subtract(v2, v0)).reshape(row_number, 1, 3)
            mesh = np.hstack((normals, mesh))

        face_count = mesh.shape[0]

        addendum = np.zeros((face_count, 2, 3))
        addendum[:, 0, 0] = mesh[:, 1, 2]
        addendum[:, 0, 1] = mesh[:, 2, 2]
        addendum[:, 0, 2] = mesh[:, 3, 2]

        addendum[:, 1, 0] = np.sqrt(np.sum(np.square(mesh[:, 0, :]), axis=-1)).reshape(face_count)
        addendum[:, 1, 1] = np.max(mesh[:, 1:4, 2], axis=1)
        addendum[:, 1, 2] = np.median(mesh[:, 1:4, 2], axis=1)
        mesh = np.hstack((mesh, addendum))

        mesh = mesh[mesh[:, 5, 0] != 0]
        face_count = mesh.shape[0]

        mesh[:, 0, :] = mesh[:, 0, :] / mesh[:, 5, 0].reshape(face_count, 1)
        mesh[:, 5, 0] = mesh[:, 5, 0] / 2

        if self.NEGL_FACE_SIZE > 0:
            negl_size = [0.1 * x for x in [self.NEGL_FACE_SIZE]][0]
            filtered_mesh = mesh[np.where(mesh[:, 5, 0] > negl_size)]
            if len(filtered_mesh) > 100:
                mesh = filtered_mesh

        time.sleep(0)
        return mesh

    def area_cumulation(self, best_n):
        alignments = self.mesh[:, 0, :]
        orient = Counter()
        for index in range(len(self.mesh)):
            orient[tuple(alignments[index])] += self.mesh[index, 5, 0]

        top_n = orient.most_common(best_n)
        time.sleep(0)
        return top_n

    def death_star(self, best_n):
        mesh_len = len(self.mesh)
        iterations = int(np.ceil(20000 / (mesh_len + 100)))

        vertexes = self.mesh[:mesh_len, 1:4, :]
        tot_normalized_orientations = np.zeros((iterations * mesh_len + 1, 3))
        for i in range(iterations):
            two_vertexes = vertexes[:, np.random.choice(3, 2, replace=False)]
            vertex_0 = two_vertexes[:, 0, :]
            vertex_1 = two_vertexes[:, 1, :]

            vertex_2 = vertexes[(np.arange(mesh_len) * 127 + 8191 + i) % mesh_len, i % 3, :]
            normals = np.cross(np.subtract(vertex_2, vertex_0),
                               np.subtract(vertex_1, vertex_0))

            lengths = np.sqrt((normals * normals).sum(axis=1)).reshape(mesh_len, 1)

            with np.errstate(divide='ignore', invalid='ignore'):
                normalized_orientations = np.around(np.true_divide(normals, lengths),
                                                    decimals=6)

            tot_normalized_orientations[mesh_len * i:mesh_len * (i + 1)] = normalized_orientations
            time.sleep(0)

        orientations = np.inner(np.array([1, 1e3, 1e6]), tot_normalized_orientations)
        orient = Counter(orientations)
        top_n = orient.most_common(best_n)
        top_n = list(filter(lambda x: x[1] > 2, top_n))

        candidate = list()
        for sum_side, count in top_n:
            face_unique, face_count = np.unique(tot_normalized_orientations[orientations == sum_side], axis=0,
                                                return_counts=True)
            candidate += [[list(face_unique[i]), count] for i, count in enumerate(face_count)]

        candidate = list(filter(lambda x: x[1] >= 2, candidate))

        candidate += [[list((-v[0][0], -v[0][1], -v[0][2])), v[1]] for v in candidate]
        return candidate

    @staticmethod
    def add_supplements():
        v = [[0, 0, -1], [0.70710678, 0, -0.70710678], [0, 0.70710678, -0.70710678],
             [-0.70710678, 0, -0.70710678], [0, -0.70710678, -0.70710678],
             [1, 0, 0], [0.70710678, 0.70710678, 0], [0, 1, 0], [-0.70710678, 0.70710678, 0],
             [-1, 0, 0], [-0.70710678, -0.70710678, 0], [0, -1, 0], [0.70710678, -0.70710678, 0],
             [0.70710678, 0, 0.70710678], [0, 0.70710678, 0.70710678],
             [-0.70710678, 0, 0.70710678], [0, -0.70710678, 0.70710678], [0, 0, 1]]
        v = [[list([float(j) for j in i]), 0] for i in v]
        return v

    def euler(self, best_side):
        if np.allclose(best_side[0], np.array([0, 0, -1]), atol=abs(self.VECTOR_TOL)):
            rotation_axis = [1, 0, 0]
            phi = np.pi
        elif np.allclose(best_side[0], np.array([0, 0, 1]), atol=abs(self.VECTOR_TOL)):
            rotation_axis = [1, 0, 0]
            phi = 0
        else:
            phi = np.pi - np.arccos(-best_side[0][2])
            rotation_axis = [-best_side[0][1], best_side[0][0], 0]
            rotation_axis = [i / np.linalg.norm(rotation_axis) for i in rotation_axis]
        v = rotation_axis
        rotational_matrix = np.array([[v[0] * v[0] * (1 - math.cos(phi)) + math.cos(phi),
                                       v[0] * v[1] * (1 - math.cos(phi)) - v[2] * math.sin(phi),
                                       v[0] * v[2] * (1 - math.cos(phi)) + v[1] * math.sin(phi)],
                                      [v[1] * v[0] * (1 - math.cos(phi)) + v[2] * math.sin(phi),
                                       v[1] * v[1] * (1 - math.cos(phi)) + math.cos(phi),
                                       v[1] * v[2] * (1 - math.cos(phi)) - v[0] * math.sin(phi)],
                                      [v[2] * v[0] * (1 - math.cos(phi)) - v[1] * math.sin(phi),
                                       v[2] * v[1] * (1 - math.cos(phi)) + v[0] * math.sin(phi),
                                       v[2] * v[2] * (1 - math.cos(phi)) + math.cos(phi)]], dtype=np.float64)
        time.sleep(0)
        return rotation_axis, phi, rotational_matrix

    @staticmethod
    def remove_duplicates(old_orients):
        alpha = 5
        tol_angle = np.sin(alpha * np.pi / 180)
        orientations = list()
        for i in old_orients:
            duplicate = None
            for j in orientations:
                if np.allclose(i[0], j[0], atol=tol_angle):
                    duplicate = True
                    break
            if duplicate is None:
                orientations.append(i)
        return orientations

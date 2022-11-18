import os
import struct


class TakeFile:

    def __int__(self):
        return None

    def load(self, file):
        file_format = os.path.splitext(file)[1].lower()
        content = []
        if file_format.lower() == ".stl":
            if "solid" in str(file.read(5).lower()):
                file = open(file, "r")
                content = [{"Mesh": self.load_binary_stl(file)}]
                if len(content[0]["Mesh"]) < 3:
                    file.seek(5, os.SEEK_SET)
                    content = [{"Mesh": self.load_binary_stl(file)}]
            else:
                content = [{"Mesh": self.load_binary_stl(file)}]
        else:
            print("File type not supported. Please select '.stl' files only")

        return content

    @staticmethod
    def load_ascii_stl(file):
        mesh = list()
        for line in file:
            if "vertex" in line:
                data = line.split()[1:]
                mesh.append([float(data[0]), float(data[1]), float(data[2])])
        return mesh

    @staticmethod
    def load_binary_stl(file):
        file.read(80-5)
        face_count = struct.unpack('<I', file.read(50))[0]
        mesh = list()
        for i in range(0, face_count):
            data = struct.unpack("<ffffffffffffH", file.read(50))
            mesh.append([data[3], data[4], data[5]])
            mesh.append([data[6], data[7], data[8]])
            mesh.append([data[9], data[10], data[11]])
        return mesh

    def rotate_mesh(self, r, content, file):
        face = []
        mesh = []
        i = 0

        rotated_content = list(map(self.rotate_vert, content, [r]*len(content)))

        for li in rotated_content:
            face.append(li)
            i += 1
            if i % 3 == 0:
                mesh.append([face[0], face[1], face[2]])
                face = []

        mesh = map(self.calculate_normal, mesh)

        tweaked = list("solid %s" % file)
        tweaked += list(map(self.write_facett, mesh))
        tweaked.append("\nendsolid %s\n" % file)
        tweaked = "".join(tweaked)

        return tweaked

    @staticmethod
    def rotate_vert(content, r):
        return [content[0]*r[0][0] + content[1]*r[1][0] + content[2]*r[2][0],
                content[0]*r[0][1] + content[1]*r[1][1] + content[2]*r[2][1],
                content[0]*r[0][2] + content[1]*r[1][2] + content[2]*r[2][2]]

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

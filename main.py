import time
import orient
import vtkplotlib as vpl
from orient import Tweak
import numpy as np
import subprocess
# from itertools import

if __name__ == "__main__":
    message = "Choose one of these files:" \
              "\n1.\ttest__0.stl" \
              "\n2.\ttest.__1stl" \
              "\n3.\ttest__2.stl" \
              "\n4.\ttest__3.stl" \
              "\n5.\ttest__4.stl" \
              "\n6.\ttest__5.stl" \
              "\n7.\ttest__6.stl\n"
    k = input(message)
    accepted_input = ["1", "2", "3", "4", "5", "6", "7"]
    while k not in accepted_input:
        print("\nERROR! Invalid input. Try again!")
        k = input(message)
    t1 = time.time()
    files = ["Resources/models/test.stl", "Resources/models/test3.stl",
             "Resources/models/test2.stl", "Resources/models/test11.stl",
             "Resources/models/test12.stl", "Resources/models/Sphere.stl",
             "Resources/models/test6.stl"]
    file = files[int(k) - 1]
    orient = orient.TakeFile()
    objects = orient.loadMesh(file)
    heights = None
    for obj in objects:
        mesh = obj["Mesh"]
        x = Tweak(mesh)
        r = x.r
        print(f'Value of R is \n{r}')
        coords = orient.rotate_mesh(r, mesh)
        # subprocess.check_call("gcc HelloWorld.c -o out1;./out1", shell=True)
        # subprocess.check_call(["g++", "test.cpp"])
        t1 = time.time()
        subprocess.check_call("g++ -pthread -o Resources/temp/test.out slicer.cpp", shell=True)
        subprocess.call("Resources/temp/test.out")
        # print(time.time() - t1)
        # time.sleep(50)
        # print("Done waiting")
        # heights, number = slicer.slice_model(coords, rev_coords)
    """    f = open("Resources/temp/adap.txt", 'r')
    points = []
    for line in f:
        points.append(list(map(lambda u: float(u), line.split())))
    f.close()

    tris = []
    for i in range(0, len(points), 3):
        tris.append([points[i], points[i+1], points[i+2]])
    mesh = map(orient.calculate_normal, tris)
    temp = list(map(orient.write_facett, mesh))
    orient.write_stl(temp, 'b')
    """
    print(time.time() - t1)

    optimised = orient.load("Resources/temp/adap.stl")
    original = orient.load(file)

    fig = vpl.figure()
    # a = vpl.colors.cmap_from_list(heights, resolution=len(heights))
    # asdf = vpl.colors.as_vtk_cmap(a)
    # mesh1 = vpl.mesh_plot(optimised, scalars= optimised.y, cmap=asdf)
    # print(heights)
    # print(np.shape(heights))
    # height_map = vpl.colors.as_rgb_a('red', 1)
    # tri = np.inner(optimised.units, points)
    mesh2 = vpl.mesh_plot(original, color="red", opacity=0.3)
    mesh = vpl.mesh_plot(optimised, color="green", opacity=1)
    # vpl.view(camera_position=[0, 0, 0])
    # vpl.mesh_plot(optimised, scalars=optimised.z, cmap=vpl.colors.as_vtk_cmap(a))
    vpl.arrow(np.array([0, 0, 0]), np.array([10, 0, 0]), 10, color='red', opacity=0.5, label="x-axis")
    vpl.arrow(np.array([0, 0, 0]), np.array([0, 10, 0]), 10, color='blue', opacity=0.5, label="y-axis")
    vpl.arrow(np.array([0, 0, 0]), np.array([0, 0, 10]), 10, color='green', opacity=0.5, label="z-axis")
    vpl.view(camera_position=[0, 10, 0])
    print(time.time() - t1)
    vpl.show()
    """
    with open("h.txt", 'w') as out:
        for i in range(len(heights)):
            out.write(heights[i])
            out.write("\n")
    """

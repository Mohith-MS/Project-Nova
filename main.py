import orient
import vtkplotlib as vpl
from orient import Tweak

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
    files = ["Resources/models/test.stl", "Resources/models/test1.stl",
             "Resources/models/test2.stl", "Resources/models/test11.stl",
             "Resources/models/test8.stl", "Resources/models/test4.stl",
             "Resources/models/test6.stl"]
    file = files[int(k) - 1]
    orient = orient.TakeFile()
    objects = orient.loadMesh(file)

    for obj in objects:
        mesh = obj["Mesh"]
        x = Tweak(mesh)
        r = x.r
        print(f'Value of R is {r}')
        tweaked = orient.rotate_mesh(r, mesh)
        with open("a.stl", 'w') as out:
            out.write(tweaked)
    optimised = orient.load("a.stl")
    original = orient.load(file)
    fig = vpl.figure()
    mesh1 = vpl.mesh_plot(optimised, color="green")
    mesh2 = vpl.mesh_plot(original, color="red", opacity=0.3)
    vpl.view(camera_position=[0, 10, 0])
    vpl.show()

import orient
import vtkplotlib as vpl

# from stl.mesh import Mesh

if __name__ == "__main__":
    message = "Choose one of these files:" \
              "\n1.\ttest__0.stl" \
              "\n2.\ttest.__1stl" \
              "\n3.\ttest__2.stl" \
              "\n4.\ttest__3.stl" \
              "\n5.\ttest__4.stl\n"
    k = input(message)
    accepted_input = ["1", "2", "3", "4", "5"]
    while k not in accepted_input:
        print("\nERROR! Invalid input. Try again!")
        k = input(message)
    files = ["Resources/models/test.stl", "Resources/models/test1.stl",
             "Resources/models/test2.stl", "Resources/models/test3.stl",
             "Resources/models/test4.stl"]
    file = files[int(k) - 1]
    orient = orient.TakeFile()
    objects = orient.load(file)

    fig = vpl.figure()
    mesh = vpl.mesh_plot(objects)
    vpl.show()

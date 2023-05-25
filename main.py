import utils
import submain

[capacity,current_capacity,suppliers] = utils.read_input("./input/input1.csv")
F0 = utils.makeF0(
    suppliers = suppliers,
    capacity = capacity,
    current_capacity = current_capacity,
    n_max=20
)

ga = submain.GA(
    population = F0,
    capacity = capacity,
    suppliers = suppliers,
    n_fix = 50,
    n_selection = 0.25,
    n_GA = 100,
    n_cross = 1,
    n_muation = 0.25,
    n_enhance = 1,
    output = "output.txt",
    current_capacity = current_capacity
)

utils.write_output(ga,"./output/output.csv")
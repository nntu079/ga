import utils
import submain

[capacity,current_capacity,suppliers] = utils.read_input("./input/input1.csv")
F0 = utils.makeF0(
    suppliers = suppliers,
    capacity = capacity,
    current_capacity = current_capacity,
    n_max=40
)

ga = submain.GA(
    population = F0,
    capacity = capacity,
    suppliers = suppliers,
    n_fix = 100,
    n_GA = 4,
    n_cross = 10,
    n_selection = 50,
    n_muation = 0.3,
    n_enhance = 0.8,
    output = "output.txt",
    current_capacity = current_capacity
)

utils.write_output(ga,"./output/output.csv")
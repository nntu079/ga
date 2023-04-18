import utils
import submain

[capacity,current_capacity,suppliers] = utils.read_input("./input/input1.csv")
F0 = utils.makeF0(suppliers,capacity,current_capacity,5)

ga = submain.GA(
    population = F0,
    n_fix = 10,
    capacity = capacity,
    suppliers = suppliers,
    n_GA = 3,
    n_cross = 5,
    n_muation = 0.6,
    n_enhance = 10,
    n_selection = 10,
    output = "output.txt",
    current_capacity = current_capacity
)

utils.write_output(ga,"./output/output.csv")
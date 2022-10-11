from numpy import ceil, log2, floor, pi
from qiskit.circuit import QuantumCircuit, QuantumRegister


def get_qram(N, M, array):
    index = 0
    index_size = int(ceil(log2(N)))
    value_size = int(floor(log2(M))) + 1

    index_reg = QuantumRegister(name="index", size=index_size)
    value_reg = QuantumRegister(name="value", size=value_size)

    circ = QuantumCircuit(index_reg, value_reg, name="oracle")
    circ.h(index_reg)
    # to store circuits for previously seen elements
    circ_cache = {}

    def get_elem_circ(elem, idx):
        # analyse this element
        if elem in circ_cache:
            elem_circ = circ_cache[elem]
        else:
            bin_rep = bin(elem)[2:]
            elem_circ = QuantumCircuit(value_size, name=f"x_{idx}")
            bin_rep = bin_rep[::-1]

            for i, bit in enumerate(bin_rep):
                if bit == "1":
                    elem_circ.x(i)
            circ_cache[elem] = elem_circ

        elem_circ = elem_circ.control(num_ctrl_qubits=index_size, ctrl_state=idx)

        return elem_circ

    for elem in array:
        circuit = get_elem_circ(elem, index)
        circuit.name = f"x_{index}"
        circ.compose(circuit, inplace=True)
        index += 1

    del circ_cache

    return circ


def get_qram_rotations(N, rotations):
    index = 0
    index_size = int(ceil(log2(N)))
    value_size = 1

    index_reg = QuantumRegister(name="index", size=index_size)
    value_reg = QuantumRegister(name="value", size=value_size)

    circ = QuantumCircuit(index_reg, value_reg, name="oracle")
    circ.h(index_reg)
    # to store circuits for previously seen elements

    def get_elem_circ(idx, rot_type, angle):
        # analyse this element

        elem_circ = QuantumCircuit(value_size, name=f"{rot_type}_{round(angle,4)}")
        if rot_type == "x":
            elem_circ.rx(2 * pi * angle, 0)
        elif rot_type == "y":
            elem_circ.ry(2 * pi * angle, 0)
        else:
            elem_circ.rz(2 * pi * angle, 0)

        elem_circ = elem_circ.control(num_ctrl_qubits=index_size, ctrl_state=idx)

        return elem_circ

    for elem in rotations:
        rot_type, angle = elem
        circuit = get_elem_circ(index, rot_type, angle)
        circuit.name = f"x_{index}"
        circ.compose(circuit, inplace=True)
        index += 1

    return circ

from qiskit import QuantumCircuit


def dj_circuit_general(size, oracle):

    #     dj_circuit = QuantumCircuit(n+1, n)
    ### Your code here
    qc = QuantumCircuit(size + 1, size)

    # last qubit should be in |-> state
    qc.x(size)
    qc.h(range(size + 1))

    qc.barrier()
    qc.compose(oracle, qubits=list(range(size + 1)), inplace=True)
    qc.barrier()

    qc.h(range(size))

    qc.measure(list(range(size)), list(range(size)))

    return qc
    ### Your code here

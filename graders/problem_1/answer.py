from qiskit import QuantumCircuit, Aer, execute

sv_backend = Aer.get_backend("statevector_simulator")


def get_bell():
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.h(0)
    qc.cx(0, 1)

    return qc


def get_even_odd(n):

    even = QuantumCircuit(n)
    odd = QuantumCircuit(n)

    # even circuit
    even.h(range(1, n))

    # odd circuit
    odd.h(range(1, n))
    odd.x(0)

    even_sv = execute(even, sv_backend).result().get_statevector()
    odd_sv = execute(odd, sv_backend).result().get_statevector()

    return even_sv, odd_sv

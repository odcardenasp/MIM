def psiToPa(P_psi):
    result = P_psi * 6894.76 
    return result 

def PaTopsi(P_Pa):
    result = P_Pa / 6894.76 
    return result 

def TdPoly(Ps, Pc, Ts, n):
    Td = Ts * (Pc / Ps)**( (n - 1) / n )
    return Td

def btuToW(input):
    output = input / 3.412
    return output
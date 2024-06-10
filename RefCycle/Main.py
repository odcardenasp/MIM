from compressor import Compressor

comp2 = Compressor("CP1", "Copeland", "ZB48", "R22")
print(comp2.reference)

bb = comp2.massFlow(-8, 20)
ab = comp2.work_per_mass(50, 200, 20, 90)
print(ab)
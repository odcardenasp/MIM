import numpy as np

data = {"azul": 123, "rojo" : 100, "colores": [103, 105] }

print(data)


for x in data:
    print(data.get(x))
    if data.get(x) is not None:
        print("Que rico")
    else:   
        print("No que rico")


mydata = np.arange(1,5)
print(mydata)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
file = pd.read_csv('ExoplanetsPars_2024.csv',comment='#')
print(file.columns)
print(file)
plt.plot(np.log(file['pl_bmassj']),np.log(file['pl_orbper']))




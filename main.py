import pandas as pd
import numpy as np

import_data = pd.read_excel('restoran.xlsx')
data = import_data.to_numpy().copy()

print(data)
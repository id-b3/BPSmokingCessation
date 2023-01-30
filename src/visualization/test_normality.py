#!/usr/bin/env python
from pathlib import Path
import sys
import pdb

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from matplotlib.pyplot import text

output_dir = Path("./reports/figures/test_normal/")
output_dir.mkdir(parents=True, exist_ok=True)
# Generate some random data
# data = np.random.normal(0,1,1000)
data = pd.read_csv(sys.stdin)
var_name = data.columns[0].replace("_", " ").upper()

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle(var_name)

# histogram
axs[0, 0].hist(data.iloc[:, 0], bins=20, density=True, alpha=0.6, color='b')
axs[0, 0].set_title('Histogram')
axs[0, 0].set_xlabel('Data')
axs[0, 0].set_ylabel('Frequency')

# Q-Q plot
sm.qqplot(data.iloc[:, 0], line='s', ax=axs[0, 1])
axs[0, 1].set_title("Q-Q plot")

# Anderson-Darling test
result = stats.anderson(data.iloc[:, 0])
axs[1, 0].text(0.5,
               0.7,
               'Anderson-Darling test:',
               fontsize=12,
               ha='center',
               va='center',
               weight='bold')
axs[1, 0].text(
    0.5,
    0.4,
    'Statistic: %.3f\n' % result.statistic + '\n'.join([
        f'{sl} : {cv}, data ' +
        ('does not look normal (reject H0)'
         if result.statistic > cv else 'looks normal (fail to reject H0)')
        for sl, cv in zip(result.significance_level, result.critical_values)
    ]),
    fontsize=12,
    ha='center',
    va='center')
axs[1, 0].axis('off')

# Shapiro-Wilk test
result = stats.shapiro(data.iloc[:, 0])
text(0.5,
     0.6,
     'Shapiro-Wilk test:',
     fontsize=12,
     ha='center',
     va='center',
     transform=axs[1, 1].transAxes,
     weight='bold')
text(0.5,
     0.5,
     'Statistics=%.3f, p=%.3f' % (result),
     fontsize=12,
     ha='center',
     va='center',
     transform=axs[1, 1].transAxes)
axs[1, 1].axis('off')

# Kolmogorov-Smirnov test
result = stats.kstest(data.iloc[:, 0], 'norm')
text(0.5,
     0.4,
     'Kolmogorov-Smirnov test:',
     fontsize=12,
     ha='center',
     va='center',
     fontweight='bold',
     transform=axs[1, 1].transAxes)
text(0.5,
     0.3,
     'Statistics=%.3f, p=%.3f' % (result),
     fontsize=12,
     ha='center',
     va='center',
     transform=axs[1, 1].transAxes)
axs[1, 1].axis('off')

plt.subplots_adjust(hspace=0.4)
plt.savefig(str(output_dir / f'{var_name}_norm_test.png'), dpi=300)
plt.close()

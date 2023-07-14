#!/usr/bin/env python
import logging

import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
from matplotlib.pyplot import text

logger = logging.getLogger("BronchialParameters")

def test(data, bps, out_path):

    for param in bps:
        for sex in data["sex"].unique():
            var_name = param.replace("_", " ").title()
            var_name += f" {sex}"
            logger.info(f"Testing normality for {var_name}")

            fig, axs = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle(var_name)

            param_data = data[param].dropna()

            # histogram
            axs[0, 0].hist(param_data,
                           bins=30,
                           density=True,
                           alpha=0.6,
                           color='b')
            axs[0, 0].set_title('Histogram')
            axs[0, 0].set_xlabel('Data')
            axs[0, 0].set_ylabel('Frequency')

            # Q-Q plot
            sm.qqplot(param_data, line='s', ax=axs[0, 1])
            axs[0, 1].set_title("Q-Q plot")

            # Anderson-Darling test
            result = stats.anderson(param_data)
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
                    ('does not look normal (reject H0)' if result.statistic > cv else
                     'looks normal (fail to reject H0)') for sl, cv in zip(
                         result.significance_level, result.critical_values)
                ]),
                fontsize=12,
                ha='center',
                va='center')
            axs[1, 0].axis('off')

            # Shapiro-Wilk test
            result = stats.shapiro(param_data)
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
            result = stats.kstest(param_data, 'norm')
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
            plt.savefig(str(out_path / f'{var_name}_{sex}_norm_test.png'), dpi=300)
            plt.close()
            logger.info(f"Done testing normality for {param}")

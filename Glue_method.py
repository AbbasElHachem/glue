# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: EL Hachem Abbas,
Institut für Wasser- und Umweltsystemmodellierung - IWS
"""
import os
import timeit
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print('\a\a\a\a Started on %s \a\a\a\a\n' % time.asctime())
START = timeit.default_timer()  # to get the runtime of the program

main_dir = os.path.join(r'X:\hiwi\ElHachem\AdvancedPython')
os.chdir(main_dir)

in_data_file = os.path.join(main_dir, '\Glue_method\discharge_bedload.csv')
assert in_data_file

df_sep = ','
in_df = pd.read_csv(in_data_file, sep=df_sep, header=[0])

ns_thr = 0.5

range_first_param = [0, 0.8]
range_second_param = [0.05, 1.2]

sim_nbr = 0

var_bed_load = np.var(in_df['Bedload'].values) * len(in_df['Bedload'].values)
nash_vals = {'a': [], 'b': [], 'NS': []}

while sim_nbr < 1e5:
    rv_first_param = np.random.rand()*(
        max(range_first_param) - min(range_first_param))\
        + min(range_first_param)

    rv_second_param = np.random.rand()*(
        max(range_second_param) - min(range_second_param))\
        + min(range_second_param)

    diff_orig_sim = np.sum([(rv_first_param * discharge ** rv_second_param
                             - bedload) ** 2
                            for bedload, discharge in
                            zip(in_df['Bedload'].values,
                                in_df['Discharge'].values)])
    nash_value = 1 - diff_orig_sim/var_bed_load

    nash_vals['a'].append(rv_first_param)
    nash_vals['b'].append(rv_second_param)
    nash_vals['NS'].append(nash_value)

    sim_nbr += 1
    print('done with simulation:', sim_nbr)

df_param_nash = pd.DataFrame.from_dict(nash_vals)
df_param_nash.to_csv('parameters_and_ns_all_.csv', sep=';')

df_param_nash2 = df_param_nash[df_param_nash['NS'] >= ns_thr]
df_param_nash2.to_csv('parameters_and_ns_good_perf.csv', sep=';')

plt.scatter(df_param_nash['a'], df_param_nash['b'],
            c='b', marker='+', alpha=0.25, s=2,
            label='All parameters')
plt.scatter(df_param_nash2['a'], df_param_nash2['b'],
            c='r', marker='o', alpha=0.75, s=35,
            label='NS >0.5 parameters')
plt.ylim([0.6, 1.21])
plt.xlim([0, 0.03])
plt.title('Distribution of Prameters leading to highest Nash values')
plt.xlabel('Parameter: a')
plt.ylabel('Parameter: b')
plt.legend(loc=0)
plt.savefig('parmaters_all_simulations_and_good_params.png')

STOP = timeit.default_timer()  # Ending time
print(('\n\a\a\a Done with everything on %s. Total run time was'
       ' about %0.4f seconds \a\a\a' % (time.asctime(), STOP-START)))

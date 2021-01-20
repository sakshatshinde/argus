import numpy as np
import matplotlib.pyplot as plt
import retrieve_data as rd
import time

# print(rd.cachestat_data_ms)
print("-----------------------------")
# print(rd.cachestat_data_IO)
# print(rd.io_latency_data)

# for reference
# "{'hits': '18797', 'misses': '0', 'mbd': '12', 'ratio': '100', 'buffers_mb': '82', 'cached_mb': '1341'}"

labels = 'hits', 'misses', 'cached_mb'
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

for _ in rd.io_latency_data:
    result = list(_.values())
    result_temp = result[:2]
    result_temp.append(result[5:][0])
    result = result_temp
    print(result)

    fig1, ax1 = plt.subplots()


    #explsion
    explode = (0.05,0.05,0.05)

    ax1.pie(result, labels = None, labeldistance = 0.9, colors = colors,
            shadow=False, startangle=90, autopct='%1.1f%%')

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # drawing a middle circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.legend(labels, loc='center', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

    plt.show()
    plt.tight_layout()
    time.sleep(2)
    break

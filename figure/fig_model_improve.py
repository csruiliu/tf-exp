# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import csv
import re

#csvpath = '/home/ruiliu/Development/mtml-tf/mt-exp/exp-result/exp-resnet.csv'
outpath = '/home/ruiliu/Development/mtml-tf/figure/gpu-model-improve.pdf'


model_no = [1,2,3,4]
improve_mlp = [0, 39.7, 65, 74]
improve_resnet = [0, 21.1, 25, 27]
improve_mobilenet = [0, 21.8, 30, 33.2]

model_no_densenet = [1,2,3]
improve_densenet = [0, 17.9, 21]

plt.figure(figsize=(6, 4))

plt.plot(model_no, improve_mlp, color='royalblue', marker='^', linestyle='-', linewidth=2, markersize=8, label='MLP-3')
plt.plot(model_no, improve_mobilenet, color='seagreen', marker='o', linestyle=':', linewidth=2, markersize=6, label='MobileNet')
plt.plot(model_no, improve_resnet, color='orangered', marker='D', linestyle='-.', linewidth=2, markersize=7, label='ResNet-50')
plt.plot(model_no_densenet, improve_densenet, color='goldenrod', marker='*', linestyle='--', linewidth=2, markersize=9, label='DenseNet-121')
plt.yticks(np.arange(0,103,20), ('0%', '20%', '40%', '60%', '80%', '100%'))
plt.xticks(np.arange(1,5,1))
plt.tick_params(axis='y',direction='in',labelsize=20) 
plt.tick_params(axis='x',direction='in',bottom='False',labelsize=20)

plt.xlabel("Number of Packing Models", fontsize=22)
plt.ylabel("Improvement of Packing", fontsize=21)
plt.legend(loc='upper left', fontsize=15)
plt.tight_layout()
plt.savefig(outpath, format='pdf', bbox_inches='tight', pad_inches=0.05)
#plt.show()
#print(x_pt)
#print(y_pt)




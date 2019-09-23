import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fileName = "Plot example"
plt.rcParams["figure.figsize"] = (12,7)
f, ax1 = plt.subplots()
f.suptitle('Example plot', fontsize=20)
ax1.set_xlabel('$x_1$' , fontsize=18)
ax1.set_ylabel('$x_2$' , fontsize=18)
ax1.grid(b=True, which='major', color='#666666', linestyle='-')
ax1.minorticks_on()
ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax1.plot([0,1,2,3],[0,1,2,3], c='red', label='Plot L1')
ax1.legend(bbox_to_anchor=(0.78, 0.95), loc=2, borderaxespad=0.)

plt.savefig(fileName+'.pdf', dpi=1000, bbox_inches='tight', pad_inches=0)
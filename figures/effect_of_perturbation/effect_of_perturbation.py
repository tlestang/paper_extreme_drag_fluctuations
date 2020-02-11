import os
import numpy as np
import matplotlib.pyplot as plt

tau_c = 1999
N = 2
labels = ["Trajectory {}".format(i) for i in range(N)]
labels[0] = "Reference trajectory"

fig, ax = plt.subplots(1, 1, figsize=(10, 4), constrained_layout=True)

for i in range(N):
    dirname = "simulation_{}".format(i)
    f = np.fromfile(os.path.join(dirname, "dragFile.dat"), float, -1, "")
    tspan = np.linspace(0, (len(f) - 1) / tau_c, len(f))
    plt.plot(tspan, f)

plt.legend(labels)

plt.xlabel(r"$t / \tau_c$", fontsize=22)
plt.ylabel("$f_d$", fontsize=22)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
figname = os.path.splitext(__file__)[0] + ".png"
plt.savefig(figname)
plt.show()

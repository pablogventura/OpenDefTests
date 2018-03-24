import numpy as np
import matplotlib.pyplot as plt

def export_legend(legend, filename="legend.pdf", expand=[-5,-5,5,5]):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)


colors = [r"$|\mathbf{A}|=30$",r"$|\mathbf{A}|=40$",r"$|\mathbf{A}|=50$",]
f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]
handles = [f(m, "black") for m in ["s","p","*","+","D","d","|","_"]]
labels = colors
legend = plt.legend(handles, labels,ncol=3)
legend.get_frame().set_edgecolor('black')

export_legend(legend, filename="legend_a2.pdf")

colors = [r"$|\mathbf{A}|=20$",r"$|\mathbf{A}|=30$",r"$|\mathbf{A}|=40$",]
f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]
handles = [f(m, "black") for m in ["o","s","p","*","+","D","d","|","_"]]
labels = colors
legend = plt.legend(handles, labels,ncol=3)
legend.get_frame().set_edgecolor('black')

export_legend(legend, filename="legend_a3.pdf")

colors = [r"$\lfloor{\mathbf{A}}\rfloor_{\leq k}$",r"$\ \mathbf{A}$"]
colors.reverse()
f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]
handles = [f(m, "black") for m in ["+","*","D","d","|","_"]]
labels = colors
legend = plt.legend(handles, labels,ncol=2,handletextpad=0)
legend.get_frame().set_edgecolor('black')

export_legend(legend, filename="legend_pre.pdf")


import matplotlib.pyplot as plt
import cfe.regression as rgsn
import numpy as np
import matplotlib.cm
from scipy.stats import gaussian_kde as kde
from cfe.df_utils import use_indices

def annotate_quantiles(labelY,ax,xbar,x99):
    xtext = -2
    ytext_offset = -0.057 #to center line orgin with text
    ytext = labelY - ytext_offset
    ytext_sign = np.sign(ytext) if np.sign(ytext) else 1
    ytext_spacing = 0.13
    
    def point_on_circle(theta,r):
        return r*np.cos(theta),-r*np.sin(theta)
    
    def intersection_on_circle(quantile,y):
        radius = np.log(xbar.quantile(quantile))/np.log(x99)
        print(y/radius)
#         unit_y = ytext_sign*np.pi/2 if np.abs(y/radius) >= 1 else np.arcsin(y/radius)+np.pi
        unit_y = np.arcsin(y/radius)+np.pi,
        temp = point_on_circle(unit_y,radius)
    
    ax.annotate("99%",
                xy=intersection_on_circle(0.99,ytext),
                xytext=(xtext, ytext),
                arrowprops=dict(arrowstyle="-"))
    ax.annotate("Median",
                xy=intersection_on_circle(0.5,ytext:=ytext-ytext_sign*ytext_spacing),
                xytext=(xtext, ytext),
                arrowprops=dict(arrowstyle="-"))
    ax.annotate("1%",
                xy=intersection_on_circle(0.01,ytext:=ytext-ytext_sign*ytext_spacing),
                xytext=(xtext, ytext),
                arrowprops=dict(arrowstyle="-"))
    return ax

def make_engel_pie(r: rgsn.Regression, labelY = -0.5) -> plt.Axes:
    def circle(r):
        angles = np.linspace(0,2*np.pi,100)
        return r*np.cos(angles),r*np.sin(angles)

    xbar = r.predicted_expenditures().groupby(['i','t','m']).sum()
    x99 = xbar.quantile(1)
    Y = np.geomspace(1,x99,100)    
    p = ((r.y.unstack('j')>0) + 0.).mean()
    fig,ax = plt.subplots()
    
    shares = r.expenditures(Y[-1])*p
    shares = shares/shares.sum()
    labels = use_indices(shares,['j'])
    labels['shares'] = shares
    labels = labels.j.where(labels.shares>0.01,'').tolist()

    ax.pie(shares,labels=labels,rotatelabels=False,labeldistance=1.1)

    for i in range(len(Y)-1,0,-1):
        ax.pie(r.expenditures(Y[i])*p,radius=np.log(Y[i])/np.log(x99))

    ax.arrow(0,0,1,0,shape='full',head_width=.05,length_includes_head=True)
    ax.annotate(r"$\log x$", xy=(1,0),color='red')    
    
    ax.plot(*circle(np.log(xbar.quantile(0.01))/np.log(x99)),'k')
    ax.plot(*circle(np.log(xbar.quantile(0.5))/np.log(x99)),'k')
    ax.plot(*circle(np.log(xbar.quantile(0.99))/np.log(x99)),'k')
    
#    ax = annotate_quantiles(labelY,ax,xbar,x99)
    return ax

r = rgsn.read_pickle('./data/preferred.rgsn')
ax = make_engel_pie(r)
ax.get_figure().savefig('./out/engel_pie-0.png')

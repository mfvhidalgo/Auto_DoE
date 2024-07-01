#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dexpy
import dexpy.factorial
import dexpy.ccd
import itertools

#%%

# Define the range for each axis
axis_range = [-1, 1]

# Generate all combinations of corners dynamically
x, y, z = np.meshgrid(axis_range, axis_range, axis_range)
x = x.flatten()
y = y.flatten()
z = z.flatten()

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the scatter points
ax.scatter(x, y, z, c='r', marker='o')

# Set specific rotation
ax.view_init(elev=30, azim=45)  # elevation and azimuth

# Set the limits for x, y, z
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xticks([-1,0,1])
ax.set_yticks([-1,0,1])
ax.set_zticks([-1,0,1])

# Show the plot
plt.show()

#%% 2n vs 3n
# Function to sync the view of all axes
def sync_views(event):
    if event.inaxes:
        for ax in axs:
            if ax != event.inaxes:
                ax.view_init(elev=event.inaxes.elev, azim=event.inaxes.azim)
        fig.canvas.draw_idle()

# Create figure and 3D subplots
fig, axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'})

df = pd.DataFrame(dexpy.factorial.build_full_factorial(3))
axs[0].scatter(df[0], df[1], df[2], c='k', marker='o')

factor_data = []
for run in itertools.product([-1,0,1],repeat=3):
    factor_data.append(list(run))
df = pd.DataFrame(factor_data)
axs[1].scatter(df[0], df[1], df[2], c='k', marker='o')


for ax in axs:
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.view_init(elev=30, azim=45)  # Initial view angle
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks([-1,0,1])

# Connect the sync_views function to the motion_notify_event
fig.canvas.mpl_connect('motion_notify_event', sync_views)

# Show the plot in interactive mode
plt.show()

#%% 2n vs 3n vs FCD
# Function to sync the view of all axes
s = 50
def sync_views(event):
    if event.inaxes:
        for ax in axs:
            if ax != event.inaxes:
                ax.view_init(elev=event.inaxes.elev, azim=event.inaxes.azim)
        fig.canvas.draw_idle()

# Create figure and 3D subplots
fig, axs = plt.subplots(1, 3, subplot_kw={'projection': '3d'})

df = pd.DataFrame(dexpy.factorial.build_full_factorial(3))
axs[0].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)

factor_data = []
for run in itertools.product([-1,0,1],repeat=3):
    factor_data.append(list(run))
df = pd.DataFrame(factor_data)
axs[1].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)

df = dexpy.ccd.build_ccd(3,alpha=1)
df.columns = [0,1,2]
axs[2].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)


# df = dexpy.ccd.build_ccd(3)
# df.columns = [0,1,2]
# axs[2].scatter(df[0], df[1], df[2], c='k', marker='o')


for ax in axs:
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.view_init(elev=30, azim=45)  # Initial view angle
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks([-1,0,1])

# Connect the sync_views function to the motion_notify_event
fig.canvas.mpl_connect('motion_notify_event', sync_views)

# Show the plot in interactive mode
plt.show()

#%% 2n vs 3n vs CCF vs CCD
# Function to sync the view of all axes
s = 50
def sync_views(event):
    if event.inaxes:
        for ax in axs:
            if ax != event.inaxes:
                ax.view_init(elev=event.inaxes.elev, azim=event.inaxes.azim)
        fig.canvas.draw_idle()

# Create figure and 3D subplots
fig, axs = plt.subplots(1, 4, subplot_kw={'projection': '3d'})

df = pd.DataFrame(dexpy.factorial.build_full_factorial(3))
axs[0].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
axs[0].set_title('2ⁿ')

factor_data = []
for run in itertools.product([-1,0,1],repeat=3):
    factor_data.append(list(run))
df = pd.DataFrame(factor_data)
axs[1].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
axs[1].set_title('3ⁿ')

df = dexpy.ccd.build_ccd(3,alpha=1)
df.columns = [0,1,2]
axs[2].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
axs[2].set_title('Central Composite Face-centered')


df = dexpy.ccd.build_ccd(3)
df.columns = [0,1,2]
axs[3].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
axs[3].set_title('Central Composite Design')

min_val,max_val = -1,1
for ax in axs:
    ax.set_xlim([min_val, max_val])
    ax.set_ylim([min_val, max_val])
    ax.set_zlim([min_val, max_val])
    ax.view_init(elev=30, azim=45)  # Initial view angle
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks([-1,0,1])

# Connect the sync_views function to the motion_notify_event
fig.canvas.mpl_connect('motion_notify_event', sync_views)

# Show the plot in interactive mode
plt.show()

#%% CCF vs CCD
# Function to sync the view of all axes
s = 50
def sync_views(event):
    if event.inaxes:
        for ax in axs:
            if ax != event.inaxes:
                ax.view_init(elev=event.inaxes.elev, azim=event.inaxes.azim)
        fig.canvas.draw_idle()

# Create figure and 3D subplots
fig, axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'})

df = dexpy.ccd.build_ccd(3,alpha=1)
df.columns = [0,1,2]
axs[0].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
axs[0].set_title('Central Composite Face-centered')


df = dexpy.ccd.build_ccd(3)
df.columns = [0,1,2]
axs[1].scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
axs[1].set_title('Central Composite Design')

min_val,max_val = -2,2
for ax in axs:
    ax.set_xlim([min_val, max_val])
    ax.set_ylim([min_val, max_val])
    ax.set_zlim([min_val, max_val])
    ax.view_init(elev=30, azim=45)  # Initial view angle
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks([-1,0,1])

# Connect the sync_views function to the motion_notify_event
fig.canvas.mpl_connect('motion_notify_event', sync_views)

# Show the plot in interactive mode
plt.show()

#%%

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)

ns = np.arange(2,11,1)
ax.plot(ns,[2**n for n in ns],label='2ⁿ',marker='o',linestyle='-')
ax.plot(ns,[3**n for n in ns],label='3ⁿ',marker='o',linestyle='-')
ax.plot(ns,[2**n+2*n+1 for n in ns],label='CCD or CCF',marker='o',linestyle='-')
ax.plot(ns,[2*n*(n-1)+1 for n in ns],label='BBD',marker='o',linestyle='-')
ax.plot(ns,[n+n+n*(n-1)/2+1 for n in ns],label='Quad. OD',marker='o',linestyle='-')

ax.set_xlabel('No. of Features')
ax.set_ylabel('No. of Experiments')
ax.set_ylim(0,100)
ax.legend(frameon=False)

#%% categorical

#%% CCF vs CCD
# Function to sync the view of all axes
s = 50
def sync_views(event):
    if event.inaxes:
        for ax in axs:
            if ax != event.inaxes:
                ax.view_init(elev=event.inaxes.elev, azim=event.inaxes.azim)
        fig.canvas.draw_idle()

# Create figure and 3D subplots
fig, axs = plt.subplots(1, 3, subplot_kw={'projection': '3d'})

df = dexpy.ccd.build_ccd(3)
df.columns = [0,1,2]
for ax,title in zip(axs,['Li','Na','K']):
    ax.scatter(df[0], df[1], df[2], c='k', marker='o',s=s)
    ax.set_title(title)

min_val,max_val = -2,2
for ax in axs:
    ax.set_xlim([min_val, max_val])
    ax.set_ylim([min_val, max_val])
    ax.set_zlim([min_val, max_val])
    ax.view_init(elev=30, azim=45)  # Initial view angle
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks([-1,0,1])

# Connect the sync_views function to the motion_notify_event
fig.canvas.mpl_connect('motion_notify_event', sync_views)

# Show the plot in interactive mode
plt.show()

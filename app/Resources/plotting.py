import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import numpy as np
from matplotlib.patches import Patch


def plot_rate(holeID, df, feature):
    fig, ax = plt.subplots(figsize = (5, 12))
    hole = df[df.holeID == holeID]
    X = hole[feature].values
    Y = hole.Depth

    ax.plot(X, Y, color='aqua')
    ax.set_facecolor('black')
    plt.gca().invert_yaxis()
    plt.ylabel('Depth')
    plt.xlabel(feature)
    plt.title('Hole: ' + holeID)

    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png')
    bytes_image.seek(0)

    return bytes_image


def encode_all_holes(df):
    list_of_dicts = []
    holeIDs = set(df.holeID)

    for hole in holeIDs:
        specific_df = df[df.holeID == hole]  # Grabs the entries of the specific holeID
        depth = specific_df.Depth.max() - specific_df.Depth.min()  # Calculates the overall depth
        temp_dict = {'holeID': hole, 'depth': depth}  # Creates a dictionary for each holeID
        fig, ax = plt.subplots(figsize = (5, 12))  # Generate the figure and axis before loop for reuseability for efficiency
        for feature in df.columns[1:6]:  # Loop over all relevant features
            ax.plot(specific_df[feature].values, specific_df.Depth, color='aqua')
            ax.set_facecolor('black')
            plt.gca().invert_yaxis()
            plt.ylabel('Depth')
            plt.xlabel(feature)
            plt.title('Hole: ' + hole)
            bytes_image = io.BytesIO()
            fig.savefig(bytes_image, format='png')
            bytes_image.seek(0)
            ## Clear the figure, axis, and close plot to reuse
            plt.cla()
            ## Encode the bytes image to base64, and convert from bytes to string to return
            img_base64 = base64.b64encode(bytes_image.read())
            temp_dict[feature] = img_base64.decode()
        ## Append the holeID dictionary to the overall list
        list_of_dicts.append(temp_dict)
    return list_of_dicts


def all_features_update(df, holeID):
    colors = ['aqua', 'salmon', 'darkviolet', 'palegreen', 'navajowhite']
    color_dict = dict(zip(df.columns[1:6], colors))
    xlim_dict = dict(zip(df.columns[1:6], [[0, 4.5], [9, 28], [33.5 , 62.5], [40, 76], [0, 4]]))

    specific_df = df[df.holeID == holeID]  # Grabs the entries of the specific holeID
    depth = specific_df.Depth.max() - specific_df.Depth.min()  # Calculates the overall depth
    temp_dict = {'holeID': holeID, 'depth': depth}  # Creates a dictionary for each holeID
    fig, ax = plt.subplots(figsize=(5, 12))  # Generate the figure and axis before loop for reuseability for efficiency

    # Plot The First Feature:
    line, = ax.plot(specific_df[df.columns[1]].values, specific_df.Depth, color=color_dict[df.columns[1]])
    ax.set_facecolor('grey')
    ax.axes.yaxis.set_ticks(range(int(np.floor(specific_df.Depth.min())),
                                  int(np.ceil(specific_df.Depth.max())) + 1))
    plt.ylim([0, int(np.ceil(specific_df.Depth.max()))])
    plt.xlim(xlim_dict[df.columns[1]])
    plt.gca().invert_yaxis()
    plt.ylabel('Depth')
    plt.xlabel(df.columns[1])
    plt.title(r"$\bf{" + holeID + ": " + df.columns[1] + "}$")
    plt.grid()
    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png', bbox_inches='tight')
    bytes_image.seek(0)
    img_base64 = base64.b64encode(bytes_image.read())
    temp_dict[df.columns[1]] = img_base64.decode()

    for feature in df.columns[2:6]:
        plt.xlim(xlim_dict[feature])
        line.set_xdata(specific_df[feature].values)
        line.set_color(color_dict[feature])
        plt.xlabel(feature)
        plt.title(r"$\bf{" + holeID + ": " + feature + "}$")
        fig.canvas.draw()
        fig.canvas.flush_events()

        bytes_image = io.BytesIO()
        fig.savefig(bytes_image, format='png', bbox_inches='tight')
        bytes_image.seek(0)
        img_base64 = base64.b64encode(bytes_image.read())
        temp_dict[feature] = img_base64.decode()
    plt.close(fig)
    return temp_dict


def plot_all_features(df, holeID):
    soft = .8
    hard = 1.8

    colors = ['aqua', 'salmon', 'darkviolet', 'palegreen', 'navajowhite']
    color_dict = dict(zip(df.columns[1:6], colors))

    specific_df = df[df.holeID == holeID]  # Grabs the entries of the specific holeID
    depth = specific_df.Depth.max() - specific_df.Depth.min()  # Calculates the overall depth
    temp_dict = {'holeID': holeID, 'depth': depth}  # Creates a dictionary for each holeID
    fig, ax = plt.subplots(figsize = (5, 13))  # Generate the figure and axis before loop for reuseability for efficiency

    for feature in df.columns[1:6]:  # Loop over all relevant features
        ax.plot(specific_df[feature].values, specific_df.Depth, color=color_dict[feature])

        #plt.xlim([0, 4.5])
        ax.set_facecolor('grey')
        ax.axes.yaxis.set_ticks(range(int(np.floor(specific_df.Depth.min())),
                                      int(np.ceil(specific_df.Depth.max())) + 1))
        plt.ylim([0, int(np.ceil(specific_df.Depth.max()))])

        plt.gca().invert_yaxis()
        plt.ylabel('Depth')
        plt.xlabel(feature)
        plt.title(r"$\bf{" + holeID + ": " + feature + "}$")
        plt.grid()
        bytes_image = io.BytesIO()
        fig.savefig(bytes_image, format='png', bbox_inches = 'tight')
        bytes_image.seek(0)
        ## Clear the figure, axis, and close plot to reuse
        plt.cla()
        ## Encode the bytes image to base64, and convert from bytes to string to return
        img_base64 = base64.b64encode(bytes_image.read())
        temp_dict[feature] = img_base64.decode()
    plt.close(fig)
    return temp_dict


def plot_cluster(data2D, projectID, labels, model = 'Agglomerative', mode = 'PCA'):
    axis_labels = ['PC1', 'PC2'] if (mode == 'PCA' or mode == 'unweighted') else ['x', 'y']

    fig, ax = plt.subplots(figsize=(15, 12))

    model_title = 'Agglomerative' if model == 'agglom' else 'KMeans' if model =='kmeans' else 'Spectral'

    clust = ax.scatter(x=data2D[axis_labels[0]], y=data2D[axis_labels[1]], c=labels, cmap='rainbow', alpha=.6,
                       s=10 + data2D.Depth.map(lambda x: 15 * float(x)))

    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])
    ax.set_title(model_title + ' Clustering of ' + projectID + ' data projected into 2D')
    # Produce a legend of the colors associated with each cluster
    legend1 = ax.legend(*clust.legend_elements(),
                        loc="upper left", title="Cluster Number", markerscale=1.5)
    ax.add_artist(legend1)

    # Produce a legend of the depth values:
    kw = dict(prop="sizes", color=clust.cmap(0.7), fmt="{x:.3f}m",
              func=lambda s: (s - 10) / 15)
    legend2 = ax.legend(*clust.legend_elements(**kw),
                        loc="upper right", title="Depth", labelspacing=1.3, borderpad=.6)
    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png', bbox_inches = 'tight', rasterized = True)
    bytes_image.seek(0)
    img_base64 = base64.b64encode(bytes_image.read())
    plt.close(fig)
    return img_base64.decode()


def hardness_bar_plot(df, holeID, projectID, color_version = 0):
    step = 1 if projectID == 'Montana' else 3 # Sets the step size for binning rows together (Not needed for montana)
    soft = 1.8 # Sets boundary for hard rock
    hard = .8 # Sets boundary for soft rock
    color_combos = [['tab:cyan', 'tab:gray', 'tab:orange'], ['red', 'black', 'gold'],
              ['red', 'yellow', 'blue']]
    colors = dict(zip(['hard', 'medium', 'soft'], color_combos[color_version]))

    hole = df[df.holeID == holeID] # Grabs the entries of the specific holeID

    fig, ax = plt.subplots(figsize=(1, 12))
    #plt.ylim([hole.Depth.min(), hole.Depth.max()])
    plt.ylim([0, hole.Depth.max()])
    #ax.axes.yaxis.set_ticks(range(int(np.ceil(hole.Depth.min())), int(np.floor(hole.Depth.max())) + 1))
    ax.axes.yaxis.set_ticks(range(int(np.floor(hole.Depth.min())), int(np.ceil(hole.Depth.max())) + 1))
    plt.gca().invert_yaxis()
    plt.ylabel('Depth (meters)')

    binned = hole.groupby(hole.index // step).PenetrRate.mean()
    binned = pd.DataFrame(binned, columns=['PenetrRate'])
    binned['Hardness'] = binned.PenetrRate.map(
        lambda rate: 'soft' if rate >= soft else 'hard' if rate <= hard else 'medium')
    depth_per = (hole.Depth.max() - hole.Depth.min()) / len(binned)

    coord = hole.Depth.min()
    for entry in binned.iterrows():
        rectangle = plt.Rectangle((0, coord), 1, depth_per, fc=colors[entry[1][-1]], linewidth=0, figure = fig)
        ax.add_patch(rectangle)
        del rectangle

        coord += depth_per

    legend_elements = [Patch(facecolor='white', label='No Data'),
                       Patch(facecolor=color_combos[color_version][0], label='hard'),
                       Patch(facecolor=color_combos[color_version][1], label='medium'),
                       Patch(facecolor=color_combos[color_version][2], label='soft')]

    ax.axes.xaxis.set_ticks([])
    #plt.title(holeID + ' Hardness', weight = 'bold')
    plt.legend(handles=legend_elements, bbox_to_anchor=[1, 1.008], facecolor = 'darkgrey')
    #plt.subplots_adjust(top = 0.25, bottom = 0.2)

    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png', bbox_inches = 'tight')
    bytes_image.seek(0)
    img_base64 = base64.b64encode(bytes_image.read())
    plt.close(fig)
    return img_base64.decode()


def highlight_location(pos, holeID):
    fig, ax = plt.subplots(figsize=(5, 4))
    pos[pos.holeID != holeID].plot.scatter('start_x', 'start_y', s=100, ax=ax, color='black')
    pos[pos.holeID == holeID].plot.scatter('start_x', 'start_y', s=200, color='aqua', ax=ax, edgecolors='black')
    plt.ylabel('Northing' + r' $\longrightarrow$')
    plt.xlabel('Easting' + r' $\longrightarrow$')
    ax.set_yticks([])
    ax.set_xticks([])
    plt.ylim([pos.start_y.min() - 12, pos.start_y.max() + 12])
    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png', bbox_inches='tight')
    bytes_image.seek(0)
    img_base64 = base64.b64encode(bytes_image.read())
    plt.close(fig)
    return img_base64.decode()


def cluster_positions(pos, labels):
    holeID_dict = {hole: idx + 1 for idx, hole in enumerate(pos.holeID.unique())}

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(pos['start_x'], pos['start_y'], s=160, c=labels, cmap='viridis', edgecolors='black')
    for hole, num in holeID_dict.items():
        ax.text(x=pos[pos.holeID == hole].start_x - .6, y=pos[pos.holeID == hole].start_y + .75, s=str(num))
    plt.ylim([pos.start_y.min() - 10, pos.start_y.max() + 15])
    plt.ylabel(' '.join(('Northing', r'$\longrightarrow$')))
    plt.xlabel(' '.join(('Easting', r'$\longrightarrow$')))
    ax.set_yticks([])
    ax.set_xticks([])

    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png', bbox_inches='tight')
    bytes_image.seek(0)
    img_base64 = base64.b64encode(bytes_image.read())
    plt.close(fig)
    return img_base64.decode()

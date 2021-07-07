import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


def plot_rate(holeID, df, feature):
    fig, ax = plt.subplots()
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
        fig, ax = plt.subplots()  # Generate the figure and axis before loop for reuseability for efficiency
        for feature in df.columns[:5]:  # Loop over all relevant features
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


def plot_all_features(df, holeID):
    specific_df = df[df.holeID == holeID]  # Grabs the entries of the specific holeID
    depth = specific_df.Depth.max() - specific_df.Depth.min()  # Calculates the overall depth
    temp_dict = {'holeID': holeID, 'depth': depth}  # Creates a dictionary for each holeID
    fig, ax = plt.subplots()  # Generate the figure and axis before loop for reuseability for efficiency
    for feature in df.columns[:5]:  # Loop over all relevant features
        ax.plot(specific_df[feature].values, specific_df.Depth, color='aqua')
        ax.set_facecolor('black')
        plt.gca().invert_yaxis()
        plt.ylabel('Depth')
        plt.xlabel(feature)
        plt.title(r"$\bf{" + feature + "}$")
        bytes_image = io.BytesIO()
        fig.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        ## Clear the figure, axis, and close plot to reuse
        plt.cla()
        ## Encode the bytes image to base64, and convert from bytes to string to return
        img_base64 = base64.b64encode(bytes_image.read())
        temp_dict[feature] = img_base64.decode()
    return temp_dict


def plot_clusters(df):
    fig, ax = plt.subplots()

    df.plot.scatter(x='x', y='y', c='CID', colormap='rainbow', figsize=(14, 10), alpha=.6,
                    s=10 + df.Depth.map(lambda x: 20 * float(x)), ax=ax)
    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    img_base64 = base64.b64encode(bytes_image.read())
    return img_base64.decode()
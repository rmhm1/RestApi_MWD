from flask_restful import Resource, reqparse, Api
from flask import jsonify, json, current_app as app
from . import engine, db
from .Resources.plotting import plot_rate, plot_cluster, encode_all_holes, pd, plot_all_features
import base64
from .models import BlastReport
from .Resources.Clustering import cluster_data, modify_data


api = Api(app)


class HolePlots(Resource):
    def get(self, feature, holeID, projectID):
        data = pd.read_sql(projectID, engine)

        if feature not in data.columns:
            response = {
                'error': 'An incorrect feature name was given'
            }
            return jsonify(response)
        bytes_obj = plot_rate(holeID, data, feature)
        img_base64 = base64.b64encode(bytes_obj.read())

        response = {
            'holeID': holeID,
            'Feature': feature,
            "image": img_base64.decode()
        }
        return jsonify(response)


class HoleIDByProject(Resource):
    def get(self, projectID):
        data = pd.read_sql(projectID, engine)
        dicts = []
        for hole in set(data.holeID):
            dicts.append({'holeID': hole})
        return dicts


class PlotAllHoles(Resource):
    def get(self, projectID):
        data = pd.read_sql(projectID, engine)
        dicts = encode_all_holes(data)

        return json.dumps(dicts)


# Plots all of the features of a specific holeID
class PlotAllFeatures(Resource):
    def get(self, projectID, holeID):
        data = pd.read_sql(projectID, engine)
        dict = plot_all_features(data, holeID)

        return dict


class Report(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('holeID', type = str, help = 'ID of Hole', required = True)
        self.reqparse.add_argument('depth', type=float, help='Depth of the blast in the hole', required=True)
        self.reqparse.add_argument('report', type=str, help='Report of Blast', required=True)
        self.reqparse.add_argument('score', type=int, help='Rating of the Blast', required=True)

    def get(self, projectID):
        args = self.reqparse.parse_args()
        result = BlastReport.query.get((args['holeID'], args['depth']))
        return result.serialize()

    def post(self, projectID):
        args = self.reqparse.parse_args()
        blast_report = BlastReport(holeID=args['holeID'], depth=args['depth'],
                                   report=args['report'], score=args['score'])
        db.session.add(blast_report)
        db.session.commit()
        return blast_report.serialize()

    def delete(self, projectID):
        args = self.reqparse.parse_args()
        result = BlastReport.query.get((args['holeID'], args['depth']))
        db.session.delete(result)
        db.session.commit()
        return result.serialize()


class Clustering(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('data_type', type=str, required=False, default='PCA')
        self.reqparse.add_argument('k', type=int, required=False, default=4)
        self.reqparse.add_argument('model', type=str, required=False, default='agglom')

    # Get method to send the encoded plots of the 2D clustering
    def get(self, projectID):
        args = self.reqparse.parse_args()

        mwd_data = pd.read_sql(projectID, engine)
        data = modify_data(mwd_data.iloc[:, 1:6], data_type = args['data_type'])
        cluster_labels = cluster_data(data, model = args['model'], k = args['k'])
        if args['data_type'] == 'weighted':
            data2D = pd.read_sql('KMeans_WMDS', engine)
            b64_string = plot_cluster(data2D, projectID, cluster_labels, args['model'], args['mode'])
        else:
            data['Depth'] = mwd_data.Depth
            b64_string = plot_cluster(data, projectID, cluster_labels, args['model'], args['data_type'])

        response = {'image': b64_string}
        return response


# Used to get entries in the same cluster as the blast
class ClusterByBlastEntry(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('depth', type=float, required=True)
        self.reqparse.add_argument('holeID', type=str, required=True)
        self.reqparse.add_argument('data_type', type=str, required=False, default='PCA')
        self.reqparse.add_argument('k', type=int, required=False, default=4)
        self.reqparse.add_argument('model', type=str, required=False, default='agglom')

    def get(self, projectID):
        mwd_df = pd.read_sql(projectID, engine)
        args = self.reqparse.parse_args()  # Request arguments
        # If we are doing weighted clustering, multiply the weights to the designated columns. Also
        # Normalize the data via StandardScalar()

        data = modify_data(mwd_df.iloc[:, 1:6], args['data_type'])

        cluster_labels = cluster_data(data, model=args['model'], k=args['k'])
        specific_hole = mwd_df[mwd_df.holeID == args['holeID']]
        idx_depth = specific_hole.Depth.sub(args['depth']).abs().idxmin()
        cluster = cluster_labels[idx_depth]

        same_cluster = mwd_df[cluster_labels == cluster]

        result = same_cluster.to_json(orient='index')
        return result


# Endpoints
# api.add_resource(HolePlots, '/Plots/<string:holeID>/<string:feature>')
api.add_resource(HolePlots, '/Plots/<string:projectID>')
api.add_resource(HoleIDByProject, '/<string:projectID>/GetHoleIDs')
api.add_resource(PlotAllFeatures, '/<string:projectID>/<string:holeID>/AllFeatures')
api.add_resource(PlotAllHoles, '/<string:projectID>/AllPlots')
api.add_resource(Report, '/<string:projectID>/BlastReport')
# api.add_resource(Report, '/<string:projectID>/<string:holeID>/BlastReport')
api.add_resource(Clustering, '/<string:projectID>/Cluster')
api.add_resource(ClusterByBlastEntry, '/<string:projectID>/SharedCluster')

from flask_restful import Resource, reqparse
from flask import jsonify, json
from . import api
from app.main import engine, db
from plotting import plot_rate, plot_clusters, plot_all_features, encode_all_holes, pd
import base64
from ..model.models import EPIROC, BlastReport, BlastCluster


class HolePlots(Resource):
    def get(self, feature, holeID):
        data = pd.read_sql('EPIROC', engine)

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


# Request Parser:
report_parse = reqparse.RequestParser()
# report_parse.add_argument('holeID', type = str, help = 'ID of Hole', required = True)
report_parse.add_argument('depth', type = float, help = 'Depth of the blast in the hole', required = True)
report_parse.add_argument('report', type = str, help = 'Report of Blast', required = True)
report_parse.add_argument('score', type = int, help = 'Rating of the Blast', required = True)


class Report(Resource):
    def get(self, projectID, holeID):
        result = BlastReport.query.get(holeID)
        return result.json()

    def post(self, projectID, holeID):
        args = report_parse.parse_args()
        blast_report = BlastReport(holeID=holeID, depth=args['depth'], report=args['report'], score=args['score'])
        db.session.add(blast_report)
        db.session.commit()
        return blast_report.json()

    def delete(self, projectID, holeID):
        result = BlastReport.query.get(holeID)
        db.session.delete(result)
        db.session.commit()
        return result.json()


class Clustering(Resource):
    ## Get method to send the encoded plots of the 2D clustering
    def get(self, projectID):
        data = pd.read_sql('KMeans_WMDS', engine)
        b64_string = plot_clusters(data)
        response = {'image': b64_string}
        return response


# Used to get entries in the same cluster as the blast
class ClusterByBlastEntry(Resource):
    def get(self, projectID, depth, holeID):
        mwd_df = pd.read_sql(projectID, engine)
        cluster_df = pd.read_sql('KMeans_WMDS', engine)
        specific_hole = cluster_df[cluster_df.holeID == holeID]
        idx_depth = specific_hole.Depth.sub(depth).abs().idxmin()
        cluster = specific_hole.CID.iloc[idx_depth]

        same_cluster = mwd_df[cluster_df.CID == cluster]

        result = same_cluster.to_json(orient='index')
        return result

# Endpoints
api.add_resource(HolePlots, '/Plots/<holeID>/<feature>')
api.add_resource(HoleIDByProject, '/GetHoleIDs/<string:projectID>')
api.add_resource(PlotAllHoles, '/<string:projectID>/AllPlots')
api.add_resource(Report, '/<string:projectID>/<string:holeID>/BlastReport')
api.add_resource(Clustering, '/<string:projectID>/Cluster')
api.add_resource(ClusterByBlastEntry, '/SharedCluster/<string:projectID>/<string:holeID>/<float:depth>')






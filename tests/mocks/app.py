from flask import Flask
from flask import request
import json

from .databricksCluster import MockDBCluster

app = Flask(__name__)
clusters = {}

def get_cluster():
  cluster_id = request.args.get('cluster_id', '')
  if cluster_id == '':
    body = request.get_json()
    if (body and 'cluster_id' in body):
      cluster_id = body['cluster_id']
    else:
      return None

  if cluster_id == '':
    return None

  if not (cluster_id in clusters):
    clusters[cluster_id] = MockDBCluster(cluster_id, 'PENDING', [])

  return clusters.get(cluster_id)

def get_libraries():
  body = request.get_json()
  if (body and 'libraries' in body):
    return body['libraries']
  else:
    return None

@app.route('/api/2.0/libraries/uninstall', methods=['POST'])
def libraries_uninstall():
  cluster = get_cluster()
  libraries = get_libraries()
  if cluster is None or libraries is None:
    return ('', 400)
  cluster.uninstall_library(libraries)
  return {}

@app.route('/api/2.0/libraries/install', methods=['POST'])
def libraries_install():
  cluster = get_cluster()
  libraries = get_libraries()
  if cluster is None or libraries is None:
    return ('', 400)
  cluster.install_library(libraries)
  return {}

@app.route('/api/2.0/libraries/cluster-status')
def libraries_clusterstatus():
  cluster = get_cluster()
  if cluster is None:
    return ('', 400)
  return {'library_statuses': cluster.get_library_statuses()}

@app.route('/api/2.0/clusters/restart', methods=['POST'])
def clusters_restart():
  cluster = get_cluster()
  if cluster is None:
    return ('', 400)
  cluster.restart_cluster(10)
  return {}

@app.route('/api/2.0/clusters/get')
def clusters_get():
  cluster = get_cluster()
  if cluster is None:
    return ('', 400)
  return {'status': cluster.get_status()}

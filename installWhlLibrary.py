# installWhlLibrary.py
#!/usr/bin/python3
import json
import requests
import sys
import getopt
import time

def main():
  workspace = ''
  token = ''
  clusterid = ''
  libs = ''
  dbfspath = ''
  print ('Start to get parameters')
  try:
      opts, args = getopt.getopt(sys.argv[1:], 'hstcld',
                                 ['workspace=', 'token=', 'clusterid=', 'libs=', 'dbfspath='])
  except getopt.GetoptError:
      print(
          'installWhlLibrary.py -s <workspace> -t <token> -c <clusterid> -l <libs> -d <dbfspath>')
      sys.exit(2)

  for opt, arg in opts:
      if opt == '-h':
          print(
              'installWhlLibrary.py -s <workspace> -t <token> -c <clusterid> -l <libs> -d <dbfspath>')
          sys.exit()
      elif opt in ('-s', '--workspace'):
          workspace = arg
      elif opt in ('-t', '--token'):
          token = arg
      elif opt in ('-c', '--clusterid'):
          clusterid = arg
      elif opt in ('-l', '--libs'):
          libs=arg
      elif opt in ('-d', '--dbfspath'):
          dbfspath=arg

  print('-s is ' + workspace)
  print('-t is ' + token)
  print('-c is ' + clusterid)
  print('-l is ' + libs)
  print('-d is ' + dbfspath)

  libslist = libs.split()

  # Uninstall Library if exists on cluster
  i=0
  for lib in libslist:
      dbfslib = dbfspath + lib
      print(dbfslib + ' before:' + getLibStatus(workspace, token, clusterid, dbfslib))

      if (getLibStatus(workspace, token, clusterid, dbfslib) != 'not found'):
          print(dbfslib + " exists. Uninstalling.")
          i = i + 1
          values = {'cluster_id': clusterid, 'libraries': [{'whl': dbfslib}]}

          resp = requests.post(workspace + '/api/2.0/libraries/uninstall', data=json.dumps(values), auth=("token", token))
          runjson = resp.text
          d = json.loads(runjson)
          print(dbfslib + ' after:' + getLibStatus(workspace, token, clusterid, dbfslib))

  # Restart if libraries uninstalled
  if i > 0:
      values = {'cluster_id': clusterid}
      print("Restarting cluster:" + clusterid)
      resp = requests.post(workspace + '/api/2.0/clusters/restart', data=json.dumps(values), auth=("token", token))
      restartjson = resp.text
      print(restartjson)

      p = 0
      waiting = True
      while waiting:
          time.sleep(30)
          clusterresp = requests.get(workspace + '/api/2.0/clusters/get?cluster_id=' + clusterid,
                                 auth=("token", token))
          clusterjson = clusterresp.text
          jsonout = json.loads(clusterjson)
          current_state = jsonout['state']
          print(clusterid + " state:" + current_state)
          if current_state in ['RUNNING','INTERNAL_ERROR', 'SKIPPED'] or p >= 10:
              break
          p = p + 1

  # Install Libraries
  for lib in libslist:
      dbfslib = dbfspath + lib
      print("Installing " + dbfslib)
      values = {'cluster_id': clusterid, 'libraries': [{'whl': dbfslib}]}

      resp = requests.post(workspace + '/api/2.0/libraries/install', data=json.dumps(values), auth=("token", token))
      runjson = resp.text
      d = json.loads(runjson)
      print(dbfslib + ' after:' + getLibStatus(workspace, token, clusterid, dbfslib))


def getLibStatus(workspace, token, clusterid, dbfslib):
  resp = requests.get(workspace + '/api/2.0/libraries/cluster-status?cluster_id='+ clusterid, auth=("token", token))
  libjson = resp.text
  d = json.loads(libjson)
  if (d.get('library_statuses')):
      statuses = d['library_statuses']

      for status in statuses:
          if (status['library'].get('whl')):
              if (status['library']['whl'] == dbfslib):
                  return status['status']
              else:
                  return "not found"
  else:
      # No libraries found
      return "not found"

if __name__ == '__main__':
  print("Start")
  main()
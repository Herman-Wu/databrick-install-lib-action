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

  libslist = libs.split(',')

  # Uninstall Library if exists on cluster
  i=0
  for lib in libslist:
      dbfslib = dbfspath + lib
      status = getLibStatus(workspace, token, clusterid, dbfslib)
      print('uninstall: ' + dbfslib + ' before: ' + status)

      if (status != 'not found'):
          print('uninstall: ' + dbfslib + ' exists. uninstalling.')
          i = i + 1
          values = {'cluster_id': clusterid, 'libraries': [{'whl': dbfslib}]}
          print('uninstall: ' + dbfslib + ' payload: ' + json.dumps(values))

          resp = requests.post(workspace + '/api/2.0/libraries/uninstall', json=values, auth=('token', token))
          print('uninstall: ' + dbfslib + ' response: ' + resp.text)
          print('uninstall: ' + dbfslib + ' after: ' + getLibStatus(workspace, token, clusterid, dbfslib))

  # Restart if libraries uninstalled
  if i > 0:
      values = {'cluster_id': clusterid}
      print('restarting cluster ' + clusterid)
      resp = requests.post(workspace + '/api/2.0/clusters/restart', json=values, auth=('token', token))
      print('restarting cluster ' + clusterid + ' response: ' + resp.text)

      p = 0
      waiting = True
      while waiting:
          time.sleep(10)
          clusterresp = requests.get(workspace + '/api/2.0/clusters/get?cluster_id=' + clusterid,
                                 auth=('token', token))
          clusterjson = clusterresp.text
          jsonout = json.loads(clusterjson)
          current_state = jsonout['state']
          print('restarting cluster ' + clusterid +  ' state:' + current_state)
          if current_state in ['RUNNING','INTERNAL_ERROR', 'SKIPPED'] or p >= 10:
              break
          p = p + 1

  # Install Libraries
  for lib in libslist:
      dbfslib = dbfspath + lib
      print('install: ' + dbfslib + ' before: ' + getLibStatus(workspace, token, clusterid, dbfslib))
      values = {'cluster_id': clusterid, 'libraries': [{'whl': dbfslib}]}
      print('install: ' + dbfslib + ' payload: ' + json.dumps(values))

      resp = requests.post(workspace + '/api/2.0/libraries/install', json=values, auth=('token', token))
      print('install: ' + dbfslib + ' response: ' + resp.text)
      status = getLibStatus(workspace, token, clusterid, dbfslib)
      print('install: ' + dbfslib + ' after: ' + status)
      if (status == 'not found'):
          raise Exception('install: failed to install library ' + dbfslib)


def getLibStatus(workspace, token, clusterid, dbfslib):
  resp = requests.get(workspace + '/api/2.0/libraries/cluster-status?cluster_id='+ clusterid, auth=('token', token))
  print('getlibstatus response: ' + resp.text)

  libjson = resp.text
  d = json.loads(libjson)
  if (d.get('library_statuses')):
      statuses = d['library_statuses']

      for status in statuses:
          if (status['library'].get('whl')):
              print('getlibstatus checking: ' + dbfslib + ' is equal to ' + status['library']['whl'])
              if (status['library']['whl'] == dbfslib):
                  return status['status']
  return 'not found'

if __name__ == '__main__':
  print('Start')
  main()
import time

class MockDBCluster:
  __cluster_id = 0
  __current_state = ''
  __installed_libraries = []
  __installed_libraries_after_restart = []
  __state_running_from = 0

  def __init__(self, cluster_id, init_state, init_libraries):
    self.__cluster_id = cluster_id
    self.__current_state = init_state
    self.__installed_libraries = init_libraries

  def __isInstalled(self, library):
    for l in self.__installed_libraries:
      if l == library:
        return True
    return False

  def __isInstalledAfterRestart(self, library):
    for l in self.__installed_libraries_after_restart:
      if l == library:
        return True
    return  False

  def install_library(self, libraries):
    for library in libraries:
      if not self.__isInstalled(library):
        self.__installed_libraries.append(library)
      if not self.__isInstalledAfterRestart(library):
        self.__installed_libraries_after_restart.append(library)

  def get_library_statuses(self):
    libs = []
    for l in self.__installed_libraries:
      libs.append({'library': l, 'status': 'installed'})
    return libs

  def uninstall_library(self, libraries):
    for library in libraries:
      if self.__isInstalled(library):
        self.__installed_libraries_after_restart.remove(library)

  def get_status(self):
    current_ts = time.time()
    if (current_ts > self.__state_running_from):
      self.__current_state = 'RUNNING'
    else:
      self.__current_state = 'PENDING'
    return self.__current_state

  def restart_cluster(self, restart_takes_seconds):
    self.__current_state = 'PENDING'
    self.__installed_libraries = self.__installed_libraries_after_restart.copy()
    self.__state_running_from = time.time() + restart_takes_seconds
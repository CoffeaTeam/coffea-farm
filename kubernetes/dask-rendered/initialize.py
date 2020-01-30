#!/usr/bin/env python3
from distributed import (
    Client,
    SchedulerPlugin,
    WorkerPlugin,
    get_worker,
)
import os
import sys
import time


class WorkerJumpAssignment(SchedulerPlugin):
    def __init__(self, workers=[]):
        self._workers = workers

    def add_worker(self, scheduler=None, worker=None, **kwargs):
        try:
            # cluster shrank and now is regrowing, insert in first empty slot
            index = self._workers.index(None)
            self._workers[index] = worker
        except ValueError:
            # cluster is expanding
            self._workers.append(worker)

    def remove_worker(self, scheduler=None, worker=None, **kwargs):
        try:
            index = self._workers.index(worker)
            self._workers[index] = None
        except ValueError:
            # invalid state, what do we do?
            raise

    def get_jump_mapping(self):
        out = {}
        for i, worker in enumerate(self._workers):
            if all(w is None for w in self._workers[i:]):
                break
            out[i] = worker
        return out


class ConfigureXRootD(WorkerPlugin):
    name = 'user_proxy'

    def __init__(self, proxy_file=None):
        '''
        If proxy_file is None, look for it in default location
        '''
        file = os.environ.get('X509_USER_PROXY', '/tmp/x509up_u%d' % os.getuid())
        self._proxy = open(file, 'rb').read()

    def setup(self, worker):
        self._location = os.path.join(worker.local_directory, 'userproxy')
        with open(self._location, 'wb') as fout:
            fout.write(self._proxy)
        os.environ['X509_USER_PROXY'] = self._location
        os.environ['XRD_CONNECTIONWINDOW'] = '10'
        os.environ['XRD_STREAMTIMEOUT'] = '10'
        os.environ['XRD_TIMEOUTRESOLUTION'] = '2'
        os.environ['XRD_WORKERTHREADS'] = '4'
        os.environ['XRD_REQUESTTIMEOUT'] = '60'

    def teardown(self, worker):
        os.remove(self._location)
        del os.environ['X509_USER_PROXY']


class DistributeZipball(WorkerPlugin):
    def __init__(self, zipfile):
        self._fname = os.path.basename(zipfile)
        self._code = open(zipfile, 'rb').read()

    def setup(self, worker):
        self._location = os.path.join(worker.local_directory, self._fname)
        self._pathstr = os.path.join(self._location, self._fname.replace('.zip', ''))
        with open(self._location, 'wb') as fout:
            fout.write(self._code)
        sys.path.insert(0, self._pathstr)

    def teardown(self, worker):
        os.remove(self._location)
        sys.path.remove(self._pathstr)


class InstallPackage(WorkerPlugin):
    def __init__(self, name):
        self.name = name

    def setup(self, worker):
        import os, sys, subprocess
        installdir = os.path.join(os.path.dirname(worker.local_directory), '.local')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--prefix', installdir, self.name])
        sitepackages = os.path.join(installdir, 'lib', 'python' + sys.version[:3], 'site-packages')
        if sitepackages not in sys.path:
            sys.path.insert(0, sitepackages)

    def teardown(self, worker):
        pass


client = Client(os.environ['DASK_SCHEDULER'])
plugins = set()
for p in client.run(lambda: set(get_worker().plugins)).values():
    plugins |= p
print("Current plugins:", plugins)

if 'user_proxy' not in plugins:
    client.register_worker_plugin(ConfigureXRootD(), 'user_proxy')

if 'boostedhiggs' not in plugins:
    client.register_worker_plugin(InstallPackage('https://github.com/nsmith-/boostedhiggs/archive/dev.zip'), 'boostedhiggs')

if 'cache' not in plugins:
    from coffea.processor.dask import ColumnCacheHolder
    client.register_worker_plugin(ColumnCacheHolder(), 'cache')

if False:
    jump_assignment = WorkerJumpAssignment()
    def put(dask_scheduler=None):
        dask_scheduler.add_plugin(WorkerJumpAssignment(list(dask_scheduler.workers.keys())))

    def get(dask_scheduler=None):
        for p in dask_scheduler.plugins:
            try:
                return p.get_jump_mapping()
            except AttributeError:
                pass

    client.run_on_scheduler(put)

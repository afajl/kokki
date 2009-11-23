
__all__ = ["DebianServiceProvider"]

import subprocess

from pluto.base import Fail
from pluto.providers import Provider

class DebianServiceProvider(Provider):
    def action_start(self):
        if not self.status():
            self._init_cmd("start", 0)
            self.updated()

    def action_stop(self):
        if self.status():
            self._init_cmd("stop", 0)
            self.updated()

    def action_restart(self):
        self._init_cmd("restart", 0)

    def action_reload(self):
        self._init_cmd("reload", 0)

    def status(self):
        return self._init_cmd("status") == 0

    def _init_cmd(self, command, expect=None):
        ret = subprocess.call(["/etc/init.d/%s" % self.resource.service_name, command],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if expect is not None and expect != ret:
            raise Fail("%r command %s for service %s failed" % (self, command, self.resource.service_name))
        return ret

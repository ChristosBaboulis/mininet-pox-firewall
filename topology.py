#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import RemoteController


class part1_topo(Topo):
    def build(self):
        switch1 = self.addSwitch('s1')
        for i in range(1, 6):
            host = self.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
            self.addLink(host, switch1)


topos = {"part1": part1_topo}

if __name__ == "__main__":
    t = part1_topo()
    net = Mininet(topo=t, controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6653))
    net.start()
    CLI(net)
    net.stop()

# Part 2 
# based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, arp, udp

log = core.getLogger()


class Firewall(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        log.info("Firewall activated on %s", connection)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        # Αποδοχή ARP - flood
        if packet.type == ethernet.ARP_TYPE:
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.in_port = event.port
            self.connection.send(msg)
            log.debug("Allowed ARP packet (flood)")
            return

        # Αν είναι IPv4
        if packet.type == ethernet.IP_TYPE:
            ip_packet = packet.payload

            # Αν είναι UDP -> forward
            if isinstance(ip_packet.payload, udp):
                # Εύρεση port εξόδου
                dst_ip = str(ip_packet.dstip)
                dst_host = dst_ip.split('.')[-1]  # π.χ. '10.0.0.3' → '3'
                out_port = int(dst_host)  # Γιατί το h3 είναι στη port 3

                # Εγκατάσταση κανόνα στο switch
                msg = of.ofp_flow_mod()
                msg.match.dl_type = 0x0800  # IPv4
                msg.match.nw_proto = 17     # UDP
                msg.match.nw_dst = ip_packet.dstip
                msg.priority = 20  # Προτεραιότητα πάνω από το drop rule
                msg.actions.append(of.ofp_action_output(port=out_port))
                self.connection.send(msg)

                # Εκτέλεση για αυτό το πακέτο
                msg = of.ofp_packet_out()
                msg.data = event.ofp
                msg.actions.append(of.ofp_action_output(port=out_port))
                msg.in_port = event.port
                self.connection.send(msg)
                log.debug("Allowed UDP packet to %s (port %d)", dst_ip, out_port)
                return

            # Άλλο IPv4 πρωτόκολλο → drop
            msg = of.ofp_flow_mod()
            msg.match.dl_type = 0x0800
            msg.priority = 10
            self.connection.send(msg)
            log.debug("Dropped non-UDP IPv4 packet")
            return

        # Οτιδήποτε άλλο → drop (χωρίς εγκατάσταση rule)
        log.debug("Dropped unknown packet type: %s", packet.type)
        return


def launch():
    def start_switch(event):
        log.info("Controlling %s", event.connection)
        Firewall(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)

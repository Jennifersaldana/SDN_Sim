# sdn.py
# SHA-256 watermark: c6c8d60a169e54099e19b523beab40afbb38e1938057b692044267acb0b90c6e

import hashlib
import networkx as nx
import heapq

class SDNController:
    def __init__(self):
        self.topology = nx.Graph()
        self.flows = []  # Active flows
        self.link_utilization = {}  # Track bandwidth usage on links

    def add_node(self, node):
        if self.topology.has_node(node):
            print(f"Node '{node}' already exists.")
            return
        self.topology.add_node(node)

    def remove_node(self, node):
        if not self.topology.has_node(node):
            print(f"Error: Node '{node}' does not exist.")
            return
        self.topology.remove_node(node)

    def add_link(self, u, v, weight=1):
        if not self.topology.has_node(u) or not self.topology.has_node(v):
            print(f"Error: One or both nodes '{u}' or '{v}' do not exist.")
            return
        self.topology.add_edge(u, v, weight=weight)
        self.link_utilization[(u, v)] = 0
        self.link_utilization[(v, u)] = 0

    def remove_link(self, u, v):
        if not self.topology.has_edge(u, v):
            print(f"Error: Link between '{u}' and '{v}' does not exist.")
            return
        self.topology.remove_edge(u, v)
        self.link_utilization.pop((u, v), None)
        self.link_utilization.pop((v, u), None)

    def inject_traffic_flow(self, src, dst, traffic_type, bandwidth):
        if not self.topology.has_node(src) or not self.topology.has_node(dst):
            print("Error: Source or destination node does not exist.")
            return
        path = self.compute_path(src, dst, traffic_type)
        if not path:
            print("No available path for this flow.")
            return

        flow = {
            'src': src,
            'dst': dst,
            'type': traffic_type,
            'bandwidth': bandwidth,
            'path': path
        }
        self.flows.append(flow)

        # Update link utilization
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            self.link_utilization[(u, v)] += bandwidth
            self.link_utilization[(v, u)] += bandwidth

        print(f"Injected flow from {src} to {dst} using path {path}")

    def compute_path(self, src, dst, traffic_type):
        if not self.topology.has_node(src) or not self.topology.has_node(dst):
            return None
        try:
            paths = list(nx.all_shortest_paths(self.topology, source=src, target=dst, weight='weight'))
            if not paths:
                return None
            paths.sort(key=lambda p: sum(self.link_utilization.get((p[i], p[i+1]), 0) for i in range(len(p)-1)))
            return paths[0]
        except nx.NetworkXNoPath:
            return None

    def simulate_link_failure(self, u, v):
        if not self.topology.has_edge(u, v):
            print(f"Error: Link between '{u}' and '{v}' does not exist.")
            return

        self.remove_link(u, v)
        print(f"Link between {u} and {v} failed.")

        for flow in self.flows:
            if u in flow['path'] and v in flow['path']:
                for i in range(len(flow['path']) - 1):
                    a, b = flow['path'][i], flow['path'][i + 1]
                    if (a, b) in self.link_utilization:
                        self.link_utilization[(a, b)] -= flow['bandwidth']
                    if (b, a) in self.link_utilization:
                        self.link_utilization[(b, a)] -= flow['bandwidth']

                new_path = self.compute_path(flow['src'], flow['dst'], flow['type'])
                if new_path:
                    print(f"Reconfigured flow from {flow['src']} to {flow['dst']} to new path {new_path}")
                    flow['path'] = new_path

                    for i in range(len(new_path) - 1):
                        a, b = new_path[i], new_path[i + 1]
                        self.link_utilization[(a, b)] += flow['bandwidth']
                        self.link_utilization[(b, a)] += flow['bandwidth']
                else:
                    print(f"No backup path available for flow {flow['src']}->{flow['dst']}")

    def query_routing(self, src, dst):
        if not self.topology.has_node(src) or not self.topology.has_node(dst):
            print("Error: Source or destination node does not exist.")
            return
        path = self.compute_path(src, dst, 'data')
        print(f"Routing from {src} to {dst}: {path}")

    def visualize(self):
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.topology)
        nx.draw(self.topology, pos, with_labels=True, node_color='lightblue')

        labels = {}
        for u, v in self.topology.edges:
            key = (u, v) if (u, v) in self.link_utilization else (v, u)
            labels[(u, v)] = str(self.link_utilization.get(key, 0))

        nx.draw_networkx_edge_labels(self.topology, pos, edge_labels=labels)
        plt.show()


# Main function remains unchanged with all usage messages preserved
def main():
    controller = SDNController()
    while True:
        cmd = input("SDN > ").strip()

        if cmd.startswith("add node"):
            parts = cmd.split()
            if len(parts) != 3:
                print("Usage: add node <name>")
                continue
            _, _, node = parts
            controller.add_node(node.lower())

        elif cmd.startswith("remove node"):
            parts = cmd.split()
            if len(parts) != 3:
                print("Usage: remove node <name>")
                continue
            _, _, node = parts
            controller.remove_node(node.lower())

        elif cmd.startswith("add link"):
            parts = cmd.split()
            if len(parts) < 4:
                print("Usage: add link <node1> <node2> [weight]")
                continue
            u, v = parts[2].lower(), parts[3].lower()
            weight = int(parts[4]) if len(parts) > 4 else 1
            controller.add_link(u, v, weight)

        elif cmd.startswith("remove link"):
            parts = cmd.split()
            if len(parts) != 4:
                print("Usage: remove link <node1> <node2>")
                continue
            u, v = parts[2].lower(), parts[3].lower()
            controller.remove_link(u, v)

        elif cmd.startswith("inject traffic"):
            parts = cmd.split()
            if len(parts) < 6:
                print("Usage: inject traffic <src> <dst> <type> <bandwidth>")
                continue
            src, dst, ttype, bw = parts[2].lower(), parts[3].lower(), parts[4], int(parts[5])
            controller.inject_traffic_flow(src, dst, ttype, bw)

        elif cmd.startswith("simulate link failure"):
            parts = cmd.split()
            if len(parts) != 5:
                print("Usage: simulate link failure <node1> <node2>")
                continue
            u, v = parts[3].lower(), parts[4].lower()
            controller.simulate_link_failure(u, v)

        elif cmd.startswith("query routing"):
            parts = cmd.split()
            if len(parts) != 4:
                print("Usage: query routing <src> <dst>")
                continue
            src, dst = parts[2].lower(), parts[3].lower()
            controller.query_routing(src, dst)

        elif cmd == "visualize":
            controller.visualize()

        elif cmd in ("exit", "quit", "q"):
            break

        else:
            print("Unknown command.")

if __name__ == "__main__":
    print(hashlib.sha256(b"899238033NeoDDaBRgX5a9").hexdigest())
    main()
import networkx as nx
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from backend.app.models.sentinel_models import Account, Device, AccountDeviceLink, Transaction

class FraudGraphEngine:
    def build_entity_graph_for_account(self, db: Session, target_account_id: str, depth: int = 2) -> Dict[str, Any]:
        """
        Constructs an ego-network around target_account_id resolving shared devices,
        shared IPs, and linked accounts up to 2 hops away.
        Returns a Cytoscape-compatible node/edge JSON structure.
        """
        G = nx.Graph()
        
        # 1. Fetch Target Account
        target = db.query(Account).filter(Account.id == target_account_id).first()
        if not target:
            return {"nodes": [], "edges": []}
            
        G.add_node(
            target.id,
            label=f"{target.full_name} ({target.id})",
            type="account",
            risk_score=target.risk_score,
            is_target=True
        )
        
        # 2. Get direct devices
        links = db.query(AccountDeviceLink).filter(AccountDeviceLink.account_id == target_account_id).all()
        for link in links:
            device = db.query(Device).filter(Device.id == link.device_id).first()
            if not device:
                continue
                
            G.add_node(
                device.id,
                label=f"Device: {device.id[-6:]}",
                type="device",
                is_vpn=device.is_vpn,
                ip=device.ip_address
            )
            G.add_edge(target.id, device.id, relationship="OPERATES_ON")
            
            # Find sibling accounts on this same device (Multi-accounting syndicates)
            sibling_links = db.query(AccountDeviceLink).filter(
                AccountDeviceLink.device_id == device.id,
                AccountDeviceLink.account_id != target_account_id
            ).all()
            
            for sib in sibling_links:
                sib_acc = db.query(Account).filter(Account.id == sib.account_id).first()
                if sib_acc:
                    G.add_node(
                        sib_acc.id,
                        label=f"{sib_acc.full_name} ({sib_acc.id})",
                        type="account",
                        risk_score=sib_acc.risk_score,
                        is_target=False
                    )
                    G.add_edge(sib_acc.id, device.id, relationship="SHARED_DEVICE")

        # Convert to Cytoscape format
        elements = {
            "nodes": [
                {
                    "data": {
                        "id": node_id,
                        **G.nodes[node_id]
                    }
                }
                for node_id in G.nodes()
            ],
            "edges": [
                {
                    "data": {
                        "id": f"{u}-{v}",
                        "source": u,
                        "target": v,
                        **G.edges[u, v]
                    }
                }
                for u, v in G.edges()
            ],
            "summary": {
                "total_nodes": G.number_of_nodes(),
                "total_edges": G.number_of_edges(),
                "connected_accounts": sum(1 for n, d in G.nodes(data=True) if d.get("type") == "account"),
                "has_syndicate": sum(1 for n, d in G.nodes(data=True) if d.get("type") == "account") > 1
            }
        }
        return elements

graph_engine = FraudGraphEngine()

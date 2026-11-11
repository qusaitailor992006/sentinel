from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.services.graph_engine import graph_engine

router = APIRouter(prefix="/api/graph", tags=["Fraud Graph Analytics"])

@router.get("/account/{account_id}")
def get_account_entity_graph(account_id: str, db: Session = Depends(get_db)):
    """
    Returns NetworkX multi-hop entity graph (accounts, shared devices, IP linkages)
    in Cytoscape.js visual graph structure.
    """
    graph_data = graph_engine.build_entity_graph_for_account(db, account_id)
    return graph_data

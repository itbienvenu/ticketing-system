from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.dbs import get_db
from database.models import RouteSegment, Route, BusStation, Company
from schemas.RouteSegmentScheme import RouteSegmentCreate, RouteSegmentUpdate, RouteSegmentResponse
from methods.functions import get_current_user

router = APIRouter(prefix="/route_segments", tags=["RouteSegments"])

# Create a new route segment
@router.post("/", response_model=RouteSegmentResponse)
def create_route_segment(segment: RouteSegmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Check route exists and belongs to user's company
    route = db.query(Route).filter(Route.id == segment.route_id, Route.company_id == current_user.company_id).first()
    if not route:
        raise HTTPException(404, "Route not found")

    # Check start and end stations exist
    start_station = db.query(BusStation).filter(BusStation.id == segment.start_station_id, BusStation.company_id == current_user.company_id).first()
    end_station = db.query(BusStation).filter(BusStation.id == segment.end_station_id, BusStation.company_id == current_user.company_id).first()
    if not start_station or not end_station:
        raise HTTPException(404, "One or both stations not found")

    new_segment = RouteSegment(
        route_id=segment.route_id,
        start_station_id=segment.start_station_id,
        end_station_id=segment.end_station_id,
        price=segment.price,
        stop_order=segment.stop_order,
        company_id=current_user.company_id
    )
    db.add(new_segment)
    db.commit()
    db.refresh(new_segment)
    return new_segment

# List all segments (optional: filter by route)
@router.get("/", response_model=List[RouteSegmentResponse])
def list_route_segments(route_id: str = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(RouteSegment).filter(RouteSegment.company_id == current_user.company_id)
    if route_id:
        query = query.filter(RouteSegment.route_id == route_id)
    return query.all()

# Get a single segment
@router.get("/{segment_id}", response_model=RouteSegmentResponse)
def get_route_segment(segment_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    segment = db.query(RouteSegment).filter(RouteSegment.id == segment_id, RouteSegment.company_id == current_user.company_id).first()
    if not segment:
        raise HTTPException(404, "Route segment not found")
    return segment

# Update a segment
@router.put("/{segment_id}", response_model=RouteSegmentResponse)
def update_route_segment(segment_id: str, segment_update: RouteSegmentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    segment = db.query(RouteSegment).filter(RouteSegment.id == segment_id, RouteSegment.company_id == current_user.company_id).first()
    if not segment:
        raise HTTPException(404, "Route segment not found")

    segment.start_station_id = segment_update.start_station_id
    segment.end_station_id = segment_update.end_station_id
    segment.price = segment_update.price
    segment.stop_order = segment_update.stop_order
    db.commit()
    db.refresh(segment)
    return segment

# Delete a segment
@router.delete("/{segment_id}")
def delete_route_segment(segment_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    segment = db.query(RouteSegment).filter(RouteSegment.id == segment_id, RouteSegment.company_id == current_user.company_id).first()
    if not segment:
        raise HTTPException(404, "Route segment not found")

    db.delete(segment)
    db.commit()
    return {"message": "Route segment deleted successfully"}

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, asc, desc
from sqlalchemy import cast, Float
from db import get_db
from models import Airnb
import math

app = FastAPI()

@app.get("/listings_airnb")
async def get_listings(
    session: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Halaman keberapa"),
    limit: int = Query(10, ge=1, le=100, description="Jumlah item per halaman"),
    neighbourhood_group: str = Query(None, description="Filter berdasarkan neighbourhood_group"),
    price_lte: float = Query(None, gt=0, le=1000000, description="Filter harga maksimal"),
    host_name: str = Query(None, description="Filter berdasarkan nama host"),
    sort_by: str = Query("id", description="Kolom untuk sorting (id,name,price,number_of_reviews)"),
    order: str = Query("asc", description="Urutan sorting: asc / desc")
):
    try:
        # Validasi parameter sort_by dan order
        valid_sort_columns = ["id", "name", "price", "number_of_reviews"]
        valid_orders = ["asc", "desc"]

        if sort_by not in valid_sort_columns:
            raise HTTPException(status_code=400, detail="Invalid value for sort_by parameter")
        
        if order not in valid_orders:
            raise HTTPException(status_code=400, detail="Invalid value for order parameter")

        query = select(Airnb)
        filters = []

        # Filter berdasarkan neighbourhood_group (case-insensitive)
        if neighbourhood_group:
            filters.append(func.lower(Airnb.neighbourhood).like(f"%{neighbourhood_group.lower()}%"))

        # Filter harga maksimal
        if price_lte is not None:
            filters.append(cast(Airnb.price, Float) <= price_lte)

        # Filter berdasarkan host_name (case-insensitive)
        if host_name:
            filters.append(func.lower(Airnb.host_name).like(f"%{host_name.lower()}%"))

        # Gabungkan semua filter
        if filters:
            query = query.filter(and_(*filters))

        # Sorting
        sort_column = getattr(Airnb, sort_by, None)
        if sort_column is not None:
            if order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

        # Pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await session.execute(query)
        data = result.scalars().all()

        # Hitung total data untuk pagination dengan filter yang sama
        count_query = select(func.count(Airnb.id)).filter(and_(*filters))
        total_count = await session.execute(count_query)
        total_count = total_count.scalar()

        # Hitung jumlah halaman total
        total_pages = math.ceil(total_count / limit)

        # Format data untuk response JSON
        listings = []
        for item in data:
            listings.append({
                "id": item.id,
                "name": item.name,
                "host_name": item.host_name,
                "neighbourhood_group": item.neighbourhood_group,
                "neighbourhood": item.neighbourhood,
                "price": item.price,
                "number_of_reviews": item.number_of_reviews,
                "last_review": item.last_review,
                "reviews_per_month": item.reviews_per_month,
            })

        return {
            "status": "success",
            "message": "Data fetched successfully",
            "page": page,
            "total_pages": total_pages,
            "data": listings
        }

    except HTTPException as e:
        # Menangani error 400
        raise e
    except Exception as e:
        # Menangani error 500
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
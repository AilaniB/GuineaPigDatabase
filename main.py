from multiprocessing.sharedctypes import synchronized

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated

from starlette.status import HTTP_204_NO_CONTENT

import models
from models import guinea_pigs, foster, customer
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

app = FastAPI()

models.guinea_pigs.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

class GuineaPigBase(BaseModel):
    id: int
    name: str
    age: int
    bonded: bool
    foster_id: int
    customer_id: int

class FosterBase(BaseModel):
    id: int
    name: str
    age: int
    email: str
    phone_number: str
    address: str

class CustomerBase(BaseModel):
    id: int
    name: str
    age: int
    email: str
    phone_number: str
    address: str


@app.post("/guinea_pig/", status_code=status.HTTP_201_CREATED, tags=["GuineaPig"])
async def create_guinea_pig(guinea_pig: GuineaPigBase, db: db_dependency):
    db_guinea_pig = models.guinea_pigs.GuineaPig(**guinea_pig.model_dump())
    db.add(db_guinea_pig)
    db.commit()
    return {"detail": "Guinea Pig added successfully"}

@app.get("/guinea_pig/", status_code=status.HTTP_200_OK, tags=["GuineaPig"])
async def get_guinea_pigs(db: db_dependency):
    return db.query(models.guinea_pigs.GuineaPig).all()

@app.put("/guinea_pig/{guinea_pig_id}", response_model=GuineaPigBase,
         status_code=status.HTTP_200_OK, tags=["GuineaPig"])
async def update_guinea_pig(guinea_pig_id: int, guinea_pig_request: GuineaPigBase, db: db_dependency):
    db_guinea_pig = db.query(models.guinea_pigs.GuineaPig).filter(models.guinea_pigs.GuineaPig.id == guinea_pig_id)
    if db_guinea_pig.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guinea Pig not found.")

    update_data = guinea_pig_request.model_dump(exclude_unset=True)

    db_guinea_pig.update(update_data, synchronize_session=False)
    db.commit()

    return db_guinea_pig.first()

@app.delete("/guinea_pig/{guinea_pig_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["GuineaPig"])
async def delete_guinea_pig(guinea_pig_id: int, db: db_dependency):
    db_guinea_pig = (db.query(models.guinea_pigs.GuineaPig).filter
                     (models.guinea_pigs.GuineaPig.id == guinea_pig_id).first())
    if db_guinea_pig is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guinea Pig not found.")

    db.delete(db_guinea_pig)
    db.commit()

@app.get("/fosters/", status_code=status.HTTP_200_OK, tags=["Foster"])
async def get_fosters(db: db_dependency):
    return db.query(models.foster.Foster).all()

@app.post("/fosters/", status_code=status.HTTP_201_CREATED, tags=["Foster"])
async def create_foster(single_foster: FosterBase, db: db_dependency):
    db_foster = models.foster.Foster(**single_foster.model_dump())
    db.add(db_foster)
    db.commit()

    return {"detail": "Foster added successfully"}

@app.put("/foster/{foster_id}", response_model=FosterBase, status_code=status.HTTP_200_OK, tags=["Foster"])
async def update_foster(foster_id: int, foster_request: FosterBase, db: db_dependency):
    db_foster = db.query(models.foster.Foster).filter(models.foster.Foster.id == foster_id).first()
    if db_foster is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foster not found.")

    update_data = foster_request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_foster, key, value)

    db.commit()
    db.refresh(db_foster)

    return db_foster

@app.delete("/foster/{foster_id}", status_code=HTTP_204_NO_CONTENT, tags=["Foster"])
async def delete_foster(foster_id: int, db: db_dependency):
    db_foster = (db.query(models.foster.Foster).filter
                 (models.foster.Foster.id == foster_id).first())

    if db_foster is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foster not found.")

    db.delete(db_foster)
    db.commit()

@app.get("/fosters_count", status_code=status.HTTP_200_OK, tags=["Foster"])
async def get_fosters_count(db: db_dependency):
    count_result = db.query(func.count(models.foster.Foster.id)).scalar()
    return {"foster_count": count_result}

@app.post("/customer/", status_code=status.HTTP_201_CREATED, tags=["Customer"])
async def create_customer(customer: CustomerBase, db: db_dependency):
    db_customer = models.customer.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    return {"detail": "Customer added successfully"}

@app.get("/customer/", status_code=status.HTTP_200_OK, tags=["Customer"])
async def get_customers(db: db_dependency):
    return db.query(models.customer.Customer).all()

@app.put("/customer/{customer_id}", response_model=CustomerBase, status_code=status.HTTP_200_OK, tags=["Customer"])
async def update_customer(customer_id: int, customer_request: CustomerBase, db: db_dependency):
    db_customer = db.query(models.customer.Customer).filter(models.customer.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    update_data = customer_request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer

@app.delete("/customer/{customer_id}", status_code=HTTP_204_NO_CONTENT, tags=["Customer"])
async def delete_customer(customer_id: int, db: db_dependency):
    db_customer = (db.query(models.customer.Customer).filter
                   (models.customer.Customer.id == customer_id).first())

    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    db.delete(db_customer)
    db.commit()

@app.get("/guinea_pig_customer_by_id/", status_code=status.HTTP_200_OK, tags=["GuineaPig-Customer"])
async def get_guinea_pig_customer_by_id(guinea_pig_name: str, customer_id: int, db: db_dependency):
    db_guinea_pig_customer = (
        db.query(models.customer.Customer)
        .join(models.guinea_pigs.GuineaPig)
        .filter(models.guinea_pigs.GuineaPig.name == guinea_pig_name,
                models.guinea_pigs.GuineaPig.customer_id == customer_id)
        .all()
    )

    return db_guinea_pig_customer

@app.get("/guinea_pig_foster_by_id/", status_code=status.HTTP_200_OK, tags=["GuineaPig-Foster"])
async def get_guinea_pig_foster_by_id(guinea_pig_name: str, foster_id: int, db: db_dependency):
    db_guinea_pig_foster = (
        db.query(models.foster.Foster)
        .join(models.guinea_pigs.GuineaPig)
        .filter(models.guinea_pigs.GuineaPig.name == guinea_pig_name,
                models.guinea_pigs.GuineaPig.foster_id == foster_id)
        .all()
    )

    return db_guinea_pig_foster

@app.get("/foster_guinea_pig_by_id/", status_code=status.HTTP_200_OK, tags=["Foster-GuineaPig"])
async def get_foster_guinea_pig_by_id(foster_id: int, db: db_dependency):
    db_foster_guinea_pigs = (
        db.query(models.guinea_pigs.GuineaPig)
        .join(models.foster.Foster)
        .filter(models.foster.Foster.id == foster_id)
        .all()
    )

    return [
        {
            "guinea_pig_name" : guineapig.name,
            "guinea_pig_age" : guineapig.age,
        }
        for guineapig in db_foster_guinea_pigs
    ]

@app.get("/customer_guinea_pig_by_id/", status_code=status.HTTP_200_OK, tags=["Customer-GuineaPig"])
async def get_customer_guinea_pig_by_id(customer_id: int, db: db_dependency):
    db_customer_guinea_pigs = (
        db.query(models.guinea_pigs.GuineaPig)
        .join(models.customer.Customer)
        .filter(models.customer.Customer.id == customer_id)
        .all()
    )

    return [
        {
            "guinea_pig_name" : guineapig.name,
            "guinea_pig_age" : guineapig.age,
        }
        for guineapig in db_customer_guinea_pigs
    ]

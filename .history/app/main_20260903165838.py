# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.routers.auth as auth
import app.routers.category as category
import app.routers.customer as customer
import app.routers.payment as payment
import app.routers.product as product
import app.routers.receipt as receipt
import app.routers.sale as sale
import app.routers.sale_item as sale_item
import app.routers.supplier as supplier
import app.routers.user as user

app = FastAPI(
    title="Hospital Pharmacy POS System",
    description="Point of Sale System for Hospital and Pharmacy Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(customer.router)
app.include_router(payment.router)
app.include_router(product.router)
app.include_router(receipt.router)
app.include_router(sale.router)
app.include_router(sale_item.router)
app.include_router(supplier.router)
app.include_router(user.router)

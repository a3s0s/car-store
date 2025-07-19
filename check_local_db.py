#!/usr/bin/env python3
from app import create_app
from models import Car

app = create_app()

with app.app_context():
    cars = Car.query.all()
    print(f"Found {len(cars)} cars in local database:")
    print("=" * 50)
    
    for car in cars:
        print(f"ID: {car.id}")
        print(f"Name: {car.name}")
        print(f"Brand: {car.brand}")
        print(f"Model: {car.model}")
        print(f"Year: {car.year}")
        print(f"Price: {car.price}")
        print(f"Image: {car.image_url}")
        print("-" * 30)
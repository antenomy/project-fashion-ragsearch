
# app = FastAPI()
# print("test")



# # === Database === #

# @app.get('/db-get-all')
# async def db_get_all():
#     db = SessionLocal()

#     try:
#         items = db.query(Measurement).all()
#         return [measurement_to_json(item) for item in items]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()

# @app.post('/db-insert')
# async def db_insert(measurement: MeasurementCreate):
#     db = SessionLocal()

#     try: 
#         new_measurement = Measurement(
#             measurement_one = round(measurement.measurement_one, 1),
#             measurement_two = round(measurement.measurement_two, 1),
#             result = round(measurement.result, 1),
#             creation_date = measurement.creation_date
#         )
#         db.add(new_measurement)
#         db.commit()
#         db.refresh(new_measurement)
#         print(f"""
# POST Request on /db-insert
# Inserted:
# {measurement}
# """)
#         return {"id": new_measurement.id}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()


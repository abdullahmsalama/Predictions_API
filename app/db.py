""" This file is used for defining the database connection"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///./database.sqlite", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

""" This function create the predictions table (if not already exists),
no primary_key was specified as we want to actually allow repition of
requests done for the same id 
"""
def create_prediction_table():
    session = SessionLocal()
    try:
        session.execute("""CREATE TABLE IF NOT EXISTS model_prediction (
                                        id integer,
                                        prediction float); """)
    except Exception as e:
        print(e)

    finally:
        session.close()

""" This function inserts into the prediction table based on the
model prediction and the id from the POST request"""
def prediction_table_insert(id, prediction):
    try:
        engine.execute("""INSERT INTO "model_prediction"
               (id, prediction) VALUES (?,?)""",[id, prediction])
               #.format(id, prediction))        
    except Exception as e:
        print(e)
    
""" This function retreive the number of times a specific passenger_id
occured in the table """
def select_id_repetition(id):
    try:
        query = engine.execute("""SELECT count(id) as id_count from
         model_prediction where id = ?""", id)
        for query_result in query:    
            id_count = query_result['id_count']
        return id_count
    except Exception as e:
        print(e)
        return 0

""" This function counts the enteries in the predictions table and 
that was stored before, this function is only created to be used in testing """
def count_enteries_table():
    try:
        query_pred = engine.execute("""SELECT count(*) as pred_count from model_prediction""")
        for query_result in query_pred:    
            predictions_count = query_result['pred_count']
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
         detail="""Item not found, The model_prediction table was not created yet""")
    return predictions_count

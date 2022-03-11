import random
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from models import Promo, Participant, Prize
from schema import (
    PromoSchemaRequest,
    PromoSchemaFull,
    PromoSchemaModify,
    ParticipantSchemaRequest,
    PrizeSchemaRequest,
    PromoSchema,
)

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/promo", status_code=201)
def promo_post(item: PromoSchemaRequest) -> int:
    db_item = Promo(description=item.description, name=item.name)
    db.session.add(db_item)
    db.session.commit()
    return db_item.id


@app.get("/promo", response_model=List[PromoSchema])
def promo_get():
    return db.session.query(Promo).all()


@app.get("/promo/{promo_id}", response_model=PromoSchemaFull)
def promo_get_id(promo_id: int):
    db_item = db.session.query(Promo).get(promo_id)
    if db_item:
        return db_item
    raise HTTPException(status_code=404, detail="Promo not found")


@app.put("/promo/{promo_id}")
def promo_put_id(promo_id: int, data: PromoSchemaModify):
    db_item = db.session.query(Promo).get(promo_id)
    if db_item:
        mod_field = data.dict()
        res = {}
        if mod_field.get("name"):
            res["name"] = mod_field.get("name")
            db_item.name = mod_field.get("name")

        if "description" in mod_field:
            res["description"] = mod_field.get("description")
            db_item.description = mod_field.get("description")

        db.session.commit()
        return res
    raise HTTPException(status_code=404, detail="Promo not found")


@app.delete("/promo/{promo_id}", status_code=204)
def promo_delete_id(promo_id: int):
    db_item = db.session.query(Promo).get(promo_id)
    if db_item:
        db.session.delete(db_item)
        db.session.commit()
        return
    raise HTTPException(status_code=404, detail="Promo not found")


@app.post("/promo/{promo_id}/participant", status_code=201)
def promo_post_participant(promo_id: int, item: ParticipantSchemaRequest) -> int:
    db_promo = db.session.query(Promo).get(promo_id)
    if not db_promo:
        raise HTTPException(status_code=404, detail="Promo not found")

    db_item = Participant(name=item.name, promo_id=promo_id)
    db.session.add(db_item)
    db.session.commit()
    return db_item.id


@app.delete("/promo/{promo_id}/participant/{participant_id}", status_code=204)
def promo_delete_participant(promo_id: int, participant_id: int):
    db_promo = db.session.query(Promo).get(promo_id)
    db_part = db.session.query(Participant).get(participant_id)
    if not db_promo or not db_part:
        raise HTTPException(status_code=404, detail="Promo or participant not found")

    db.session.delete(db_part)
    db.session.commit()


@app.post("/promo/{promo_id}/prize", status_code=201)
def promo_post_prize(promo_id: int, item: PrizeSchemaRequest) -> int:
    db_promo = db.session.query(Promo).get(promo_id)
    if not db_promo:
        raise HTTPException(status_code=404, detail="Promo not found")

    db_item = Prize(description=item.description, promo_id=promo_id)
    db.session.add(db_item)
    db.session.commit()
    return db_item.id


@app.delete("/promo/{promo_id}/prize/{prize_id}", status_code=204)
def promo_delete_prize(promo_id: int, prize_id: int):
    db_promo = db.session.query(Promo).get(promo_id)
    db_part = db.session.query(Prize).get(prize_id)
    if not db_promo or not db_part:
        raise HTTPException(status_code=404, detail="Promo or prize not found")

    db.session.delete(db_part)
    db.session.commit()


@app.get("/promo/{promo_id}/raffle")
def promo_raffle(promo_id: int):
    people = list(db.session.query(Participant).filter_by(promo_id=promo_id))
    person_ids = [p.id for p in people]
    prizes = list(db.session.query(Prize).filter_by(promo_id=promo_id))
    prize_ids = [p.id for p in prizes]

    if len(prizes) != len(people):
        raise HTTPException(
            status_code=409, detail="Number of prizes and participants not equally"
        )

    result = []
    i = 0
    while i < len(people):
        person = {"id": people[i].id, "name": people[i].name}
        prize_id = prize_ids[random.randint(0, len(prize_ids) - 1)]
        prize = {
            "id": prize_id,
            "description": db.session.query(Prize).get(prize_id).description,
        }
        prize_ids.remove(prize_id)
        result.append({"winner": person, "prize": prize})
        i += 1

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

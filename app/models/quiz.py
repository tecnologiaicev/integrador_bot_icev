from extensions import db 
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy import func
from dataclasses import dataclass, asdict
import json 

@dataclass
class Quiz(db.Model):
    __tablename__ = "icev_quiz"
    id: Mapped[int] = mapped_column(sa.Identity(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.Text())
    timeclose: Mapped[int] = mapped_column(sa.Integer())

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)
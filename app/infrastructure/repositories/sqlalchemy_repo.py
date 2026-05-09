from sqlalchemy.orm import Session
from app.domain.entities import Link
from app.domain.repositories import LinkRepositoryInterface
from app.infrastructure.models import LinkModel


class SqlAlchemyLinkRepository(LinkRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, link: Link) -> Link:
        db_link = self.db.query(LinkModel).filter(LinkModel.slug == link.slug).first()
        if not db_link:
            db_link = LinkModel(**link.__dict__)
            self.db.add(db_link)
        else:
            for key, value in link.__dict__.items():
                if hasattr(db_link, key):
                    setattr(db_link, key, value)
        self.db.commit()
        self.db.refresh(db_link)
        return Link(
            **{k: v for k, v in db_link.__dict__.items() if k != "_sa_instance_state"}
        )

    def get_by_slug(self, slug: str) -> Link | None:
        db_link = self.db.query(LinkModel).filter(LinkModel.slug == slug).first()
        if not db_link:
            return None
        return Link(
            **{k: v for k, v in db_link.__dict__.items() if k != "_sa_instance_state"}
        )

    def delete(self, slug: str) -> None:
        self.db.query(LinkModel).filter(LinkModel.slug == slug).delete()
        self.db.commit()

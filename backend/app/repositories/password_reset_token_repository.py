from sqlalchemy.orm import Session

from app.models.password_reset_token import PasswordResetToken


class PasswordResetTokenRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, token: PasswordResetToken):
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def get_by_token(self, token: str):
        return (
            self.db.query(PasswordResetToken)
            .filter(PasswordResetToken.token == token)
            .first()
        )

    def update(self):
        self.db.commit()
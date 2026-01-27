from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Super Puper Tour Agency"
    debug: bool = False

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_exp_minutes: int = 60

    api_version: str = "v1"
    database_url: str = "sqlite:///./app.db"
    booking_auto_cancel_hours: int = 24

    class Config:
        env_file = ".env"


settings = Settings()

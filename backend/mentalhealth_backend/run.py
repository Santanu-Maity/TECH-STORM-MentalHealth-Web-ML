import os
from app import create_app
from config import DevelopmentConfig, ProductionConfig

env = os.getenv("FLASK_ENV", "development")
config = ProductionConfig if env == "production" else DevelopmentConfig

app = create_app(config)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=config.DEBUG,
    )

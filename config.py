import os

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "pv-monitoring-secret-key"
    )

   # MENGGUNAKAN JALUR IPv4 POOLER DARI SUPABASE
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres.dseekoorntdtrveppvqp:Teknikelektro@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MQTT_TOPIC = os.environ.get(
        "MQTT_TOPIC",
        "pv/data"
    )

    MQTT_WS_HOST = os.environ.get(
        "MQTT_WS_HOST",
        "b792c9ff.ala.asia-southeast1.emqxsl.com"
    )

    MQTT_WS_PORT = int(
        os.environ.get(
            "MQTT_WS_PORT",
            8084
        )
    )

    MQTT_WS_PATH = os.environ.get(
        "MQTT_WS_PATH",
        "/mqtt"
    )

    MQTT_USERNAME = os.environ.get(
        "MQTT_USERNAME",
        "Rsi123"
    )

    MQTT_PASSWORD = os.environ.get(
        "MQTT_PASSWORD",
        "Rsi123"
    )

    MQTT_USE_SSL = os.environ.get(
        "MQTT_USE_SSL",
        "true"
    ).lower() in ["true", "1", "yes"]
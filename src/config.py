from pathlib import Path

from common.settings import AppSettings
from common.settings import KafkaConfig as BaseKafkaConfig
from common.settings import PostgresConfig, SentryConfig, ServiceBaseSettings

BASE_DIR = Path(__file__).parent.parent.parent


class KafkaConfig(BaseKafkaConfig):
    faust_app_type: str = "worker"


class Settings(ServiceBaseSettings):
    app: AppSettings = AppSettings()
    base_dir: Path = BASE_DIR
    database: PostgresConfig = PostgresConfig()
    sentry: SentryConfig = SentryConfig()
    kafka: KafkaConfig = KafkaConfig()

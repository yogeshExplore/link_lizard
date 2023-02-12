from app.config import Config
from app.setting import Setting
from app_logging import logger
from app.services import Service

injected_services = Service()

logger.info(f"[START]: {Config.APP_NAME} running in {Config.ENVIRONMENT} mode in {Setting.PROJECT_BASE_DIR}")

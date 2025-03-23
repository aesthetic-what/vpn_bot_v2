import logging


class Logger(logging.Logger):
    instance: "Logger|None" = None
    @staticmethod
    def getinstance() -> "Logger":
        if Logger.instance is None:
            Logger.instance = logging.getLogger("vpn_bot_v2")
            logging.basicConfig(filename='api.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')
        return Logger.instance
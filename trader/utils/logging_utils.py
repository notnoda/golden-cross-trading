import datetime
import logging

################################################################################
# Log 정보를 설정 한다.
################################################################################
def console_logger(log_path: str):
    current_time = datetime.datetime.now().strftime("-%Y%m%d%H%M%S")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        filename=f"{log_path}{current_time}.log",  # 로그를 파일로 저장
        filemode="w"
    )

    '''
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
    stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정

    logger = logging.getLogger(name="kisLogger")
    logger.addHandler(stream_handler)
    '''

################################################################################
# Log 정보를 설정 한다.
################################################################################
def file_logger(log_path: str):
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        filename=f"{log_path}-{current_time}.log",  # 로그를 파일로 저장
        filemode="w"
    )

    '''
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
    stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정

    logger = logging.getLogger(name="kisLogger")
    logger.addHandler(stream_handler)
    '''

################################################################################
# Log 정보를 설정 한다.
################################################################################
def get_logger(log_path: str):
    current_time = datetime.datetime.now().strftime("-%Y%m%d%H%M%S")

    logger = logging.getLogger("SOXL")
    file_handler = logging.FileHandler(f"{log_path}{current_time}.log")
    logger.addHandler(file_handler)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
    file_handler.setFormatter(formatter)

    logging.info("test")

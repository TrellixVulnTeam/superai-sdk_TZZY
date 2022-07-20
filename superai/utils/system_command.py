import logging
import shlex
import subprocess

logger = logging.getLogger(__name__)


def system(command: str) -> int:
    """
    An alternative of `os.system`, with error catching and failure on bash commands
    Args:
        command: String command
    Returns:
        Return code of the command
    """
    logger.info(f"Running '{command}'")
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with process.stdout:
        try:
            for line in iter(process.stdout.readline, b""):
                logger.info(line.decode("utf-8").strip())
        except subprocess.CalledProcessError as e:
            logger.error(f"{str(e)}")
            raise
    process.wait()
    if process.returncode != 0:
        logger.error(f"Command '{command}' failed with return code {process.returncode}")
        raise subprocess.CalledProcessError(process.returncode, command, output=process.stdout, stderr=process.stderr)
    return process.returncode

"""This module configures the logger.

Creates a logger instance that can be imported
in project files.
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='job_radar.log'
)

logger = logging.getLogger('job_radar')

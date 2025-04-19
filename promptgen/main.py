#!/usr/bin/env python3
"""
Main entry point for the Prompt Generator application.
"""

import logging
import os
from dotenv import load_dotenv

from promptgen.web.app import create_app

# Load environment variables
load_dotenv()

# Configure logging
logging_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Run the application."""
    logger.info("Starting Prompt Generator application")
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") == "development")


if __name__ == "__main__":
    main() 
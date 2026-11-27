import logging

def test_logging_level(level_name, level_value):
    """Test logging at different levels"""
    print(f"\n--- Testing with {level_name} level ---")
    
    # Configure logging with specific level
    logging.basicConfig(
        level=level_value,
        format='%(levelname)s: %(message)s',
        force=True  # This forces reconfiguration
    )
    
    logger = logging.getLogger(f"test_{level_name.lower()}")
    
    # Test all levels
    logger.debug("DEBUG: Detailed diagnostic information")
    logger.info("INFO: General information")
    logger.warning("WARNING: Something unexpected happened")
    logger.error("ERROR: A serious problem occurred")
    logger.critical("CRITICAL: Very serious error")

# Test different logging levels
test_logging_level("DEBUG", logging.DEBUG)
test_logging_level("INFO", logging.INFO)
test_logging_level("WARNING", logging.WARNING)
test_logging_level("ERROR", logging.ERROR)
test_logging_level("CRITICAL", logging.CRITICAL)

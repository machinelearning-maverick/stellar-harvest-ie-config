def test_pytest_plugin_logs_configured(pytester):
    # Create a dummy test file that emits a log
    pytester.makepyfile("""
        import logging
        logger = logging.getLogger(__name__)

        def test_dummy(caplog):
            caplog.set_level(logging.INFO)
            logger.info("plugin is active")
            assert "plugin is active" in caplog.text
    """)

    result = pytester.runpytest("--maxfail=1", "--disable-warnings", "-q")
    # test should pass and the logged message should appear in caplog.text
    result.assert_outcomes(passed=1)

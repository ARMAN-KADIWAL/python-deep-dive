from devops_ai.config import Settings


def test_settings_have_safe_local_defaults(monkeypatch):
    monkeypatch.delenv("DEVOPS_AI_BEDROCK_ENABLED", raising=False)
    monkeypatch.delenv("BEDROCK_MODEL_ID", raising=False)
    settings = Settings.from_env()
    assert settings.bedrock_enabled is False
    assert settings.bedrock_model_id == ""
    assert settings.max_upload_bytes > 0


def test_invalid_limits_fall_back_to_defaults(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_BYTES", "not-a-number")
    monkeypatch.setenv("ERROR_SPIKE_THRESHOLD", "0")
    settings = Settings.from_env()
    assert settings.max_upload_bytes == 5 * 1024 * 1024
    assert settings.error_spike_threshold == 5


def test_boolean_configuration_is_explicit(monkeypatch):
    monkeypatch.setenv("DEVOPS_AI_BEDROCK_ENABLED", "yes")
    assert Settings.from_env().bedrock_enabled is True

import pytest
from pydantic import ValidationError

from backend.models import AddonOptions, AdditionalHost, OptionsRead


def make(**kw):
    base = {"external_hostname": "ha.example.com", "additional_hosts": []}
    base.update(kw)
    return AddonOptions(**base)


class TestHostnameValidation:
    def test_valid_hostname(self):
        assert make().external_hostname == "ha.example.com"

    @pytest.mark.parametrize(
        "bad",
        ["https://ha.example.com", "ha.example.com:8123", "HA.EXAMPLE.COM", "-bad.tld"],
    )
    def test_invalid_hostname(self, bad):
        with pytest.raises(ValidationError):
            make(external_hostname=bad)

    def test_empty_hostname_allowed_with_other_config(self):
        opts = AddonOptions(
            external_hostname="",
            additional_hosts=[{"hostname": "a.example.com", "service": "http://x"}],
        )
        assert opts.external_hostname == ""

    def test_additional_host_hostname_validated(self):
        with pytest.raises(ValidationError):
            AdditionalHost(hostname="http://bad", service="http://x")

    def test_additional_host_service_required(self):
        with pytest.raises(ValidationError):
            AdditionalHost(hostname="a.example.com", service="  ")


class TestRunParameters:
    def test_allowed(self):
        opts = make(run_parameters=["--loglevel=debug", "--region=us"])
        assert opts.run_parameters == ["--loglevel=debug", "--region=us"]

    @pytest.mark.parametrize(
        "bad", ["--evil=1", "--token=x", "loglevel=debug", "--loglevel debug"]
    )
    def test_rejected(self, bad):
        with pytest.raises(ValidationError):
            make(run_parameters=[bad])


class TestCrossChecks:
    def test_npm_and_catch_all_mutually_exclusive(self):
        with pytest.raises(ValidationError, match="mutually exclusive"):
            make(catch_all_service="http://x", nginx_proxy_manager=True)

    def test_empty_config_rejected(self):
        with pytest.raises(ValidationError, match="Cannot run without"):
            AddonOptions(external_hostname="", additional_hosts=[])

    def test_token_only_config_allowed(self):
        opts = AddonOptions(
            external_hostname="", additional_hosts=[], tunnel_token="abc"
        )
        assert opts.tunnel_token == "abc"


class TestToSupervisorOptions:
    def test_unset_optionals_omitted(self):
        result = make().to_supervisor_options()
        assert result == {
            "external_hostname": "ha.example.com",
            "additional_hosts": [],
        }

    def test_set_values_included(self):
        result = make(
            tunnel_name="mytunnel",
            post_quantum=True,
            log_level="debug",
            run_parameters=["--loglevel=debug"],
        ).to_supervisor_options()
        assert result["tunnel_name"] == "mytunnel"
        assert result["post_quantum"] is True
        assert result["log_level"] == "debug"
        assert result["run_parameters"] == ["--loglevel=debug"]

    def test_disable_chunked_encoding_omitted_when_none(self):
        opts = AddonOptions(
            external_hostname="",
            additional_hosts=[{"hostname": "a.example.com", "service": "http://x"}],
        )
        host = opts.to_supervisor_options()["additional_hosts"][0]
        assert "disableChunkedEncoding" not in host


class TestOptionsRead:
    def test_token_masked(self):
        read = OptionsRead.from_supervisor(
            {"external_hostname": "", "additional_hosts": [], "tunnel_token": "s3cret"}
        )
        assert read.tunnel_token_set is True
        assert "s3cret" not in read.tunnel_token_masked

    def test_no_token(self):
        read = OptionsRead.from_supervisor(
            {"external_hostname": "", "additional_hosts": []}
        )
        assert read.tunnel_token_set is False
        assert read.tunnel_token_masked == ""

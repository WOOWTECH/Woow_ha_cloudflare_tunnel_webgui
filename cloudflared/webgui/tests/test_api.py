class TestHealth:
    def test_health(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200
        body = res.json()
        assert body["supervisor_connected"] is True
        assert body["addon_version"] == "1.0.0"
        assert body["tunnel"]["status"] in ("running", "starting", "stopped")


class TestOptionsApi:
    def test_get_options_masks_token(self, client, fake_supervisor):
        fake_supervisor.options["tunnel_token"] = "s3cret"
        res = client.get("/api/options")
        assert res.status_code == 200
        body = res.json()
        assert body["tunnel_token_set"] is True
        assert "s3cret" not in str(body)

    def test_put_options_saves_via_supervisor(self, client, fake_supervisor):
        res = client.put(
            "/api/options",
            json={"external_hostname": "ha.example.com", "additional_hosts": []},
        )
        assert res.status_code == 200
        assert fake_supervisor.validated is not None
        assert fake_supervisor.options["external_hostname"] == "ha.example.com"
        assert fake_supervisor.restarted is False

    def test_put_options_with_restart(self, client, fake_supervisor):
        res = client.put(
            "/api/options?restart=true",
            json={"external_hostname": "ha.example.com", "additional_hosts": []},
        )
        assert res.status_code == 200
        assert res.json()["restarting"] is True
        assert fake_supervisor.restarted is True

    def test_put_keeps_existing_token_when_omitted(self, client, fake_supervisor):
        fake_supervisor.options["tunnel_token"] = "keepme"
        client.put(
            "/api/options",
            json={"external_hostname": "ha.example.com", "additional_hosts": []},
        )
        assert fake_supervisor.options["tunnel_token"] == "keepme"

    def test_put_empty_string_removes_token(self, client, fake_supervisor):
        fake_supervisor.options["tunnel_token"] = "removeme"
        client.put(
            "/api/options",
            json={
                "external_hostname": "ha.example.com",
                "additional_hosts": [],
                "tunnel_token": "",
            },
        )
        assert "tunnel_token" not in fake_supervisor.options

    def test_put_invalid_options_rejected(self, client, fake_supervisor):
        res = client.put(
            "/api/options",
            json={
                "external_hostname": "ha.example.com",
                "additional_hosts": [],
                "catch_all_service": "http://x",
                "nginx_proxy_manager": True,
            },
        )
        assert res.status_code == 422
        assert fake_supervisor.validated is None

    def test_restart_endpoint(self, client, fake_supervisor):
        res = client.post("/api/restart")
        assert res.status_code == 200
        assert fake_supervisor.restarted is True


class TestWizard:
    def test_state_local_mode(self, client):
        res = client.get("/api/wizard/state")
        assert res.status_code == 200
        body = res.json()
        assert body["mode"] == "local"

    def test_state_token_mode(self, client, fake_supervisor):
        fake_supervisor.options["tunnel_token"] = "tok"
        res = client.get("/api/wizard/state")
        assert res.json()["mode"] == "token"


class TestLogs:
    def test_snapshot(self, client):
        res = client.get("/api/logs")
        assert res.status_code == 200
        assert "lines" in res.json()

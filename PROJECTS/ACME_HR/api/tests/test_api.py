def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def bootstrap_admin(client) -> str:
    from sqlalchemy import select

    from app.db import get_session_factory
    from app.models import Account, Employee, Role
    from app.security import hash_password

    session = get_session_factory()()
    try:
        existing = session.scalar(select(Employee).where(Employee.work_email == "asha@acme.test"))
        if existing is None:
            employee = Employee(
                employee_code="ADMIN-1",
                name="Asha Admin",
                work_email="asha@acme.test",
                activated=True,
                archived=False,
            )
            session.add(employee)
            session.flush()
            session.add(
                Account(
                    employee_id=employee.id,
                    role=Role.SYSTEM_ADMINISTRATOR,
                    password_hash=hash_password("asha-password"),
                )
            )
            session.commit()
    finally:
        session.close()
    login = client.post("/auth/login", json={"work_email": "asha@acme.test", "password": "asha-password"})
    assert login.status_code == 200, login.text
    return login.json()["access_token"]


def test_archived_employee_cannot_sign_in(client):
    token = bootstrap_admin(client)
    created = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-1",
            "name": "Isha Employee",
            "work_email": "isha@acme.test",
            "password": "isha-password",
            "role": "Employee",
        },
    )
    assert created.status_code == 201, created.text
    employee_id = created.json()["id"]
    assert client.post(f"/employees/{employee_id}/archive", headers=auth(token)).status_code == 200
    refused = client.post("/auth/login", json={"work_email": "isha@acme.test", "password": "isha-password"})
    assert refused.status_code == 401


def test_employee_cannot_create_a_department(client):
    token = bootstrap_admin(client)
    employee = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-2",
            "name": "Nia Employee",
            "work_email": "nia@acme.test",
            "password": "nia-password",
            "role": "Employee",
        },
    ).json()
    login = client.post("/auth/login", json={"work_email": "nia@acme.test", "password": "nia-password"})
    unit = client.post("/business-units", headers=auth(token), json={"name": "Delivery"})
    assert unit.status_code == 201, unit.text
    refused = client.post(
        "/departments",
        headers=auth(login.json()["access_token"]),
        json={"name": "Engineering", "business_unit_id": unit.json()["id"]},
    )
    assert refused.status_code == 403
    assert employee["role"] == "Employee"


def test_self_update_cannot_change_name_and_directory_hides_phone(client):
    token = bootstrap_admin(client)
    created = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-3",
            "name": "Meera Employee",
            "work_email": "meera@acme.test",
            "password": "meera-password",
            "role": "Employee",
            "phone": "99999",
        },
    )
    assert created.status_code == 201, created.text
    employee_token = client.post(
        "/auth/login", json={"work_email": "meera@acme.test", "password": "meera-password"}
    ).json()["access_token"]
    renamed = client.patch("/employees/me", headers=auth(employee_token), json={"name": "Someone Else"})
    assert renamed.status_code == 422
    updated = client.patch("/employees/me", headers=auth(employee_token), json={"phone": "88888"})
    assert updated.status_code == 200
    assert updated.json()["phone"] == "88888"
    cards = client.get("/directory", headers=auth(employee_token)).json()
    meera = next(card for card in cards if card["work_email"] == "meera@acme.test")
    assert "phone" not in meera
    assert meera["name"] == "Meera Employee"


def test_manager_cannot_download_another_employees_document(client):
    token = bootstrap_admin(client)
    manager = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "M-1",
            "name": "Ravi Manager",
            "work_email": "ravi@acme.test",
            "password": "ravi-password",
            "role": "Manager",
        },
    ).json()
    employee = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-4",
            "name": "Lata Employee",
            "work_email": "lata@acme.test",
            "password": "lata-password",
            "role": "Employee",
            "reporting_manager_id": manager["id"],
        },
    ).json()
    employee_token = client.post(
        "/auth/login", json={"work_email": "lata@acme.test", "password": "lata-password"}
    ).json()["access_token"]
    uploaded = client.post(
        f"/employees/{employee['id']}/documents",
        headers=auth(employee_token),
        data={"document_type": "ID Proof"},
        files={"file": ("proof.txt", b"identity", "text/plain")},
    )
    assert uploaded.status_code == 201, uploaded.text
    manager_token = client.post(
        "/auth/login", json={"work_email": "ravi@acme.test", "password": "ravi-password"}
    ).json()["access_token"]
    refused = client.get(f"/documents/{uploaded.json()['id']}", headers=auth(manager_token))
    assert refused.status_code == 403
    allowed = client.get(f"/documents/{uploaded.json()['id']}", headers=auth(employee_token))
    assert allowed.status_code == 200
    assert allowed.content == b"identity"


def test_leave_rules_and_manager_approval(client):
    token = bootstrap_admin(client)
    manager = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "M-2",
            "name": "Kiran Manager",
            "work_email": "kiran@acme.test",
            "password": "kiran-password",
            "role": "Manager",
        },
    ).json()
    employee = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-5",
            "name": "Dev Employee",
            "work_email": "dev@acme.test",
            "password": "dev-password",
            "role": "Employee",
            "reporting_manager_id": manager["id"],
        },
    ).json()
    assert client.post(f"/employees/{employee['id']}/activate", headers=auth(token)).status_code == 200
    policy = client.put(
        "/leave-policies",
        headers=auth(token),
        json={
            "leave_type": "Casual Leave",
            "days_granted_per_year": "2.0",
            "carry_forward_maximum": "1.0",
            "expiry_months": 3,
            "grant_month": 1,
            "grant_day": 1,
        },
    )
    assert policy.status_code == 200, policy.text
    employee_token = client.post(
        "/auth/login", json={"work_email": "dev@acme.test", "password": "dev-password"}
    ).json()["access_token"]
    half = client.post(
        "/leave-requests",
        headers=auth(employee_token),
        json={
            "leave_type": "Casual Leave",
            "from_date": "2026-05-01",
            "to_date": "2026-05-03",
            "day_portion": "Half",
        },
    )
    assert half.status_code == 422
    too_long = client.post(
        "/leave-requests",
        headers=auth(employee_token),
        json={
            "leave_type": "Casual Leave",
            "from_date": "2026-05-01",
            "to_date": "2026-05-05",
            "day_portion": "Full",
        },
    )
    assert too_long.status_code == 422
    created = client.post(
        "/leave-requests",
        headers=auth(employee_token),
        json={
            "leave_type": "Casual Leave",
            "from_date": "2026-05-01",
            "to_date": "2026-05-02",
            "day_portion": "Full",
        },
    )
    assert created.status_code == 201, created.text
    manager_token = client.post(
        "/auth/login", json={"work_email": "kiran@acme.test", "password": "kiran-password"}
    ).json()["access_token"]
    decided = client.post(
        f"/leave-requests/{created.json()['id']}/decision",
        headers=auth(manager_token),
        json={"status": "Approved"},
    )
    assert decided.status_code == 200, decided.text
    notices = client.get("/notifications", headers=auth(employee_token))
    assert notices.status_code == 200
    assert any("approved" in item["body"] for item in notices.json())


def test_check_in_requires_activation_and_location(client):
    token = bootstrap_admin(client)
    location = client.post(
        "/locations",
        headers=auth(token),
        json={"name": "Hyderabad", "region": "South", "timezone": "Asia/Kolkata"},
    )
    assert location.status_code == 201, location.text
    employee = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-6",
            "name": "Om Employee",
            "work_email": "om@acme.test",
            "password": "om-password",
            "role": "Employee",
        },
    ).json()
    employee_token = client.post(
        "/auth/login", json={"work_email": "om@acme.test", "password": "om-password"}
    ).json()["access_token"]
    inactive = client.post("/attendance/check-in", headers=auth(employee_token))
    assert inactive.status_code == 403
    client.post(f"/employees/{employee['id']}/activate", headers=auth(token))
    missing_location = client.post("/attendance/check-in", headers=auth(employee_token))
    assert missing_location.status_code == 422
    client.patch(
        f"/employees/{employee['id']}",
        headers=auth(token),
        json={"location_id": location.json()["id"]},
    )
    checked_in = client.post("/attendance/check-in", headers=auth(employee_token))
    assert checked_in.status_code == 201, checked_in.text
    assert checked_in.json()["status"] == "No shift"


def test_integration_is_stored_as_not_connected(client):
    token = bootstrap_admin(client)
    created = client.post(
        "/integrations",
        headers=auth(token),
        json={"system_name": "ADP", "endpoint": "https://example.test/adp"},
    )
    assert created.status_code == 201, created.text
    assert created.json()["is_connected"] is False


def test_organization_chart_follows_reporting_manager(client):
    token = bootstrap_admin(client)
    manager = client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "M-3",
            "name": "Sara Manager",
            "work_email": "sara@acme.test",
            "password": "sara-password",
            "role": "Manager",
        },
    ).json()
    client.post(
        "/employees",
        headers=auth(token),
        json={
            "employee_code": "E-7",
            "name": "Neil Employee",
            "work_email": "neil@acme.test",
            "password": "neil-password",
            "role": "Employee",
            "reporting_manager_id": manager["id"],
        },
    )
    chart = client.get("/organization-chart", headers=auth(token))
    assert chart.status_code == 200, chart.text
    sara = next(node for node in chart.json() if node["work_email"] == "sara@acme.test")
    assert [report["work_email"] for report in sara["reports"]] == ["neil@acme.test"]

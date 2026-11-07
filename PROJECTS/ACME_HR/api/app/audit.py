from sqlalchemy.orm import Session

from app.models import AuditEvent


def record_audit(
    session: Session,
    *,
    actor_employee_id: int | None,
    action: str,
    entity_name: str,
    entity_id: str | None,
    detail: dict | None = None,
) -> None:
    session.add(
        AuditEvent(
            actor_employee_id=actor_employee_id,
            action=action,
            entity_name=entity_name,
            entity_id=entity_id,
            detail=detail,
        )
    )

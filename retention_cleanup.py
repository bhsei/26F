"""CampusShare database retention maintenance.

Preview by default. Explicit --apply is required to make changes. Run only on a
verified database backup, from a trusted administrative machine. This tool
handles database rows, not application log files, backups or uploaded photos.
"""

import argparse
from datetime import datetime, timezone
import sqlite3
from pathlib import Path


# Provisional SRS 4.0 retention periods; review with the project team.
POLICY = {
    "rental_records_months": 24,
    "messages_days": 365,
    "notifications_days": 365,
    "attempts_hours": 24,
    "reminders_days_after_end": 30,
}


def cleanup_database(database_path, *, apply=False, now=None):
    """Return per-category affected counts. Roll back unless apply=True."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    timestamp = now.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    path = Path(database_path)
    if not path.is_file():
        raise FileNotFoundError(f"Database not found: {path}")

    connection = sqlite3.connect(str(path), timeout=30)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")
        affected = {}

        def change(label, sql, parameters):
            cursor = connection.execute(sql, parameters)
            affected[label] = cursor.rowcount

        change("login_attempts", """
            DELETE FROM login_attempts
            WHERE datetime(attempted_at) < datetime(?, '-24 hours')
        """, (timestamp,))
        change("verification_email_attempts", """
            DELETE FROM verification_email_attempts
            WHERE datetime(attempted_at) < datetime(?, '-24 hours')
        """, (timestamp,))
        change("messages", """
            DELETE FROM messages
            WHERE datetime(created_at) < datetime(?, '-365 days')
        """, (timestamp,))
        change("notifications", """
            DELETE FROM notifications
            WHERE datetime(created_at) < datetime(?, '-365 days')
        """, (timestamp,))
        change("rental_reminders", """
            DELETE FROM rental_reminders
            WHERE borrowing_request_id IN (
                SELECT br.id FROM borrowing_requests br
                WHERE br.status IN ('Completed', 'Rejected', 'Cancelled')
                  AND date(br.end_date) < date(?, '-30 days')
                  AND br.damage_dispute_status != 'Pending'
                  AND br.deposit_status != 'Held'
                  AND NOT (COALESCE(br.late_fee, 0) > 0
                           AND br.late_fee_status = 'Unpaid')
            )
        """, (timestamp,))
        # Redact sensitive free-text data, retaining primary keys, financial
        # totals and audit linkage. Never redact an unresolved rental.
        change("old_rental_details_redacted", """
            UPDATE borrowing_requests
            SET damage_report = '', damage_dispute_reason = '',
                damage_dispute_resolution = '',
                inspection_rejection_reason = '', meetup_location = NULL
            WHERE status IN ('Completed', 'Rejected', 'Cancelled')
              AND date(end_date) < date(?, '-24 months')
              AND damage_dispute_status != 'Pending'
              AND deposit_status != 'Held'
              AND NOT (COALESCE(late_fee, 0) > 0
                       AND late_fee_status = 'Unpaid')
              AND (
                  COALESCE(damage_report, '') != ''
                  OR COALESCE(damage_dispute_reason, '') != ''
                  OR COALESCE(damage_dispute_resolution, '') != ''
                  OR COALESCE(inspection_rejection_reason, '') != ''
                  OR meetup_location IS NOT NULL
              )
        """, (timestamp,))

        if apply:
            connection.commit()
        else:
            connection.rollback()
        return affected
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, help="Existing CampusShare SQLite file")
    parser.add_argument("--apply", action="store_true", help="Commit changes; default is preview")
    args = parser.parse_args()
    affected = cleanup_database(args.database, apply=args.apply)
    print("APPLIED" if args.apply else "PREVIEW ONLY - NO CHANGES SAVED")
    for category, count in affected.items():
        print(f"{category}: {count}")
    if not args.apply:
        print("Run with --apply only after checking a verified database backup.")


if __name__ == "__main__":
    main()

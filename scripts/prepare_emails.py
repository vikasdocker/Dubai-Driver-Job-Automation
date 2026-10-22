#!/usr/bin/env python3
"""Prepare personalised draft emails; send only when explicitly confirmed."""
from __future__ import annotations
import csv
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTACTS = ROOT / "data" / "companies.csv"
OUT = ROOT / "outbox"
SENDER = os.getenv("SMTP_USERNAME", "").strip()
PASSWORD = os.getenv("SMTP_APP_PASSWORD", "").strip()
MODE = os.getenv("MODE", "preview").strip().lower()
CONFIRM_SEND = os.getenv("CONFIRM_SEND", "").strip()

SUBJECT = "Enquiry: Dubai Driver Opportunities and Work Visa Sponsorship"

def build_message(company: str, recipient: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = SENDER or "candidate@example.com (preview only)"
    msg["To"] = recipient
    msg["Subject"] = SUBJECT
    msg.set_content(f"""Dear Recruitment Team,

I am based in India and would like to enquire about current driver opportunities in Dubai, particularly taxi, ride-hailing, airport transfer, or company-driver roles.

Could you please confirm:
- Whether you are currently recruiting candidates from India;
- Whether the employer arranges a UAE employment visa and required onboarding;
- The driving licence / RTA permit requirements and whether training is provided;
- The salary or commission structure, working hours, accommodation (if any), and any candidate-paid fees.

I would be grateful for the official application link and the next steps. I will provide my CV and documents through your official recruitment channel if eligible.

Thank you for your time.

Kind regards,
Vikas Shelar
India
""")
    return msg

def main() -> int:
    if not CONTACTS.exists():
        print(f"ERROR: contacts file missing: {CONTACTS}", file=sys.stderr)
        return 2
    OUT.mkdir(exist_ok=True)
    with CONTACTS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        print("ERROR: no contacts listed", file=sys.stderr)
        return 2

    if MODE not in {"preview", "send"}:
        print("ERROR: MODE must be preview or send", file=sys.stderr)
        return 2
    sending = MODE == "send"
    if sending:
        if CONFIRM_SEND != "YES":
            print("ERROR: send blocked; set CONFIRM_SEND=YES explicitly.", file=sys.stderr)
            return 3
        if not SENDER or not PASSWORD:
            print("ERROR: SMTP_USERNAME and SMTP_APP_PASSWORD are required to send.", file=sys.stderr)
            return 3

    for row in rows:
        company = (row.get("company") or "").strip()
        recipient = (row.get("email") or "").strip()
        if not company or not recipient or "@" not in recipient:
            print(f"SKIP invalid contact row: {row}")
            continue
        msg = build_message(company, recipient)
        safe_name = "".join(ch.lower() if ch.isalnum() else "-" for ch in company).strip("-")
        draft_path = OUT / f"{safe_name}.eml"
        draft_path.write_bytes(msg.as_bytes())
        print(f"{'READY TO SEND' if sending else 'PREVIEW'}: {company} <{recipient}>")
        print(f"Draft: {draft_path.relative_to(ROOT)}")
        if sending:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
                server.login(SENDER, PASSWORD)
                server.send_message(msg)
            print(f"SENT: {company}")

    print(f"Finished in {MODE} mode.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

# Dubai Driver Job Outreach Automation

A cautious GitHub Actions workflow for preparing and optionally sending recruitment enquiry emails to Dubai driver/taxi employers.

## Important
- Contact details and recruitment/sponsorship policies can change. Verify each address and vacancy through the organisation's official website before sending.
- This tool prepares enquiries, not a job application for a confirmed vacancy.
- The workflow defaults to **preview**. Review generated drafts before selecting send.
- Sending requires your own Gmail App Password stored as GitHub Actions secrets. Never commit passwords or share them in chat.
- ChatGPT consumer subscription does not include OpenAI API usage. This starter uses editable email templates and does not call the ChatGPT/OpenAI API.

## Workflow setup
1. Open **Settings → Secrets and variables → Actions**.
2. Add `SMTP_USERNAME` (your Gmail address) and `SMTP_APP_PASSWORD` (a Google App Password; not your normal password).
3. Open **Actions → Dubai Driver Job Outreach → Run workflow**.
4. Run with `mode=preview` first and inspect the artifacts/log output.
5. Only after verifying the company contacts and draft, select `mode=send` and type `confirm_send=YES`.

The send option is deliberately gated and sends only to the recipients listed in `data/companies.csv`.

## Contact tracker
Edit `data/companies.csv` to add/update contacts. The included contact leads are unverified examples and should be checked before use.

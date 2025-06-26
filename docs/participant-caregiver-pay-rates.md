---
title: Participant Caregiver Pay Rates
---

# Participant Caregiver Pay Rates

_Path_: `../PAYRATE/pce/`

| Column | Type | Required |
|--------|------|----------|
| ParticipantId | string | ✅ |
| CaregiverEmployerId | string | ✅ |
| ServiceCode | string | ✅ |
| BillCode | string | ❌ |
| StartDate | date | ✅ |
| EndDate | date | ❌ |
| StartTime | time | ✅ |
| EndTime | time | ❌ |
| ValidDays | string | ❌ |
| EarnType | string | ❌ |
| IsOvertimeEligible | boolean | ❌ |
| Rate | number | ✅ |
| HolidayPremium | number | ❌ |
| IsActive | boolean | ❌ |
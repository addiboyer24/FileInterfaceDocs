---
title: Participant Caregiver Pay Rates
version: 1.0
---

# Participant Caregiver Pay Rates

**Path:** `PAYRATE/pce/`

`📁 PAYRATE/pce/`

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
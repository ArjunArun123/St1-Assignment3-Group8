# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures:
py -m pytest -q from project/ – 6 failed, 33 passed. 
Key failures: 
1. test_book_appointment_practitioner_conflict (Failed: DID NOT RAISE ValueError)
2. test_book_different_practitioner_same_time_allowed (ValueError raised incorrectly)
3. test_cancel_scheduled_appointment (AssertionError: assert None is Appointment)
## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: 
Booking the same practitioner at the exact same time succeeds (no error), but booking a *different* practitioner at the same time fails with a ValueError.
- Expected behaviour and requirement: 
Only another SCHEDULED booking for the same practitioner at exactly the same datetime should be rejected (FR-05, AC-04.1). A different practitioner at the same time is allowed (AC-04.2).
- Minimal synthetic reproduction steps: 
1. Register patient P1, practitioner DR1, and practitioner DR2.
2. Book appointment A1 for P1/DR1 at 10:00.
3. Attempt to book A2 for P1/DR1 at 10:00. (Expected: ValueError. Observed: Success).
4. Attempt to book A3 for P1/DR2 at 10:00. (Expected: Success. Observed: ValueError).
- Meaningful failing test path/name and exact relevant failure: 
1. `tests/test_services.py::TestAppointmentBooking::test_book_appointment_practitioner_conflict` - Failed: DID NOT RAISE ValueError.
2. `tests/test_services.py::TestAppointmentBooking::test_book_different_practitioner_same_time_allowed` - ValueError: Practitioner already has a SCHEDULED appointment at this time.
3. `tests/test_starter.py::test_conflict_rule_and_different_practitioner` - Failed: DID NOT RAISE ValueError.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: 
After cancelling a SCHEDULED appointment, looking it up via `store.find_appointment()` returns `None` (which causes the service to raise a LookupError), even though the appointment object still exists in memory with a CANCELLED status.
- Expected behaviour and requirement: 
Cancelled appointments must remain retrievable via lookup and listing during the session (FR-07, AC-05.2). Repeated cancellation should raise a ValueError, not a LookupError (AC-05.3).
- Minimal synthetic reproduction steps: 
1. Register patient P1 and practitioner DR1.
2. Book appointment A1.
3. Cancel appointment A1.
4. Call `store.find_appointment("A1")`. (Expected: Returns the appointment object. Observed: Returns None).
- Meaningful failing test path/name and exact relevant failure: 
1. `tests/test_services.py::TestAppointmentCancellation::test_cancel_scheduled_appointment` - AssertionError: assert None is <Appointment>.
2. `tests/test_services.py::TestAppointmentCancellation::test_cancel_already_cancelled_raises_value_error` - LookupError: Appointment not found.
3. `tests/test_services.py::TestCancellationGuards::test_cancel_retains_history` - assert None is <Appointment>.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible:
The logic in `SmartCareDataStore.has_practitioner_conflict()` is inverted. It is likely checking `!=` (not equal) instead of `==` (equal) when comparing practitioner IDs. This perfectly explains why the rule fails in both directions (same practitioner allowed, different practitioner rejected).

Evidence intended to inspect / competing explanation / discriminating check: 
Evidence: `has_practitioner_conflict()` in `smartcare/data_store.py`.
Competing explanation: The service is passing the wrong practitioner ID to the conflict check.
Discriminating check: Call `store.has_practitioner_conflict('DR1', time)` and `store.has_practitioner_conflict('DR2', time)` directly after booking A1. If they return False and True (flipped), the fault is in the store method.

Member and saved sequence/time or commit showing this preceded consultation: 
Arjun Arun Madambikattil. Hypothesis recorded before Copilot consultation.

### F8-02 human entry
Likely cause and why plausible: 
The `SmartCareDataStore.find_appointment()` method has an extra condition that filters out appointments if their status is `CANCELLED`, effectively "hiding" them from lookup even though they aren't deleted from the store. This explains why `list_appointments()` still sees it, but `find_appointment()` returns None.

Evidence intended to inspect / competing explanation / discriminating check:
Evidence: `SmartCareDataStore.find_appointment()` in `smartcare/data_store.py`.
Competing explanation: The cancellation process is accidentally deleting the appointment from the store's dictionary.
Discriminating check: After cancelling, check if `len(store.list_appointments())` decreases. If the count stays the same but `find_appointment` returns None, the lookup is hiding it, not deleting it.

Member and saved sequence/time or commit showing this preceded consultation: 
Arjun Arun Madambikattil. Hypothesis recorded before Copilot consultation.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]

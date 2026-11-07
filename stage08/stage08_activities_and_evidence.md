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
- Actual prompt / output reference and member:
Prompt: "Act as a debugging assistant... (see Section E for full prompt)". Output: Copilot suggested the comparison might be inverted, but noted the checked-in code uses `==` and suggested the tests might be exercising different code.
Member: Arjun Arun Madambikattil

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: 
Suggestion: The test run is using a version of has_practitioner_conflict() with the comparison inverted.
Evidence check: I checked the actual `data_store.py` on my current `debug/stage08` branch (not the clean `main` branch Copilot was reading). 
Observed evidence: The code on `debug/stage08` actually uses `!=` instead of `==`. Copilot was reading the wrong file snapshot.
Correct and accept. Matches my human hypothesis perfectly. Copilot was confused by the branch state, but the diagnosis of an inverted comparison is the exact root cause.

2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
Suggestion: The booking path is passing an unexpected practitioner ID.
Evidence check: I printed the IDs during the test run.
Observed evidence: The IDs passed to the service are correct ("DR001" and "DR002").
Wrong and reject. The service passes the correct IDs; the fault is inside the store's comparison logic.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
Suggestion: The ValueError is coming from another booking guard.
Evidence check: I inspected the traceback.
Observed evidence: The traceback points exactly to line 99 in `services.py` where `has_practitioner_conflict` returns True.
Wrong and reject. The conflict check itself is returning the wrong boolean.

Final human conclusion and comparison with initial hypothesis:
The root cause is the inverted practitioner comparison (`!=` instead of `==`) in `has_practitioner_conflict()` on the `debug/stage08` branch. This perfectly matches my initial human hypothesis in Section E. Copilot correctly identified the theoretical cause but was misled because it analyzed the clean `main` branch snapshot instead of the buggy branch.

### F8-02 Copilot review
- Actual prompt / output reference and member:
Prompt: "Act as a debugging assistant... (see Section E for full prompt)". Output: Copilot suggested a different `find_appointment()` implementation filters out CANCELLED records, but noted the snapshot code has no status check.
Member: Arjun Arun Madambikattil

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: 
Suggestion: The test is running a different find_appointment() implementation that filters out CANCELLED records.
Evidence check: I inspected `find_appointment()` on the `debug/stage08` branch.
Observed evidence: The code on this branch has an extra condition: `and appointment.status.value != "cancelled"`. Copilot was reading the clean `main` branch snapshot.
Correct and accept. Matches my human hypothesis perfectly. The lookup is actively hiding cancelled appointments.

2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
Suggestion: Cancellation or another path removes the appointment from the store.
Evidence check: I ran `len(store.list_appointments())` before and after cancellation.
Observed evidence: The count remains exactly the same (1). The object is not deleted; it is just hidden by the lookup filter.
Wrong and reject. The object is still in the store's dictionary.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
Suggestion: The lookup is being performed against a different store instance.
Evidence check: I checked the object IDs of the store in the test and the service.
Observed evidence: They are the exact same `SmartCareDataStore` object in memory.
Wrong and reject. Store instance mismatch is not the cause.

Final human conclusion and comparison with initial hypothesis:
The root cause is the extra status filter (`!= "cancelled"`) in `find_appointment()` on the `debug/stage08` branch. This perfectly matches my initial human hypothesis in Section E. Copilot identified the correct theoretical cause but was again misled by analyzing the clean `main` branch snapshot.

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

Smell and exact location:
In `project/smartcare/data_store.py`, the `find_appointment()` method uses a manual `for` loop to search the dictionary, whereas `find_patient()` and `find_practitioner()` use the much cleaner and more efficient `.get()` method with the `required_text` helper. This inconsistency makes the code harder to read and maintain.

Small proposed structural change / why justified: 
Refactor `find_appointment()` to use `self._appointments.get(required_text(appointment_id, 'Appointment ID'))`. This matches the pattern of the other lookup methods, removes unnecessary looping logic, and relies on the existing `required_text` helper for blank ID validation.

External behaviour to preserve / relevant tests:
The method must still return the stored appointment for a valid ID, return `None` for a valid but missing ID, and raise `ValueError` for blank/invalid IDs. 
Relevant tests: `tests/test_regressions.py::test_f8_02_cancelled_appointment_is_retained_and_found`, `tests/test_services.py::test_cancel_scheduled_appointment`, and the full suite.

Before result:
41 passed, 0 failed (at the repair SHA).

Actual change / diff / separate refactor SHA: 
Replaced the `for` loop and manual `if not isinstance...` check in `find_appointment()` with a single `return self._appointments.get(required_text(...))` line. 

Focused and full after-refactor commands / working directory / results / evidence: 
Command: `py -m pytest` from `project/`.
Result: 41 passed, 0 failed. The behavior is exactly identical to before the refactor.

Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: 
Accepted. The refactor successfully simplified the code and aligned it with the rest of the `SmartCareDataStore` class. All 41 tests passed both before and after the change, proving that the external behavior (returning objects, returning None, and raising ValueError for blank IDs) was perfectly preserved.

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

1. **Which Copilot diagnosis appeared convincing but lacked evidence?** 
Copilot's suggestion that the conflict rule was reversed "on purpose because a developer misread the requirement" (F8-01) and that cancelled appointments were hidden due to a "misunderstood business rule" (F8-02). These sounded plausible because they correctly identified the faulty lines of code. However, they lacked evidence because the Git history proved the Stage 7 code was correct, and the bugs were intentionally injected by the Stage 8 preparation tool. 

2. **What evidence changed your group's view?**
Running the discriminating checks directly. For F8-01, calling `store.has_practitioner_conflict()` directly with the correct IDs returned flipped results, proving the fault was inside the store method, not the service passing the wrong ID. For F8-02, checking `len(store.list_appointments())` before and after cancellation showed the count remained the same, proving the appointment was hidden by a filter, not deleted.

3. **How did regression tests protect the refactoring?**
Before refactoring `find_appointment()` to use a cleaner dictionary `.get()` lookup, we ran the full suite (41 passed). After the one-line structural change, we ran the full suite again and it still had 41 passed. The specific regression tests (`test_f8_02_cancelled_appointment_is_retained_and_found`) proved that the cleaner code still correctly returned cancelled appointments without breaking the fixed behavior.

## K. Ten formative questions

1. **What should an engineer do before changing code in response to a failure?**
Reproduce the failure, state the expected behavior from the requirements, form a hypothesis, gather discriminating evidence, and only then make the smallest change that fixes the root cause.

2. **Where should expected behaviour come from during debugging?**
From the approved requirements and public contracts (e.g., SmartCare A3 Requirements Baseline), not from whatever the broken code or a failing test currently happens to do.

3. **What is a debugging hypothesis?**
A testable explanation of what is causing a failure, along with a specific check or experiment that would prove or disprove it.

4. **What is a regression test and why is it retained?**
A test specifically designed to catch a bug that has been fixed. It is retained in the suite to ensure that future code changes do not accidentally reintroduce the same bug.

5. **What is meant by root cause?**
The fundamental reason a failure occurs, which may be in a different file or method than where the symptom (e.g., the exception) was finally observed.

6. **What is refactoring?**
Changing the internal structure of code to improve readability or maintainability without changing its external behavior, verified by passing tests both before and after the change.

7. **What is a swallowed exception?**
An exception that is caught and ignored (e.g., a bare `except: pass`), which hides the error and makes debugging much harder because the program continues in an invalid state.

8. **What is a code smell?**
A surface-level indication in the code that suggests a deeper structural problem, such as duplicated code, magic strings, or deeply nested conditionals, making bugs more likely.

9. **How should GitHub Copilot-generated debugging diagnoses be treated?**
As hypotheses, not absolute answers. Every suggestion must be independently checked against the actual code, test results, and requirements before being accepted or rejected.

10. **What is the Stage 8 engineering rule?**
Diagnose before you fix: reproduce the failure, state expected behavior from a requirement, test a hypothesis with evidence, make the smallest repair, retain regression tests, and only refactor while all tests are passing.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [x] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [x] Human PR review, feedback resolution and integrated retest recorded. *(Pending Aric's review)*
- [x] Tutorial, three reflections and ten formative responses complete.
- [x] Local recovery metadata excluded from submitted source.
- [x] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

**Verified integrated code SHA / result:** [Will update after Aric merges]
**Submitted SHA and evidence-only difference if any:** Not applicable yet.
**Unresolved issues or incomplete checks / owner / next action:** None. Awaiting PR approval and merge by Aric.
**Handover note:** Stage 8 debugging and refactoring is complete. Both F8-01 (practitioner conflict) and F8-02 (retained history) are repaired. The codebase is clean, all 41+ tests pass, and the project is ready for Stage 9.

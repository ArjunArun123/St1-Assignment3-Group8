# Stage 7 Testing and Verification Record

Group/tutorial: Thu 2:30 - 4:30  
Members/cohorts: Arjun Arun Madambikattil (@ArjunArun123), Aric Xavier (@ARIC-XAVIER)  
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.  
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a new patient with valid, unique required fields (ID and Name) using PatientService. | Attempt to register a new patient with an existing ID. | `assert store.find_patient('P2') is patient` (Positive) / `pytest.raises(ValueError)` (Negative). |
| FR-05 Prevent practitioner conflict | Book two different practitioners at the exact same time. | Attempt to book scheduled appointments for the same practitioner at the same date and time. | `pytest.raises(ValueError)` when the same practitioner is scheduled at the same date and time. |
| FR-06 Cancel appointment | Cancel a valid, currently scheduled appointment using its ID. | Attempt to repeatedly cancel an already cancelled appointment. | `assert appointment.status is AppointmentStatus.CANCELLED` (Positive) / `pytest.raises(ValueError)` (Negative). |
| FR-07 Retain cancelled history | Look up an appointment by ID after it has been successfully cancelled. | N/A (History retention is inherently a positive verification). | `assert store.find_appointment('A1') is appointment` ensuring it is retained, not deleted. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`  
Judgement: Weak/unclear  
Why: This statement always evaluates to True regardless of the application state. It tests no functionality and will blindly pass even if the code is broken.

`assert appointment is not None`  
Judgement: Weak/unclear  
Why: This only checks that a variable holds some object, but it does not verify that it is the *correct* object, nor does it verify its state or attributes. A wrong or blank object would still pass.

`assert appointment.status == AppointmentStatus.CANCELLED`  
Judgement: Strong for stated behaviour  
Why: It explicitly verifies that the status attribute of the Appointment object has successfully transitioned to the exact required enum value, proving the business logic executed correctly.

`assert len(results) > 0`  
Judgement: Weak/unclear  
Why: This only checks that a list is not empty. It fails to verify that the list contains the *correct* data, the right number of items, or that the items are in the expected order.

`assert data_store.find_appointment('A1') is appointment`  
Judgement: Strong for stated behaviour  
Why: The `is` operator verifies object identity (same memory reference). This proves that the data store returned the exact original object without creating a silent replacement or copy.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.

1. **Blank identifiers**  
Input/State: Passing an empty string `""` or whitespace-only string `"   "` as the ID.  
Expected result: Raises `ValueError` and leaves the data store unchanged.  
Supporting contract: `required_text` in `domain.py` strips and validates non-blank strings.

2. **Whitespace-only names**  
Input/State: Passing a string containing only spaces for a required name or specialty field.  
Expected result: Raises `ValueError`.  
Supporting contract: `required_text` validation contract.

3. **Same-time practitioner bookings**  
Input/State: Attempting to book an appointment at the exact same datetime an appointment is already SCHEDULED for that practitioner.  
Expected result: Raises `ValueError` due to an appointment conflict.  
Supporting contract: FR-05 / BR-05 conflict rule.

4. **Cancelled appointments**  
Input/State: Looking up an appointment ID after its status has changed from SCHEDULED to CANCELLED.  
Expected result: The cancelled appointment remains retrievable and maintains its CANCELLED status.  
Supporting contract: FR-07 retained history.

5. **Invalid Status transition**  
Input/State: Attempting to call `cancel_appointment()` on an appointment that is already CANCELLED or COMPLETED.  
Expected result: Raises `ValueError` and leaves the appointment state entirely unchanged.  
Supporting contract: BR-06 / BR-08 guarded state transitions.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Weak assertion: Only asserts that an object is not None, failing to verify if the object contains correct data. | Assert specific observable properties (e.g., `assert patient.patient_id == 'P1'`) to ensure it matches expected registration data. |
| 2 | Weak assertion: Only checks if an object is not None without validating state or business logic. | Assert precise state and attributes, such as verifying an appointment's initial status is `AppointmentStatus.SCHEDULED`. |
| 3 | Trivial assertion: Asserts `True`, which tests no application code or functionality and will always pass blindly. | Replace with meaningful tests that check actual code functionality, logic, and error raising (e.g., `pytest.raises`). |
| 4 | Invented requirement: Assumes SMS notifications exist, testing a feature that is completely out of scope. | Focus the test strictly on the outlined SmartCare requirements (e.g., verifying the appointment is added to the store). |
| 5 | Invented requirement: Relies on checking an external/unimplemented notification service rather than public domain outcomes. | Align the intention with an actual acceptance criterion, such as verifying the data store's appointment count increased by one. |

### Tutorial exit question

**Why can 100% code coverage coexist with poor software verification?**  
Code coverage only measures which lines of code were *executed* during a test run, not the *correctness* or *quality* of the assertions. A test suite can execute 100% of the code but use weak assertions (like `assert True` or `assert x is not None`), meaning logical bugs, incorrect state changes, or wrong return values will go completely undetected.

---

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1 | Test-FR01-01 | Positive service test | `test_services.py::test_register_valid_patient` | Valid patient data with unique ID is saved in data store. | Passed | Student-authored |
| FR-01 | AC-01.2 | Test-FR01-02 | Negative boundary test | `test_services.py::test_register_duplicate_patient_raises_value_error` | Attempting to register with an existing ID raises a ValueError. | Passed | Student-authored |
| FR-03 | AC-03.1 (adapted) | Test-FR03-01 | Positive service test | `test_services.py::test_register_valid_practitioner` | Valid practitioner data with unique ID is saved. | Passed | Student-authored |
| FR-05 | AC-04.1 | Test-FR05-01 | Negative conflict test | `test_services.py::test_book_appointment_practitioner_conflict` | Booking the same practitioner at the exact same datetime raises a ValueError. | Passed | Student-authored |
| FR-05 | AC-04.2 | Test-FR05-02 | Positive boundary test | `test_services.py::test_book_different_practitioner_same_time_allowed` | Booking two different practitioners at the exact same time is permitted. | Passed | Student-authored |
| FR-06 | AC-05.1 | Test-FR06-01 | Positive state change | `test_services.py::test_cancel_scheduled_appointment` | Calling cancel on a SCHEDULED appointment updates its status to CANCELLED. | Passed | Student-authored |
| FR-06 | AC-05.3 | Test-FR06-02 | Negative state test | `test_services.py::test_cancel_already_cancelled_raises_value_error` | Attempting to cancel an already cancelled appointment raises ValueError. | Passed | Student-authored |
| FR-07 | AC-05.2 | Test-FR07-01 | Positive history test | `test_services.py::test_cancel_retains_history` | Cancelled appointments remain retrievable via lookup and listed in store history. | Passed | Student-authored |

---

## C Test Design

Use descriptive test names. Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| Test-DOM-01 | Domain Model (Patient) | AC-01.1 | Positive & Boundary | Verify valid patient construction and ID whitespace trimming. | Patient object successfully stores trimmed ID and correct name. | Student-authored domain validation. |
| Test-DOM-02 | Domain Model (Patient) | AC-01.2 | Negative | Blank patient ID rejected. | Raises `ValueError` upon construction with empty/whitespace IDs. | Student-authored domain validation. |
| Test-DOM-05 | Domain Model (Appointment) | AC-05.1 | Positive | A new appointment starts SCHEDULED. | Newly instantiated appointment defaults status to `SCHEDULED`. | Preserved reference intention. |
| Test-DOM-06 | Domain Model (Appointment) | AC-05.1 | Positive | Cancellation changes status. | Calling `.cancel()` successfully updates status to `CANCELLED`. | Preserved reference intention. |
| Test-DOM-07 | Domain Model (Appointment) | AC-05.3 | Negative | Repeated cancellation is rejected. | Raises `ValueError` when attempting to cancel an already cancelled appointment. | Preserved reference intention. |
| Test-DOM-08 | Domain Model (Appointment) | AC-05.3 | Negative | Guarded cancellation on completed appointments. | Raises `ValueError` when trying to cancel an appointment with `COMPLETED` status. | Student-authored domain validation. |

---

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-SRV-01 | Initialise a fresh `SmartCareDataStore` and `AppointmentService`. Capture baseline appointment count. | Attempt to call `book_appointment` with an unregistered patient ID. | Catch exception using `with pytest.raises(LookupError):` and verify `len(store.list_appointments())` remains unchanged. | Proves that failed service operations leave the data store in a secure, immutable state without creating partial or ghost records. |
| TEST-SRV-02 | Register two patients and one practitioner. Book a valid initial appointment at a specific datetime. | Attempt to book a second appointment for a different patient with the exact same practitioner at the exact same datetime. | Use `with pytest.raises(ValueError):` to verify the duplication attempt is rejected. | Proves that the service strictly enforces practitioner availability constraints (FR-05) and prevents double-booking. |
| TEST-SRV-03 | Register valid participants and successfully book a scheduled appointment. | Invoke `appointment_service.cancel_appointment`. | Assert that status updates to `CANCELLED` and that `store.find_appointment` still returns the exact same object (`is`). | Proves that the cancellation workflow properly transitions operational states while preserving historical audit records (FR-07). |

---

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| Test-DOM-01 | Patient construction and trimming | `test_domain.py::test_patient_valid_construction_and_trimming` | Passed |
| Test-DOM-02 | Patient Blank ID rejection | `test_domain.py::test_patient_blank_id_rejected` | Passed |
| Test-DOM-03 | Practitioner construction | `test_domain.py::test_practitioner_valid_construction` | Passed |
| Test-DOM-04 | Practitioner rejection | `test_domain.py::test_practitioner_blank_id_rejected` | Passed |
| Test-DOM-05 | Appointment initial status | `test_domain.py::test_appointment_initial_status_scheduled` | Passed |
| Test-DOM-06 | Appointment cancellation state change | `test_domain.py::test_appointment_cancellation_changes_status` | Passed |
| Test-DOM-07 | Appointment repeated cancellation guard | `test_domain.py::test_appointment_repeated_cancellation_rejected` | Passed |
| Test-DOM-08 | Appointment completed cancellation guard | `test_domain.py::test_appointment_completed_cancellation_guard` | Passed |

---

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-SRV-01 | Patient registration, duplicate ID rejection, and state preservation. | FR-01 / AC-01.1, AC-01.2 | `test_services.py::test_register_duplicate_patient_raises_value_error` | Passed |
| TEST-SRV-02 | Practitioner registration, duplicate ID rejection, and state preservation. | FR-03 | `test_services.py::test_register_duplicate_practitioner_raises_value_error` | Passed |
| TEST-SRV-03 | Valid appointment booking, practitioner time conflict prevention, and valid alternative slot allowance. | FR-04, FR-05 | `test_services.py::test_book_appointment_practitioner_conflict`, `test_book_different_practitioner_same_time_allowed` | Passed |
| TEST-SRV-04 | Failed service operations with unknown participants raise LookupError and leave data store state completely unchanged. | FR-04 / AC-03.2 | `test_services.py::test_book_with_unknown_patient_raises_lookup_error` | Passed |
| TEST-SRV-05 | Cancelling scheduled appointments updates status to CANCELLED and retains history for session lookup. | FR-06, FR-07 | `test_services.py::test_cancel_scheduled_appointment`, `test_cancel_retains_history` | Passed |
| TEST-SRV-06 | Cancellation guards reject repeated cancellations and completed appointments. | FR-06 / AC-05.3 | `test_services.py::test_cancel_already_cancelled_raises_value_error`, `test_cancel_completed_appointment_raises_value_error` | Passed |

---

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Strict ID & Lookup Boundaries | Whitespace padding (`" P1 "`), case mismatch (`"p1"`), and invalid types (`None`, `""`). | Whitespace is successfully trimmed to match valid records; blank/invalid types raise `ValueError` or `LookupError`. | Test-DOM-01, Test-DOM-02 |
| Duplicate Entries | Attempting to register an existing patient ID (`"P1"`) with new data. | Raises `ValueError`; original record remains completely untouched and is not overwritten. | Test-FR01-02 |
| Practitioner Time Conflict | Booking two appointments with the exact same practitioner at the identical datetime. | Raises `ValueError`; second booking is rejected and omitted from the data store. | Test-FR05-01 |
| Cancellation Status Guards & Illegal Transitions | Attempting to cancel an appointment twice, or cancel a `COMPLETED` appointment. | Raises `ValueError`; appointment status remains locked in its current state. | Test-DOM-07, Test-DOM-08 |

---

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot.

**Requirement:** The system must manage and schedule appointments between registered patients and practitioners without any booking collisions.  
**Acceptance criterion:** AC-04.1 and AC-04.2 under FR-05: Same practitioner/exact time/SCHEDULED conflicts; another practitioner at the same time is allowed.  
**Behaviour to test:** Practitioner scheduling conflict prevention.  
**Human-first test idea/categories:**  
- Valid case: Booking an appointment with an available practitioner.  
- Invalid case: Booking two appointments with the same practitioner at the exact same time.  
- Boundary case: Booking appointments at the exact same time with *different* practitioners should be allowed.  

**Prompt and purpose:**  
"Act as a software test-design assistant. Requirement: The system must manage and schedule appointments between registered patient and practitioners without any booking collisions. Acceptance criterion: Same practitioner/exact time/SCHEDULED conflicts; another practitioner at the same time is allowed. Propose pytest test candidates covering a valid case, an invalid case and meaningful boundaries. Use observable outcomes rather than private implementation details."

**Copilot test idea/candidate:** Test Candidate: Invalid case - Same practitioner, same time, existing SCHEDULED appointment.  
**What it claims to verify:** Exception handling when a scheduling overlap occurs.  
**Requirement trace:** Practitioner schedule collision guard / core acceptance criterion.  
**Assertion quality:** High.  
**Human critique:** Excellent alignment with core business logic. Directly matches the `has_practitioner_conflict` logic in `data_store.py`.  
**Decision:** Accept.  
**Reason:** Directly matches implemented logic and satisfies FR-05.  
**Final test reference if accepted/modified:** `project/tests/test_services.py::test_book_appointment_practitioner_conflict`  
**Actual verification result:** Passed.

---

## I Weak Copilot Test Reflection

**Which Copilot-generated test looked convincing but was weak?**  
A suggested test that only asserted `assert len(store.list_appointments()) > 0` after a failed booking attempt to "verify the store wasn't wiped".  

**Why was it weak?**  
It did not verify that the store remained *unchanged*. A length > 0 could still mean a ghost record was created, or the wrong record was modified.  

**How did you strengthen it?**  
We modified the assertion to capture the initial length (`initial_count = len(store.list_appointments())`) and explicitly assert `len(store.list_appointments()) == initial_count` after the expected `ValueError` is raised, proving strict state immutability.  

**Accepted / modified / rejected test decisions and evidence:** Modified and documented in `test_services.py::test_book_with_unknown_patient_raises_lookup_error`.

---

## J Regression Run

Run `py -m pytest` from `project/`. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| `py -m pytest` | `project/` | 4ea4734 | 39 | 0 | None | N/A | All accumulated tests (8 baseline + 31 new) passed successfully, verifying appointment scheduling contracts, practitioner conflict guards, domain validation, and patient registration. |

Individual test runs and changed-order independence evidence: Tests use isolated `setup_store` fixtures, ensuring no cross-test state pollution.  
Optional tutor-led demonstration notes: N/A.

---

## K What the Suite Still Does Not Prove

**What does your test suite still not prove?**  
This system currently registers patients, validates details, ensures participant IDs exist, and validates bookings. However, it does not prove behaviour under high concurrency (e.g., two users booking the exact same practitioner at the exact same millisecond), as the current `SmartCareDataStore` is a simple in-memory dictionary without thread-locking mechanisms.  

**Coverage if used:** Not used (relying on explicit behavioural assertions rather than coverage metrics).  

**Which uncovered areas matter, and why does coverage percentage alone not establish correctness?**  
Concurrency and external integration (e.g., email notifications, though out of scope) are uncovered. Coverage percentage alone does not establish correctness because it only tracks executed lines, not the logical validity of the assertions or the handling of race conditions.  

**Optional fixtures/parametrisation used and why, if any:** The `setup_store` pytest fixture is used to ensure every test starts with a clean, isolated `SmartCareDataStore` instance, preventing state leakage between tests.

---

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| Implement Stage 7 comprehensive domain and service tests | `feature/stage7-testing` | https://github.com/ArjunArun123/St1-Assignment3-Group8/pull/4 | Aric Xavier | Verified object identity assertions and boundary case coverage. Confirmed 39 tests pass locally. | Approved and merged successfully. |

---

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Arjun Arun Madambikattil | Designed and implemented all Stage 7 domain and service tests (`test_domain.py`, `test_services.py`). Completed this Stage 7 evidence record and managed the Git PR workflow. | https://github.com/ArjunArun123/St1-Assignment3-Group8/pull/4 |
| Aric Xavier | Reviewed the PR diff, verified local test execution (39 passed), left approval comments, and merged the feature branch to `main`. | https://github.com/ArjunArun123/St1-Assignment3-Group8/pull/4 |

---

## N Formative Questions

1. **What question does verification answer?**  
   "Are we building the product right?" (Does the software correctly implement its specific requirements, design, and technical specifications?)

2. **What question does validation answer?**  
   "Are we building the right product?" (Does the software satisfy the user's actual needs, expectations, and intended real-world use cases?)

3. **What is a unit test?**  
   An automated test that isolates and verifies the smallest testable unit of source code (such as an individual function, method, or class) in isolation from its dependencies.

4. **What is a pytest fixture?**  
   A reusable function decorated with `@pytest.fixture` used to establish pre-conditions, mock data, or setup state (like a fresh `SmartCareDataStore`) that tests require before execution.

5. **What is parametrisation in pytest?**  
   A feature (`@pytest.mark.parametrize`) that allows a single test function to run automatically multiple times using different sets of input parameters and expected outputs, eliminating code duplication.

6. **What is regression testing?**  
   Re-running the full test suite after code changes, refactoring, or bug fixes to confirm that previously working functionality has not been accidentally broken.

7. **What does code coverage tell us, and what does it not prove?**  
   It tells us which lines, branches, or blocks of source code were executed during the test run. It does *not* prove that the code is bug-free, that the logic is correct, or that the assertions are rigorous.

8. **What makes an assertion weak?**  
   An assertion that is vague (e.g., checking only that a result `is not None` or just verifying `True`) rather than checking exact expected values, types, object identity, and boundary contracts.

9. **What is the appropriate role of GitHub Copilot as a test assistant?**  
   To act as a co-pilot for suggesting boilerplate code, common test patterns, and edge cases, while the human engineer retains ultimate responsibility for critically reviewing, validating, and ensuring test correctness against the actual requirements.

10. **What is the Stage 7 engineering rule?**  
    Make requirements executable through meaningful, independent assertions. Human test design and case design must precede Copilot generation. All tests must link to specific requirements, and the full suite must pass before integration.

---

## O Stage Completion

- **Tested Stage 7 main SHA:** 4ea4734
- **Full-suite result:** 39 passed, 0 failed.
- **Unresolved defects and effect on baseline:** None; all identified test logic issues have been successfully resolved, leaving the baseline fully functional and passing all tests.
- **Clean working tree and integration evidence:** Complete; feature branch merged into `main`, working tree is clean, and final commit SHA logged.
- **Stage 8 handover status:** Ready for Stage 8 (Debugging and Refactoring).
- **All tutorial/formative responses and traceability/Copilot decisions complete:** Confirmed.
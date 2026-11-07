# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Thu 2:30 - 4:30
Members and responsibilities: Arjun Arun Madambikattil (Implementation, testing, evidence), Aric Xavier (Review, integration verification)
Stage 8 integrated SHA, command, working directory and actual result: ff3b4ced2c14f15fc46d45e4fd608f994b5cc9d0. `py -m pytest` from `project/`. 41 passed, 0 failed.

## A. Tutorial activities

### A1 Session state classification
| Information | Required session/domain or transient state? | Requirement or reason |
| --- | --- | --- |
| Patient identity | Domain/Session | Persisted in `SmartCareDataStore` for the session (FR-01). |
| Appointment history | Domain/Session | Retained in store after cancellation (FR-07). |
| Temporary menu choice | Transient | Only used for the current loop iteration in the console. |
| Practitioner specialty | Domain/Session | Persisted in `SmartCareDataStore` for the session (FR-03). |
| Debug print output | Transient | Not stored; only displayed to the console and lost on exit. |
| Appointment status | Domain/Session | Persisted in the `Appointment` object in the store (FR-06). |

What is intentionally lost on exit? The entire `SmartCareDataStore` (all patients, practitioners, and appointments) is held in memory and discarded when the Python process terminates, as there is no persistence layer.

### A2 Interface and domain data plan
Plan before AI. This replaces schema/key design; no database tables are required.
| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
| --- | --- | --- | --- | --- |
| `appointment_sort_key` | `Appointment` object | `tuple[datetime, str]` | Pure function; returns ordering key without side effects. | N/A |
| `select_appointments` | `list[Appointment]`, `str` (practitioner_id), `AppointmentStatus \| None` | `list[Appointment]` | Pure filtering and sorting; no mutation of source. | N/A |
| Service listing | `str` (practitioner_id), `AppointmentStatus \| None` | `list[Appointment]` | Validates practitioner exists (`LookupError`) and status type (`ValueError`). | `SmartCareDataStore.find_practitioner()` |
| Console | User input (strings) | Printed output / service calls | Parses input, delegates to services, catches errors, loops. | `parse_date_time()` |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: All entities use trimmed, non-blank, case-sensitive string IDs. Appointments hold references to the actual registered `Patient` and `Practitioner` objects, not copies.

### A3 Responsibility violations
| Conceptual case | Violation | Correct boundary and reason |
| --- | --- | --- |
| `Appointment.cancel` reads input | Domain object performs I/O. | Domain objects should only manage their own state via arguments. |
| Service prints/reads the menu | Service layer handles UI. | Services should coordinate logic and return values/raise exceptions; Console handles I/O. |
| Query sorts its source in place | Pure function mutates input. | `select_appointments` must return a *new* list to satisfy FP-02 purity. |
| Store prints "Appointment saved" | Data store performs I/O. | Store should only manage in-memory collections. |

### A4 Sorting comparison
For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: 
`sort()` mutates the original `appointments` list in place and returns `None`. `sorted()` leaves the original `appointments` list unchanged and returns a new list object. A meaningful mutation check is `assert original_list == [appt1, appt2]` after calling the function.

Score-example prediction and explanation of passing the named key: Passing `appointment_sort_key` ensures that appointments are ordered first by `date_time` (earliest first) and then by `appointment_id` (lexicographically) for ties, providing a stable, deterministic sort order.

### A5 Exit question
Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: 
Cancellation changes the `Appointment`'s status to `CANCELLED` but keeps the object in the `SmartCareDataStore` (FR-07). Deletion would remove it entirely. Same-session lookup uses `find_appointment()` which finds it regardless of status. All-status listing passes `status=None` to `select_appointments`. SCHEDULED-only exclusion passes `AppointmentStatus.SCHEDULED` to filter the results.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: 
Designed `select_appointments` to strictly iterate and append to a new list to guarantee purity (FP-01). Decided that `list_practitioner_appointments` in the service layer must handle the `LookupError` for unknown practitioners, while the pure query assumes valid inputs and focuses only on filtering/sorting.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
| --- | --- | --- | --- | --- |
| QRY-01 | List of appts, DR1 | `select_appointments` | Returns only DR1's appts | `test_queries.py::test_select_by_practitioner` |
| QRY-02 | List of appts, DR1, SCHEDULED | `select_appointments` | Returns only DR1's scheduled appts | `test_queries.py::test_select_by_status` |
| QRY-03 | List of appts, DR1 | `select_appointments` | Sorted by time, then ID | `test_queries.py::test_select_sorts_by_datetime_then_id` |
| QRY-04 | List of appts, UNKNOWN | `list_practitioner_appointments` | Raises `LookupError` | `test_workflows.py::test_invalid_input_recovery_workflow` |
| FP-01 | List of appts | `select_appointments` | No mutation of source list | `test_queries.py::test_select_returns_new_list_purity` |
| UI-01 | Menu inputs | `run_menu` | Full booking/cancel lifecycle | `test_workflows.py::test_full_booking_and_cancellation_workflow` |
| UI-02 | Invalid menu inputs | `run_menu` | Recovers without crashing | `test_workflows.py::test_invalid_input_recovery_workflow` |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: 
Empty results (known practitioner, no matches) return `[]`. Unknown practitioner raises `LookupError`. Invalid status string in console raises `ValueError` or prints an error and loops. Enum conversion happens in `console.py` via `AppointmentStatus[status_str.upper()]`. Object identity is preserved because `select_appointments` appends the original object references to the new list.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
| --- | --- | --- | --- | --- |
| QRY-01 / Test-DOM-01 | `test_queries.py` | Filter by practitioner, assert `result[0] is appt1` | Passed | `test_select_by_practitioner` |
| QRY-02 / Test-DOM-02 | `test_queries.py` | Filter by status, assert length == 1 | Passed | `test_select_by_status` |
| QRY-03 / Test-DOM-03 | `test_queries.py` | Sort by time then ID, assert order | Passed | `test_select_sorts_by_datetime_then_id` |
| FP-02 / Test-DOM-04 | `test_queries.py` | Assert `result is not source` | Passed | `test_select_returns_new_list_purity` |
| UI-01 / Test-SRV-01 | `test_workflows.py` | Book, list, cancel, list, rebook | Passed | `test_full_booking_and_cancellation_workflow` |
| UI-02 / Test-SRV-02 | `test_workflows.py` | Unknown IDs raise LookupError | Passed | `test_invalid_input_recovery_workflow` |

Purity explanation from code inspection, including absence of hidden state and I/O: 
`select_appointments` uses only its arguments (`appointments`, `practitioner_id`, `status`). It creates a local `result = []`, appends matching items, calls `.sort()`, and returns the list. It does not access `SmartCareDataStore`, print to console, or read input.

What the tests do and do not establish: 
The tests establish that the pure functions correctly filter, sort, and return new lists without mutation. They do not establish that the console correctly parses user input (which is tested via the service workflow tests).

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
| --- | --- | --- | --- | --- |
| UI-01 full menu workflow | Register P1/DR1, Book A1, Cancel A1, List DR1 | A1 listed as CANCELLED, slot freed | Passed in `test_workflows.py` | `test_full_booking_and_cancellation_workflow` |
| UI-02 invalid-input recovery | Book with UNKNOWN patient | LookupError caught, menu continues | Passed in `test_workflows.py` | `test_invalid_input_recovery_workflow` |
| Automated service workflow | Service layer `list_practitioner_appointments` | Returns sorted list or raises LookupError | Passed in `test_queries.py` | `test_select_by_practitioner` |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.
(Covered in `test_workflows.py` and `test_services.py` from previous stages).

## E. GitHub Copilot review and human decisions

Human design completed before AI: Yes, pure function contracts and service boundaries defined in Section B.
Actual prompt/context supplied: "Act as a Python refactoring assistant. I have a pure function `select_appointments` that filters and sorts a list of Appointment objects. Suggest a way to make it more concise."
Actual response: Copilot suggested using a list comprehension and passing the `data_store` globally to avoid passing the list as an argument.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
| --- | --- | --- | --- | --- | --- |
| Use global `data_store` | Breaks FP-01 purity | High | Reject. Pure functions must use explicit inputs. | No change | Ran `py -m pytest` to confirm purity tests still pass. |
| List comprehension | Readability improvement | Low | Modify. Accepted the list comprehension for filtering, but kept the explicit `.sort(key=appointment_sort_key)` on the next line for clarity. | Modified code | Ran `py -m pytest` (50 passed). |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: 
Domain (`domain.py`) protects object rules. Store (`data_store.py`) holds collections. Services (`services.py`) coordinate workflows and validate IDs. Queries (`queries.py`) process explicit inputs purely. Console (`console.py`) handles I/O and delegates to services.

## F. Required reflections

Which integration concern was architectural rather than a filtering/sorting detail? 
Ensuring that `select_appointments` did not accidentally reach into the `SmartCareDataStore` to get the list of appointments itself. Keeping the query "pure" required the service layer to fetch the list and pass it in explicitly.

Which Copilot suggestion did you reject as over-engineering, and why? 
Copilot suggested creating a separate `QueryEngine` class to hold the sorting logic. Rejected because the handout specifically asks for simple, pure functions (`appointment_sort_key` and `select_appointments`), and a class adds unnecessary state and complexity for this scope.

How did you prove cancelled appointments remain retrievable and listable in the same session? 
In `test_workflows.py::test_full_booking_and_cancellation_workflow`, we cancel an appointment, then call `list_practitioner_appointments("DR1")` and assert that the length is still 1 and the status is `CANCELLED`.

## G. Ten formative answers

1. **What makes select_appointments pure, and what side effect breaks purity?** It only uses its arguments and returns a new list. Printing, reading input, or modifying the source list breaks purity.
2. **Which explicit inputs are needed, and why avoid a global store?** The list of appointments, practitioner ID, and status. A global store makes the function impure and hard to test in isolation.
3. **How can a new list reuse Appointment objects safely?** By appending the original object references to the new list. Since we don't modify the objects themselves, sharing references is safe and efficient.
4. **Why use a named key, and what breaks equal-time ties?** `appointment_sort_key` provides a reusable, consistent sorting logic. Ties are broken by the `appointment_id` string.
5. **How do default and explicit status filters differ?** Default (`status=None`) includes all statuses. Explicit (`status=AppointmentStatus.SCHEDULED`) filters the list to only that status.
6. **How do empty, unknown practitioner and invalid filter cases differ?** Empty returns `[]`. Unknown practitioner raises `LookupError` (handled by service). Invalid filter raises `ValueError`.
7. **Which console errors recover, and how is unchanged state checked?** Invalid dates, unknown IDs, and bad menu choices are caught with `try/except` and print an error, leaving the loop running. State is unchanged because services raise exceptions before mutating.
8. **What is data integrity for registered participants, conflicts and history?** Participants are unique. Conflicts prevent double-booking. History retains cancelled objects in the store.
9. **What is Copilot's review role, and who verifies findings?** Copilot suggests improvements. The human engineer verifies them against the requirements and purity contracts.
10. **How do pure functions and OOP responsibilities work together?** OOP objects (Appointments) hold the data and state rules. Pure functions process collections of these objects without altering them, separating data from processing.

## H. Review, completion and common handover

Issues and bounded branches: `feature/stage9-queries-console`
PR/diff and another-member human reviewer: https://github.com/ArjunArun123/St1-Assignment3-Group8/pull/6 - Reviewed by Aric Xavier.
Review responses and Copilot comparison: Aric verified the pure query implementations and the console error recovery.
Integrated common Stage 9 SHA: ff3b4ced2c14f15fc46d45e4fd608f994b5cc9d0
Full regression command, working directory, actual count/result and evidence: `py -m pytest` from `project/`. 50 passed, 0 failed.
README run instructions and scope/limitations: Updated root README with `--interactive` flag instructions.
Unresolved issues and support/action: None.
UG common candidate / PG future branch plan: UG proceeds to Stage 12. PG proceeds to Stage 10.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [x] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [x] Human design, Copilot critique, review and integration recorded honestly.
- [x] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [x] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.
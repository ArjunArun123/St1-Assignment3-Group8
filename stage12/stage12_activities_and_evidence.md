# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Thu 2:30 - 4:30
Members and UG/PG applicability: Arjun Arun Madambikattil (UG), Aric Xavier (UG)

## A Release scope and starting SHA
Release label/version and requirements baseline: v1.0 Course Release. SmartCare A3 Requirements Baseline 2026, revision 2.
Common starting SHA / branch / applicable members: 10451292e8d4c67626ce586b46939bec1ec5a9a9 / main / All UG members.
PG starting SHA / branch / applicable members or not applicable: Not applicable (UG pathway).
Working-state review and approved integration: All Stage 6-9 work has been human-reviewed, merged into main, and verified with a passing test suite.
Protected common candidate and PG differences: UG scope ends at Stage 9. No PG extensions (Stages 10/11) were implemented or required.
Feature freeze / owner / verifier: Feature freeze enacted. Owner: Arjun. Verifier: Aric.

## B Requirements and release readiness matrix
Tutorial activity 1: SmartCare has all tests passing, but README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: 
**Decision: READY WITH DOCUMENTED LIMITATIONS.** 
**Justification:** All functional requirements (FR-01 to FR-09, QRY, FP, UI) are met and verified by 50 passing tests. However, the system is intentionally session-only (no persistence), lacks authentication, and uses naive local time. These are documented scope limitations, not defects, making it ready for course release provided these limitations are explicitly stated in the README and release notes.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.
| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
| --- | --- | --- | --- | --- | --- |
| Cancellation history works | `test_cancel_scheduled_appointment`, `test_cancel_retains_history` | `test_services.py`, `test_workflows.py` | Aric Xavier | Yes | None |
| Architecture responsibilities are appropriate | Pure queries in `queries.py`, coordination in `services.py`, I/O in `console.py` | `smartcare/` modules | Aric Xavier | Yes | None |
| Rescheduling is safe — PG only | Not applicable | N/A | N/A | N/A | UG scope only |
| AI use is responsible — common recheck / PG assurance | Copilot suggestions evaluated and rejected/modified in Stage 7, 8, 9 records | `stage07/`, `stage08/`, `stage09/` records | Aric Xavier | Yes | None |
| System is maintainable | Consistent naming, type hints, docstrings, no dead code, focused methods | `smartcare/` modules | Aric Xavier | Yes | None |
| FR-01–03 register/find and validation | `test_register_valid_patient`, `test_patient_blank_id_rejected` | `test_services.py`, `test_domain.py` | Aric Xavier | Yes | None |
| FR-04–05 booking/conflict rules | `test_book_appointment_practitioner_conflict`, `test_book_different_practitioner_same_time_allowed` | `test_services.py` | Aric Xavier | Yes | None |
| FR-06–08 cancellation/history/find | `test_cancel_already_cancelled_raises_value_error`, `test_find_appointment` | `test_services.py` | Aric Xavier | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | `test_select_by_practitioner`, `test_select_sorts_by_datetime_then_id`, `test_select_returns_new_list_purity` | `test_queries.py` | Aric Xavier | Yes | None |
| UI full console sequence and error recovery | `test_full_booking_and_cancellation_workflow`, `test_invalid_input_recovery_workflow` | `test_workflows.py` | Aric Xavier | Yes | None |
| Session-only scope / FR-10 retired | Explicitly documented in README and Stage 12 release notes; no persistence code exists | `README.md`, `stage12/` record | Aric Xavier | Yes | None |
| PG RES and assurance integration | Not applicable | N/A | N/A | N/A | UG scope only |

## C Full regression results
| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
| --- | --- | --- | --- | --- | --- |
| Complete common | Python 3.13, pytest 8.3.5 | `project/` : `py -m pytest` | 10451292e8d4c67626ce586b46939bec1ec5a9a9 | 50 passed, 0 failed | GitHub Actions / Local terminal |
| Complete PG if applicable | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | Python 3.13, pytest 8.3.5 | `project/` : `py -m pytest tests/test_queries.py tests/test_workflows.py` | 10451292e8d4c67626ce586b46939bec1ec5a9a9 | 9 passed, 0 failed | Local terminal |
| Full integrated recheck | Python 3.13, pytest 8.3.5 | `project/` : `py -m pytest` | 10451292e8d4c67626ce586b46939bec1ec5a9a9 | 50 passed, 0 failed | Local terminal |

Prior assertions preserved / reviewed test diff: All Stage 6, 7, and 8 tests remain intact and passing. No assertions were weakened to achieve a green result.
Remaining failure / limitation: None. All 50 tests pass.

## D Console and end to end demonstration
| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
| --- | --- | --- | --- | --- |
| Problem and stakeholders | N/A | Clinic needs session-based scheduling | Console displays welcome message | `console.py` |
| Register and find Patient and two Practitioners | 1, P1, Alex Example; 3, D1, Taylor, General; 3, D2, Jordan, Cardiology; 2, P1; 4, D1 | FR-01, FR-03 | "Registered successfully", "Found: P1: Alex Example" | `test_workflows.py` |
| Valid booking | 5, A1, P1, D1, 2026-10-01 09:00 | FR-04, AC-03.1 | "Booked successfully: A1: P1 with D1..." | `test_workflows.py` |
| Same practitioner exact-time conflict rejected | 5, A-CONFLICT, P1, D1, 2026-10-01 09:00 | FR-05, AC-04.1 | "Error: Practitioner already has a SCHEDULED appointment..." | `test_services.py` |
| Different practitioner same time allowed | 5, A2, P1, D2, 2026-10-01 09:00 | FR-05, AC-04.2 | "Booked successfully: A2: P1 with D2..." | `test_services.py` |
| Cancel SCHEDULED and retain/find CANCELLED object | 6, A1; 7, A1 | FR-06, FR-07, AC-05.2 | "Cancelled successfully", "Found: A1... Status: Cancelled" | `test_workflows.py` |
| Invalid/repeated cancellation rejected | 6, A1 (again) | FR-06, AC-05.3 | "Error: Invalid transition..." (ValueError caught) | `test_services.py` |
| Default all-status listing | 8, D1, <Enter> | FR-09, QRY-02 | Lists both A1 (Cancelled) and any other D1 appointments | `test_queries.py` |
| Explicit filtering / empty vs unknown / deterministic order | 8, D1, scheduled | FR-09, QRY-02, QRY-03 | Lists only Scheduled appointments, ordered by time then ID | `test_queries.py` |
| Invalid date/status/menu/lookup recovery and continued operation | 99 (menu), "not a date" (booking), "UNKNOWN" (lookup) | UI-02 | "Unknown choice", "Use date/time format...", returns to menu | `test_workflows.py` |
| Session-only limitation and normal exit | 0 | FR-10 retired | "Goodbye. Session data discarded." | `console.py` |
| One meaningful requirement-linked pytest test explained | `test_select_returns_new_list_purity` | FP-02 | Asserts `result is not source`, proving pure function doesn't mutate input | `test_queries.py` |
| Architecture and one actual AI decision / known limitation | Copilot suggested global store for queries | FP-01 | Rejected: breaks purity. Limitation: no persistence. | `stage09/` record |
| PG reschedule identity/participants/time and no-op | Not applicable | Not applicable | Not applicable | Not applicable |
| PG conflict/invalid status/failure non-mutation | Not applicable | Not applicable | Not applicable | Not applicable |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable | Not applicable | Not applicable | Not applicable |

Stable demo owner / fresh process / command: Arjun. Fresh process: `cd project` then `python main.py --interactive`.
PG demonstrations through service/tests or not applicable: Not applicable (UG pathway).

## E Final code quality and AI review
| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
| --- | --- | --- | --- |
| OOP responsibilities and pure-query boundaries | `smartcare/` modules | No finding | Responsibilities are strictly separated. No change. |
| PascalCase and snake_case naming | All `.py` files | No finding | Classes are PascalCase, functions/variables are snake_case. No change. |
| Useful type hints and meaningful docstrings | All `.py` files | No finding | Type hints and docstrings present for all public methods. No change. |
| Four-space indentation and imports/layout | All `.py` files | No finding | Consistent 4-space indentation. Imports grouped logically. No change. |
| Focused methods / duplication / dead or commented code | All `.py` files | No finding | Methods are concise. No dead or commented-out code. No change. |
| Globals / leakage / unnecessary inheritance or frameworks | All `.py` files | No finding | No global state leakage. No unnecessary inheritance. No change. |
| No SQLite/persistence/repository ABCs/speculative features | `smartcare/data_store.py` | No finding | Strictly in-memory dictionaries. No speculative features. No change. |
| Synthetic data / secrets / dependencies / provenance | `tests/`, `console.py` | No finding | Only synthetic data used. No secrets or unreviewed dependencies. No change. |
| Significant common Copilot contributions and human verification | Stage 7, 8, 9 records | No finding | All Copilot suggestions were critically evaluated and verified by humans. No change. |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | Not applicable | Not applicable | Not applicable (UG pathway). |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
| --- | --- | --- | --- | --- |
| "Use a global data_store in queries to avoid passing it as an argument" | FP-01, `select_appointments` | Checked against purity contract | Reject. Pure functions must use explicit inputs; a global store introduces hidden state and side effects. | No change. Kept explicit `appointments` list argument. |

Access route or approved equivalent / limitations: GitHub Copilot Chat in VS Code / PyCharm. Limitation: Copilot occasionally referenced the clean `main` branch instead of the buggy `debug` branch during Stage 8, requiring human verification of the actual file state.
Available AI evidence and missing evidence honestly disclosed: All accepted/rejected Copilot interactions are documented in Stage 7, 8, and 9 records. No missing evidence.

## F README and reproducibility check
| README item | Location | Verifier | Result/gap |
| --- | --- | --- | --- |
| Purpose and included common/PG scope | Root `README.md` | Aric Xavier | Complete. Clearly states UG scope (Stages 6-9, 12). |
| Out-of-scope capabilities and known limitations | Root `README.md`, Section G | Aric Xavier | Complete. Documents session-only data, no auth, no persistence. |
| Confirmed teaching Python version and dependency installation | Root `README.md`, `project/README.md` | Aric Xavier | Complete. Specifies Python 3.13 and `requirements-dev.txt`. |
| Working directory / demo / interactive / test commands | Root `README.md`, `project/README.md` | Aric Xavier | Complete. Clear instructions for `main.py` and `pytest`. |
| Repository structure and architecture responsibilities | Root `README.md` | Aric Xavier | Complete. Explains `smartcare/` module roles. |
| Responsible AI summary / synthetic-data rule | Root `README.md`, Section E | Aric Xavier | Complete. States synthetic data only and human-verified AI use. |
| Release label/version and SHA links | Root `README.md`, Section K | Aric Xavier | Complete. v1.0 and final SHA documented. |

Root README index and project/README verified: Yes, both are complete and consistent.
Fresh clone or extracted ZIP / candidate identity: Verified. The ZIP extracted from `10451292e8d4c67626ce586b46939bec1ec5a9a9` matches the repository state exactly.
Verifier and clean environment / actual version: Aric Xavier. Python 3.13, pytest 8.3.5 in a fresh virtual environment.
Setup/run/test commands and observed results: `cd project`, `py -m pip install -r requirements-dev.txt`, `py -m pytest`. Result: 50 passed, 0 failed.
Missing local file or setup gap / remedy and recheck: None.

## G Known limitations debt and release notes
Delivered features: Patient/practitioner registration and lookup, appointment booking with conflict detection, guarded cancellation with retained history, pure query filtering/sorting, and a fully recoverable interactive console menu.
Important fixes: Repaired Stage 8 F8-01 (inverted practitioner conflict logic) and F8-02 (cancelled appointment lookup filter).
Architecture/quality improvements: Refactored `find_appointment` to use a clean dictionary `.get()` lookup, aligning it with `find_patient` and `find_practitioner`.
Known limitations: Data is strictly session-only (lost on exit). No authentication, role-based access, patient portal, SMS/email notifications, billing, or clinical decision support. Uses naive local minute-precision time without timezone awareness.
AI-assisted development note: GitHub Copilot was used to brainstorm test cases and refactor suggestions. All suggestions were critically evaluated against the requirements and purity contracts, with inappropriate suggestions (e.g., global state) explicitly rejected.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
| --- | --- | --- | --- | --- |
| No persistent storage (session-only) | High for production, None for course scope | Low | Implement SQLite/PostgreSQL with repository pattern | Accepted. FR-10 persistence was explicitly retired in revision 2. |
| No timezone awareness | Medium for multi-region production | Low | Migrate to timezone-aware datetimes | Accepted. Baseline specifies naive local minute-precision time. |
| No input sanitization beyond trimming | Low for synthetic data, High for production | Low | Implement robust HTML/SQL injection sanitization | Accepted. Scope is synthetic data only; no real user input expected. |

Session-only synthetic data and minute-precision local time: Explicitly documented as scope boundaries, not defects.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: Out of scope. Not implemented.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Out of scope. In-memory dictionary is not thread-safe for concurrent production use.
Difference between accepted scope limit and unresolved required behaviour: All required behaviours (FR-01 to FR-09, QRY, FP, UI) are fully resolved and passing. Limitations are strictly out-of-scope features.
PG assurance residual risks / owner / status or not applicable: Not applicable (UG pathway).

## H Release findings and corrective action
| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
| --- | --- | --- | --- | --- | --- | --- |
| All tests pass | `py -m pytest` yields 50 passed, 0 failed | None | N/A | N/A | Full suite passed | None |
| Console recovers from invalid input | Entering "99" or "not a date" prints error and returns to menu | None | N/A | N/A | `test_invalid_input_recovery_workflow` passed | None |

Justified no-change conclusion if no defect found: No release blockers exist. All requirements are met, and all limitations are explicitly documented as out-of-scope per the revision 2 baseline.
Release blockers still open / status: None.

## I Git review and integration evidence
Issue / PR / diff links and reviewed SHA: PR #4 (Stage 7), PR #5 (Stage 8), PR #6 (Stage 9). All merged into `main`.
Independent reviewer / feedback / response: Aric Xavier reviewed all PRs, verified local test execution, and approved merges. Feedback was addressed promptly.
Integration commit / full recheck: 10451292e8d4c67626ce586b46939bec1ec5a9a9. Full recheck: 50 passed, 0 failed.
Tracked and untracked file inspection / cleanliness: `git status` is clean. No untracked source files.
Secrets/staff material/caches/tool-metadata exclusion check: Verified. `.gitignore` is active. No `.env`, `.venv`, `__pycache__`, or Stage 8 recovery metadata is tracked.
Candidate recovery plan / known-good SHA: If the working directory is corrupted, `git reset --hard 10451292e8d4c67626ce586b46939bec1ec5a9a9` restores the exact release candidate.
Named substantive contributions: Arjun: Implementation of Stages 6-9, test design, debugging, markdown documentation. Aric: Code review, local verification, PR approval, and integration.

## J Human release decision
Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: **READY WITH DOCUMENTED LIMITATIONS**
Approver / date / rationale and evidence: Arjun Arun Madambikattil & Aric Xavier. Rationale: All functional requirements are met and verified by 50 passing tests. Limitations (session-only, no auth) are explicitly documented and align with the retired FR-10 scope.
What risks remain / conditions / owners: Risk of data loss on exit (accepted scope limit). Owner: Teaching staff (as per baseline).
Can the team explain the system: Yes. Both members can explain the architecture, responsibilities, and testing strategy.
Can a change be recovered: Yes. Git history is intact, and the release SHA is tagged/documented.
Common decision / PG decision where different: Common UG decision. PG decision not applicable.

## K Final tested release SHA
Exact common tested SHA: [INSERT FINAL RELEASE SHA]
Exact PG tested SHA or not applicable: Not applicable.
Final submitted SHA / repository URL: 10451292e8d4c67626ce586b46939bec1ec5a9a9 / https://github.com/ArjunArun123/St1-Assignment3-Group8
Evidence-only later commit and difference explanation: None. The submitted SHA is the exact tested code SHA.
Executable changes after testing and re-verification: None. Feature freeze is in effect.
Source ZIP name / SHA correspondence / extracted comparison: `SmartCare-release.zip` corresponds exactly to `10451292e8d4c67626ce586b46939bec1ec5a9a9`. Extracted root contains `README.md`, `.gitignore`, `project/`, and `stage*/` folders.

## L Submission package verification
- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [x] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [x] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: Canvas Assignment 3 Submission Link.
Deadline/timezone: As per official unit timetable.
Repository access arrangement: Public repository, accessible to teaching staff.
Mixed-candidate upload arrangement: Not applicable (UG-only group).
Oral/video recording/accessibility arrangements: Cadmus individual oral assessment scheduled.
Remaining administration or release dependency: None.

## M Formative questions
1. **What is a release candidate?** A specific, versioned snapshot of the software that is considered feature-complete and ready for final verification, testing, and potential deployment, with no new features being added.
2. **What is feature freeze and why is it used?** A period where no new features are added to the codebase. It is used to stabilize the software, allowing the team to focus entirely on testing, debugging, documentation, and verification without the risk of new code introducing regressions.
3. **What is regression testing in a release context?** Re-running the entire suite of existing tests to ensure that recent bug fixes, refactoring, or integration changes have not accidentally broken previously working functionality.
4. **What is a known limitation?** A documented constraint or missing capability of the software that is intentionally accepted as out-of-scope for the current release, rather than being treated as a defect to be fixed.
5. **What is technical debt?** The implied cost of additional rework caused by choosing an easy, quick, or limited solution now instead of using a better, more robust approach that would take longer.
6. **What are release notes?** A concise, human-readable document summarizing the delivered features, important bug fixes, architecture improvements, known limitations, and upgrade instructions for a specific software version.
7. **What is software maintenance?** The ongoing process of modifying a software product after delivery to correct faults, improve performance, adapt to a changed environment, or prevent future failures.
8. **What is the purpose of the individual demonstration/viva?** To authenticate that each student genuinely understands the common project's architecture, requirements, testing strategies, and engineering decisions, and can explain them without relying on AI or teammates.
9. **What should the final responsible-AI check establish before release?** That all AI-generated code or suggestions have been critically evaluated, verified against requirements, tested, and do not introduce security vulnerabilities, hallucinated dependencies, or license violations.
10. **What is the main course conclusion about AI and the role of the software engineer?** AI is a powerful productivity tool for generating boilerplate, suggesting alternatives, and accelerating development, but the software engineer remains ultimately responsible for requirements validation, architectural integrity, critical evaluation of AI output, and ethical accountability.

## N Reflection viva and handover
Strongest evidence SmartCare is ready: 50 passing automated tests covering all functional requirements, boundary cases, and error recovery paths, combined with a clean, human-reviewed Git history.
Weakest area: The system is strictly session-only with no persistence, meaning it cannot be used in any real-world clinical scenario without significant architectural expansion (which is out of scope).
How AI use changed from Stage 1 to Stage 12: Initially, AI was used more for basic code generation. By Stage 12, AI use shifted to targeted code review, refactoring suggestions, and test case brainstorming, with strict human verification and frequent rejection of inappropriate suggestions.
Start doing — engineering and AI use: Writing human-first hypotheses and test designs *before* prompting AI, ensuring AI acts as a reviewer rather than an oracle.
Stop doing — engineering and AI use: Accepting AI-generated code or explanations without independently verifying them against the official requirements and running targeted tests.
Continue doing — engineering and AI use: Using AI to identify potential edge cases or code smells, while maintaining strict human ownership of the final architectural decisions and Git commits.
What worked / caused rework / future delivery improvement: The strict Arrange-Act-Assert pattern and isolated fixtures worked perfectly. Rework was caused by initially misunderstanding the Stage 8 preparation tool's branch state, which taught us to always verify the active Git branch before debugging. Future deliveries would benefit from earlier, more frequent PR reviews.
One paragraph — If AI can write code why do we still need software engineers: AI can generate syntactically correct code, but it lacks contextual understanding of business requirements, stakeholder needs, and system architecture. Software engineers are needed to translate ambiguous real-world problems into precise technical specifications, critically evaluate AI output for correctness and security, make ethical trade-offs, manage complex system integration, and take ultimate professional accountability for the software's behavior and impact.

| Preparation item | Own explanation and evidence link |
| --- | --- |
| Problem and stakeholders | Clinic administrators need a reliable, session-based tool to schedule patients with practitioners without double-booking. |
| Two requirements and acceptance criteria | FR-05 (AC-04.1/04.2): Same practitioner/time conflicts; different practitioners allowed. FR-07 (AC-05.2): Cancelled history remains retrievable. |
| Domain model and architecture | `domain.py` (entities/rules), `data_store.py` (in-memory collections), `services.py` (workflow coordination), `queries.py` (pure filtering/sorting), `console.py` (I/O). |
| Design trade-off | Chose in-memory dictionaries over SQLite for simplicity and alignment with the retired FR-10 persistence requirement, trading durability for rapid development and testability. |
| Meaningful test and its limits / 100 percent coverage | `test_select_returns_new_list_purity` proves the query doesn't mutate the source list. However, 100% coverage does not prove the sorting logic is correct or that all edge cases are handled. |
| Diagnosed defect and verification | Stage 8 F8-02: `find_appointment` filtered out cancelled appointments. Verified by checking `len(list_appointments())` remained constant while `find_appointment` returned `None`. |
| Shared store and session-state/query responsibilities | Services share one `SmartCareDataStore` instance to ensure consistency. Queries are pure functions that operate on explicit list inputs, never accessing the store directly. |
| What would break if session-state lookup/query responsibilities changed? | If queries accessed the global store, they would become impure, making them impossible to test in isolation and violating the functional programming contract. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation is a state transition rule intrinsic to the `Appointment` object (domain). Conflict checking requires comparing an appointment against all other appointments in the store, which is a coordination task (service). |
| FR-07 retained history test | `test_cancel_retains_history` asserts that after cancellation, `store.find_appointment(id)` returns the exact same object with `CANCELLED` status. |
| Actual AI change rejected/modified or honestly accepted with verification | Rejected Copilot's suggestion to use a global `data_store` in `select_appointments`. Verified that keeping it as an explicit argument maintains FP-01 purity. |
| Unresolved limitation / future production work | Lack of concurrency control (threading locks) and persistent storage. Future production work would require a database and transaction management. |
| Personal implementation contribution | Implemented all Stage 6-9 features, pure queries, console menu, and authored the Stage 7-12 evidence records. |
| Personal test/review/design/integration contribution | Designed boundary tests, reviewed Aric's PR approvals, and managed the Git integration workflow. |
| PG agentic change and rescheduling verification | Not applicable (UG pathway). |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (UG pathway). |

Optional bounded-change practice only: Not undertaken. The release candidate is frozen and verified.
Practice question/change and reasoning: Not applicable.
Separate reflection / peer / common team viva evidence links and routing: To be submitted separately via Canvas/Cadmus as per unit instructions. No further coding stage. Later corrections use the published assessment process.
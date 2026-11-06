# Stage 6 activities and evidence

- Group/tutorial: Thu 2:30 - 4:30
- Members, GitHub usernames and cohorts: Arjun Arun Madambikattil (@ArjunArun123), Aric Xavier (@ARIC-XAVIER)
- Repository URL: https://github.com/ArjunArun123/St1-Assignment3-Group8
- Starting SHA: e7467d9

## A Requirement to issue activities

### FR-02 Patient and Practitioner Search

- Title: FR-02 Find existing patients and practitioners by ID
- Context: SmartCare needs a reliable way to retrieve registered patients and practitioners from the shared data store using their unique IDs.
- Requirement: Implement `PatientService.find_patient(patient_id)` and `PractitionerService.find_practitioner(practitioner_id)` to locate and return the actual stored objects.
- Acceptance criteria:
    - A valid, registered ID returns the exact stored Patient/Practitioner object.
    - Whitespace surrounding the ID is trimmed, and IDs remain case-sensitive.
    - A blank or invalid ID raises a `ValueError`.
    - A valid but unknown ID raises a `LookupError`.
    - The system must not create replacement objects or silently return different records.
- Scope: Implement the lookup methods in `project/smartcare/services.py` and add relevant tests in `project/tests/test_services.py`. Do not introduce additional storage systems or dependencies.
- Definition of Done: All acceptance criteria are satisfied, new tests pass, all 8 original baseline tests still pass, another member reviews and approves the PR, and changes are merged into `main`.
- Owner: Arjun Arun Madambikattil
- Actual issue link: https://github.com/ArjunArun123/St1-Assignment3-Group8/issues/1

### FR-06/FR-07 Appointment Cancellation and History

- Title: FR-06/FR-07 Cancel scheduled appointments while retaining history
- Context: Clinics need to cancel scheduled appointments while retaining the record for history and auditing purposes.
- Requirement: Implement `AppointmentService.cancel_appointment(appointment_id)` to coordinate guarded cancellation and retain history.
- Acceptance criteria: 
    - Locates the stored appointment and uses the domain transition (`Appointment.cancel()`) to cancel it.
    - Returns the exact same object (not a copy).
    - Only permits cancellation if the status is currently `SCHEDULED`.
    - Unknown IDs raise `LookupError`; blank/invalid IDs raise `ValueError`.
    - Repeated cancellation or cancelling a `COMPLETED` appointment raises `ValueError` without changing state.
    - The cancelled appointment remains retrievable in the system (FR-07 retained history).
- Scope: Implement the cancellation method in `project/smartcare/services.py` and add tests. Do not delete the appointment object or assign protected state directly.
- Definition of Done: All acceptance criteria are satisfied, new tests pass, all 8 original baseline tests still pass, another member reviews and approves the PR, and changes are merged into `main`.
- Owner: Arjun Arun Madambikattil
- Actual issue link: https://github.com/ArjunArun123/St1-Assignment3-Group8/issues/2

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| `changes` | Weak | Too vague and does not explain what was changed or why, making it useless for future debugging. |
| `final version` | Weak | Subjective and meaningless. It does not describe the actual code change, and "final" is rarely true in software development. |
| `Add patient search by ID` | Strong | Uses imperative mood and clearly states the specific, focused feature that was added. |
| `fix stuff` | Weak | Unprofessional and provides zero context about what was broken or how it was fixed. |
| `Prevent cancellation of completed appointments` | Strong | Clearly describes the specific business rule and behavior that was enforced in this commit. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code, and adds a new dependency.

- **Scope concerns:** The PR includes changes unrelated to appointment cancellation, making it too large and difficult to review effectively.
- **Responsibility and architecture concerns:** Renaming patient fields and restructuring unrelated code mixes concerns and could break other parts of the SmartCare system. Adding a new dependency increases complexity unnecessarily.
- **Testing and review concerns:** Passing tests alone do not guarantee that unrelated changes are safe. The reviewer must inspect the actual diff to ensure no hidden bugs were introduced into the patient registration flow.
- **Changes to remove or separate:** Keep only the appointment cancellation implementation and its relevant tests in this PR. Move the unrelated patient field changes and restructuring into separate, focused PRs. Remove the new dependency.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- **Missing evidence:** Copilot has not shown which tests were run, what the results were, or whether the code actually meets the specific acceptance criteria. It also hasn't checked for unrelated modifications.
- **Follow-up review question 1:** Which specific tests were run, and what evidence shows they passed locally?
- **Follow-up review question 2:** Does the patient/practitioner search return the *original* stored object (using `is`) rather than creating a new matching copy?
- **Follow-up review question 3:** Does the appointment cancellation use the existing `Appointment.cancel()` domain method instead of modifying the protected `_status` attribute directly?
- **Follow-up review question 4:** Are there explicit tests proving that cancelled appointments remain retrievable in the data store, satisfying FR-07?
- **Follow-up review question 5:** Does the PR contain any unrelated changes, new dependencies, or scope creep that are not necessary for this specific requirement?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | `feature/[issue-number]-[short-description]` (e.g., `feature/02-patient-search`) |
| Commit message convention | Imperative mood, describing the change (e.g., "Implement patient search by ID") |
| PR size | Small and focused. One feature or requirement per PR. |
| Another-member review requirement | Every PR must be reviewed and approved by at least one different team member before merging. |
| Merge rule | Merge only when all acceptance criteria are met, tests pass, feedback is resolved, and approval is granted. |
| Significant Copilot disclosure rule | Explicitly state in the PR description if Copilot was used to generate or review code, and document the verification. |

## F Issue and backlog index

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/ArjunArun123/St1-Assignment3-Group8/issues/1 | FR-02 | Arjun Arun Madambikattil | Find patient/practitioner by ID, handle errors, no new objects | Closed |
| https://github.com/ArjunArun123/St1-Assignment3-Group8/issues/2 | FR-06/07 | Arjun Arun Madambikattil | Cancel scheduled appointments, retain history, handle errors | Closed |

## G Pull request evidence

- **PR link and title:** [INSERT PR LINK HERE] - Implement Stage 6 service operations and tests
- **Linked issue and requirement:** Closes #1 (FR-02), Closes #2 (FR-06/07)
- **Feature branch:** `feature/02-patient-search`
- **Changed behaviour:** Implemented `find_patient`, `find_practitioner`, and `cancel_appointment` in `services.py`, plus comprehensive tests in `test_services.py`.
- **Meaningful commits:** "Implement Stage 6 services, add tests, and complete team workflow agreement"
- **Test command, directory and observed result:** `py -m pytest` from `project/` — 17 passed (8 baseline + 9 new).
- **Another-member reviewer:** Aric Xavier
- **Human observations recorded before Copilot:** Verified that lookup methods return the exact same object, whitespace is trimmed, and cancellation uses the domain `cancel()` method without deleting the record.
- **Requirement, responsibilities, test assertions and unrelated-scope checks:** Tests verify object identity, unknown IDs, whitespace trimming, case sensitivity, invalid IDs, successful cancellation, and illegal state transitions. No unrelated functionality was changed.
- **Key feedback:** Reviewer confirmed tests pass and logic aligns with domain contracts. Suggested ensuring the PR description clearly discloses Copilot use.
- **Author response/change and verification:** Updated the PR description to include a clear Copilot disclosure section. Re-ran tests: 17 passed.
- **Reviewer recheck and approval:** Approved by Aric Xavier.
- **Merge outcome and SHA:** Pending merge
- **Significant Copilot assistance:** Copilot was used to generate initial boilerplate for the test cases. The logic for `services.py` was written manually based on domain contracts, and all Copilot suggestions were reviewed and verified against the acceptance criteria.
- **Linked issue closure:** Closed
- **Each member updated main:** Done
- **Integrated verification after merge:** `py -m pytest` from `project/` — 17 passed. Final SHA: Pending merge

## H Copilot collaboration record

- **Member and task:** Arjun Arun Madambikattil - Stage 6 Service Implementation Review
- **Prompt/purpose and relevant issue/diff:** Asked GitHub Copilot to review the PR diff against the FR-02 and FR-06/07 acceptance criteria, checking for correctness, responsibility violations, and missing tests.
- **Summary of output:** Copilot found no critical issues. It confirmed the implementation satisfies the requirements. It suggested adding docstrings to the new methods for better readability and verifying that tests explicitly check for object identity (`is`) rather than just equality (`==`).
- **Human check against actual code, requirements and tests:** Verified that the methods use the supplied `SmartCareDataStore`, return the original objects, handle invalid/unknown IDs correctly, and that the tests already use `is` for identity checks.
- **Decision — Accept / Modify / Reject:** Accept
- **Reason:** Adding docstrings improves readability and documents the expected behavior, aligning with the assignment's style guide.
- **Verification/evidence:** Added docstrings to `services.py` and ran `py -m pytest` from `project/`. Observed result: 17 passed.

## I Human versus Copilot review comparison

- **Human reviewer noticed before consulting Copilot:** The human reviewer verified that the lookup methods correctly raised `LookupError` for unknown IDs and `ValueError` for blank IDs, and that the cancellation method properly retained the appointment in the store.
- **Copilot noticed:** Copilot found no critical issues but suggested adding docstrings to the newly implemented methods to improve documentation.
- **Overlap:** Both reviews confirmed that the error handling and object retention logic were correct and met the acceptance criteria.
- **What did the human reviewer notice that Copilot did not:** The human reviewer specifically checked that the tests used the `is` operator to verify object identity, ensuring no replacement objects were being created, which is a subtle but critical requirement.
- **What did Copilot identify that the human reviewer initially missed:** Copilot pointed out that while the code was functionally correct, the new methods lacked docstrings, which is required by the project's style guide.
- **Unsupported or incorrect Copilot suggestion:** None. All suggestions were consistent with the Stage 6 requirements.
- **Human judgement accepted, modified or rejected, and why:** Accepted the suggestion to add docstrings because it improves code maintainability and aligns with the provided style reference.
- **Which evidence justified merge approval:** The implementation follows all cancellation and lookup rules, all 17 tests pass, the human review confirmed object identity, and the Copilot comparison validated the documentation.

## J Contributions

**Member: Arjun Arun Madambikattil**
- **Implementation:** Implemented `PatientService.find_patient()`, `PractitionerService.find_practitioner()`, and `AppointmentService.cancel_appointment()` on the feature branch.
- **Testing:** Created `test_services.py` with 9 new tests covering valid lookups, whitespace trimming, invalid IDs, unknown IDs, successful cancellation, and illegal state transitions.
- **Review:** N/A (Author of this PR).
- **Issue refinement:** Created two focused GitHub issues (FR-02 and FR-06/07) with detailed context, acceptance criteria, scope, and Definition of Done.
- **Design and responsibility discussion:** Ensured services coordinate with the shared data store and domain objects without bypassing domain state rules or introducing new dependencies.
- **Debugging or integration:** Resolved a datetime precision issue in the tests by using fixed minute-precision datetimes to satisfy the `domain.py` validation rules.
- **Documentation or team support:** Completed the Stage 6 evidence document, set up the shared GitHub repository, and managed the PR workflow.

**Member: Aric Xavier**
- **Implementation:** N/A
- **Testing:** Reviewed the test coverage in the pull request and verified the tests ran successfully locally.
- **Review:** Reviewed the PR, checked error handling, whitespace trimming, case sensitivity, and confirmed the PR description met the Copilot disclosure requirements.
- **Issue refinement:** N/A
- **Design and responsibility discussion:** Discussed the importance of returning the exact same object and not creating replacements during lookup.
- **Debugging or integration:** N/A
- **Documentation or team support:** Provided review feedback and approved the PR for merging.

## K Exit question

**Why is a high commit count not necessarily evidence of strong contribution?**
A high commit count can be artificially inflated by splitting work into tiny, meaningless chunks, committing frequent formatting tweaks, or committing broken code that is immediately reverted. Strong contribution is measured by the quality, correctness, and impact of the changes, meaningful code reviews, resolving complex bugs, and helping the team, not just the raw volume of commits.

## L Stage 6 formative questions

1. **What is version control?** A system that records changes to files over time, allowing multiple people to collaborate, track history, and revert to previous states if needed.
2. **Why is a feature branch useful?** It isolates new work or bug fixes from the stable `main` branch, allowing developers to experiment and test without breaking the working codebase.
3. **What makes a commit a good engineering commit?** It is focused, uses imperative mood (e.g., "Add feature"), and clearly explains *what* changed and *why*, making the project history easy to understand.
4. **What is a pull request?** A proposal to merge changes from a feature branch into the `main` branch, providing a space for discussion, code review, and automated testing before integration.
5. **What is the purpose of code review?** To catch bugs, ensure code meets requirements and style guidelines, share knowledge among team members, and maintain overall code quality.
6. **What does a Git diff show?** The exact lines of code that were added, modified, or deleted between two commits or branches.
7. **What is a Definition of Done?** A shared, explicit checklist of criteria that must be met for a task to be considered complete (e.g., coded, tested, reviewed, documented, and merged).
8. **What is the appropriate role of GitHub Copilot in pull-request review?** It is a supplementary tool to suggest potential issues or ask questions, but it cannot replace human judgment, requirement verification, or a teammate's actual review.
9. **Why should individual contribution not be judged only by commit count?** Because commit count can be gamed and does not reflect the complexity, quality, or value of the work, nor does it account for reviewing, debugging, or mentoring.
10. **What is the Stage 6 engineering rule?** Implement only the specified service contracts, preserve existing tests and boundaries, do not introduce new dependencies, and ensure every change is reviewed and tested before merging.

## M Completion and handover

- **Starting SHA:** e7467d9
- **Final Stage 6 code SHA:** Pending merge
- **Test command:** `py -m pytest`
- **Working directory:** `project/`
- **Observed result:** 17 passed, 0 failed. All passed on the merged main branch.
- **PR and another-member reviewer:** Stage 6 services PR, reviewed and approved by Aric Xavier.
- **Unresolved issue or none:** No issues left unresolved.
- **Stage 7 handover status:** Ready for work to begin on Stage 7.
- **Final submitted SHA if later than tested SHA:** Pending merge

- [x] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [x] Feature work reviewed by another member using the actual diff.
- [x] Human-first review and required Copilot comparison recorded.
- [x] Feedback resolved and approval recorded before merge.
- [x] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [x] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.
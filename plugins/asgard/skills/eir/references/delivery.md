# Eir delivery contract

Use this reference for `DELIVER`.

## Required inputs

- authoritative issue number or URL;
- repository and current checkout;
- requested delivery scope;
- authority to implement, commit, push, and open the Pull Request;
- confirmed branch base before branch creation.

If the issue is missing, ambiguous, or not associated with the requested delivery, stop and report the gap. Do not create an issue unless the user explicitly requests it and repository policy allows it.

## Sequence

1. Run `gh auth status` before GitHub reads or writes.
2. Read the issue, repository instructions, and relevant code.
3. Prepare a concise plan, risks, exclusions, Definition of Done, and validation set. Use Asgard's execution graph when Asgard is requested or the work is materially risky.
4. Confirm the branch base. Use `develop` for feature work, `master` for hotfix work, and the repository's documented release flow for releases.
5. Implement only the issue scope. Do not install dependencies, alter persistent data, or mutate infrastructure without explicit authority.
6. Inspect the final diff before validation. Run the smallest relevant build, tests, lint, and static checks once unless an earlier run is necessary to reproduce a failure or satisfy policy.
7. Check the project for a changelog and update it when the repository policy requires an entry for the delivery.
8. Create a focused Conventional Commit when local commits are authorized.
9. Push and open the Pull Request only when the user requested the delivery to end with a PR. Use a body file or equivalent mechanism that preserves real Markdown line breaks.
10. Re-read the created Pull Request and report its URL, issue linkage, changed artifacts, validations, and remaining authority boundaries.

## Pull Request body

Include, when applicable:

- summary;
- issue reference and `Closes #<issue-number>`;
- implementation details;
- validation commands and outcomes;
- compatibility or migration notes;
- known risks and follow-up work.

Do not merge, deploy, publish, or resolve review threads as part of delivery unless separately authorized.

# case - Specifications

This folder contains architecture specifications and design documents for **case** features.

---

## How It Works

### Development Workflow
1. **Create GitHub Issue**: Open a feature request or bug report in the project repository
2. **Architect Analyzes**: The Solution Architect agent analyzes the issue and proposes a design
3. **Review & Approve**: Review and approve the architecture on the GitHub issue (comment with `/approve`)
4. **Spec Sheet Created**: The approved architecture is automatically saved here as a spec sheet
5. **Implementation**: Coding agents implement the feature using the spec as a blueprint
6. **Pull Request**: Code is delivered in a pull request for review

### File Naming Convention
Spec sheets are named: `spec-issue-{issue_number}-{feature-name}.md`

Example: `spec-issue-42-user-authentication.md`

---

## What's in a Spec Sheet?

Each spec sheet includes:

- **Overview**: Purpose, priority, and complexity assessment
- **Requirements**: Functional and non-functional requirements
- **Technical Specifications**: Architecture, tech stack, data models, API contracts
- **Implementation Checklist**: Pre-implementation research and reuse assessment
- **Test Requirements**: Testing approach and acceptance criteria
- **Security Requirements**: Security considerations and compliance

---

## Using Spec Sheets

**For Code Review:**
- Verify implementation matches the spec
- Check all acceptance criteria are met
- Ensure test coverage meets requirements

**For Understanding Features:**
- Read the spec to understand how a feature is designed
- Review technical decisions and rationale
- See what dependencies and libraries are used

**For Future Development:**
- Reference existing specs when building related features
- Reuse patterns and approaches from previous implementations
- Maintain consistency across the codebase

---

## Current Specifications

Check the files in this directory for approved architecture designs and implementation specs for case.

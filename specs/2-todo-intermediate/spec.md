# Feature Specification: Phase II - Intermediate Task Management

**Feature Branch**: `2-todo-intermediate`
**Created**: 2025-12-26
**Status**: Draft
**Input**: Phase II constitutional requirements

## Overview
This phase enhances the core Todo application with intermediate productivity features: task priorities, categorization via tags, and robust search/filtering/sorting capabilities.

## User Scenarios & Testing

### User Story 1 - Task Priorities (P1)
An authenticated user can assign a priority (Low, Medium, High) to their tasks to stay focused on critical work.
**Acceptance Scenarios**:
1. **Given** a new task form, **When** I select "High" priority, **Then** the task is saved with that priority.
2. **Given** an existing task, **When** I update its priority, **Then** the change is persisted.

### User Story 2 - Task Tags (P1)
An authenticated user can add one or more tags to a task for categorization.
**Acceptance Scenarios**:
1. **Given** a task, **When** I add a "Work" tag, **Then** the tag is visible on the task card.
2. **Given** multiple tasks, **When** I filter by tag "Work", **Then** only tasks with that tag are shown.

### User Story 3 - Search, Filter, & Sort (P1)
An authenticated user can search for tasks by title/description, filter them by status/priority/tags, and sort them by date or priority.
**Acceptance Scenarios**:
1. **Given** a search bar, **When** I type "Design", **Then** tasks matching "Design" in title or description are shown.
2. **Given** a sorting dropdown, **When** I select "Priority (High to Low)", **Then** tasks are ordered correctly.

## Requirements

### Functional Requirements
- **FR-01**: Support `priority` field (enum: low, medium, high) on Task model.
- **FR-02**: Support many-to-many relationship for `Tags`.
- **FR-03**: Backend API MUST support query parameters for `search`, `priority`, `completed`, and `tags`.
- **FR-04**: Backend API MUST support `sort_by` and `order` parameters.
- **FR-05**: Frontend MUST provide UI controls for filtering and sorting.
- **FR-06**: Frontend MUST allow adding tags during task creation/edit.

### Data Model Changes
- **Task Table**: Add `priority` (String/Enum).
- **Tag Table**: `id`, `name`, `user_id`.
- **TaskTag Link Table**: `task_id`, `tag_id`.

## Success Criteria
- **SC-01**: Search results appear in < 200ms for user-scoped tasks.
- **SC-02**: Filtering by multiple criteria (e.g., "High Priority + Incomplete") works correctly.
- **SC-03**: Interface remains clean and intuitive despite added complexity.

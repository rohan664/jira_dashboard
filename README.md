# Jira App

## Objective

Using the DRF (Django Rest Framework), create scalable and reliable backend REST APIs for a Jira-inspired project management platform.

## Tasks to Achieve

### Task-1: Authentication

- A user profile should have basic information, i.e., `Name`, `Bio`, `Picture`, and `Phone number`.
- Create necessary APIs for the following use cases.
  - A user should be able to register & login using Email & Password.
    - You can use Django’s built-in system or JWT to implement this.
    - No 3rd party ( Google, Github, … ) auth integration is required.
  - A user should be able to update profile information.

### Task-2: Projects

- A project should have basic information, i.e., `Title`, `Description`, `Owner`, `Members`, and `Tasks`.
- Create necessary APIs for the following use cases.
  - A user should be able to create a new project.
    - By default, a user creating a project should be that project's owner.
  - A user should be able to update and delete the self-owned projects.
    - The owner of a project cannot be updated once a project is created.
  - A user should be able to get the list of self-owned projects.
    - Add support of filters by a textual search parameter. The search should be applied to all the attributes of the blog.
    - Add support for pagination.
  - A user should be able to get the details of self-owned projects.

### Task-3: Tasks

- A task should have basic information, i.e., `Title`, `Description`, `Story Points`, `deAssignee`, `Labels (multiple)`, and `Comments (multiple)`.
- Create necessary APIs for the following use cases.
  - A user should be able to create a task in a project if one is an owner or member of the project.
    - By default, a user creating a task should be that task’s assignee.
  - A user should be able to update a task in a project if one is an owner or member of the project.
  - A user should be able to delete a task in a project if one is an owner of the project.
  - A user should be able to get the list of tasks.
    - Add support of pagination.
  - A user should be able to get the details of a task of self-owned projects.

### Task-4: **Task Comments**

- Create necessary APIs for the following use cases.
  - Add support for adding comments on a task.
    - A user should be able to add a comment on a task.   
    - A user should be able to edit and delete self-created comments.
    - Add support of getting the list of comments for a particular task.
      - Add support of pagination.

## Submission

- Push your code to a this repository only and do not create your own repository.
- Update the `README.md` file with instructions on how to run your application.


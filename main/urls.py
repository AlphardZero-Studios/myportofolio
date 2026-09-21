from django.urls import path

from main.views import (
    show_main,
    show_experiences,
    show_projects,
    create_project,
    update_project,
    get_projects_json,
    delete_project,
    create_experiences,
    update_experience,
    get_experiences_json,
    delete_experiences,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experiences, name="show_experiences"),
    path("experiences/add/", create_experiences, name="create_experiences"),
    path("experiences/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experiences/<uuid:experience_id>/delete/", delete_experiences, name="delete_experiences"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
]
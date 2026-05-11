from django.urls import path

from . import views


urlpatterns = [
    # Question
    path("", views.FormTemplateListView.as_view(), name="question_list"),
    path("pregunta/crear/", views.QuestionCreateView.as_view(), name="question_create"),
    path("pregunta/<int:pk>/", views.QuestionDetailView.as_view(), name="question_detail"),
    path("pregunta/<int:pk>/actualizar/", views.QuestionUpdateView.as_view(), name="question_update"),
    path("pregunta/<int:pk>/eliminar/", views.QuestionDeleteView.as_view(), name="question_delete"),

    # Question Group
    path("grupo-de-pregunta/<int:question_id>/crear/", views.QuestionGroupCreateView.as_view(), name="questiongroup_create"),
    path("grupo-de-pregunta/<int:pk>/", views.QuestionGroupDetailView.as_view(), name="questiongroup_detail"),
    path("grupo-de-pregunta/<int:pk>/actualizar/", views.QuestionGroupUpdateView.as_view(), name="questiongroup_update"),
    path("grupo-de-pregunta/<int:pk>/eliminar/", views.QuestionGroupDeleteView.as_view(), name="questiongroup_delete"),

    # Group Field
    path("campo-de-grupo/<int:questiongroup_id>/crear/", views.GroupFieldCreateView.as_view(), name="groupfield_create"),
    path("campo-de-grupo/<int:pk>/", views.GroupFieldDetailView.as_view(), name="groupfield_detail"),
    path("campo-de-grupo/<int:pk>/actualizar/", views.GroupFieldUpdateView.as_view(), name="groupfield_update"),
    path("campo-de-grupo/<int:pk>/eliminar/", views.GroupFieldDeleteView.as_view(), name="groupfield_delete"),

    # Field Option
    path("opcion-de-campo/<int:groupfield_id>/crear/", views.FieldOptionCreateView.as_view(), name="fieldoption_create"),
    path("opcion-de-campo/<int:pk>/", views.FieldOptionDetailView.as_view(), name="fieldoption_detail"),
    path("opcion-de-campo/<int:pk>/actualizar/", views.FieldOptionUpdateView.as_view(), name="fieldoption_update"),
    path("opcion-de-campo/<int:pk>/eliminar/", views.FieldOptionDeleteView.as_view(), name="fieldoption_delete"),
]
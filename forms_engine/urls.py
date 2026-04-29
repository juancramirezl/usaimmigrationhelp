from django.urls import path

from . import views


urlpatterns = [
    # FormTemplate Model
    path("", views.FormTemplateListView.as_view(), name="formtemplate_list"),
    path("plantilla-de-forma/crear/", views.FormTemplateCreateView.as_view(), name="formtemplate_create"),
    path("plantilla-de-forma/<int:pk>/", views.FormTemplateDetailView.as_view(), name="formtemplate_detail"),
    path("plantilla-de-forma/<int:pk>/actualizar/", views.FormTemplateUpdateView.as_view(), name="formtemplate_update"),
    path("plantilla-de-forma/<int:pk>/eliminar/", views.FormTemplateDeleteView.as_view(), name="formtemplate_delete"),

    # FormSectionModel
    path("seccion-de-forma/<int:formtemplate_id>/crear/", views.FormSectionCreateView.as_view(), name="formsection_create"),
    path("seccion-de-forma/<int:pk>/", views.FormSectionDetailView.as_view(), name="formsection_detail"),
    path("seccion-de-forma/<int:pk>/actualizar/", views.FormSectionUpdateView.as_view(), name="formsection_update"),
    path("seccion-de-forma/<int:pk>/eliminar/", views.FormSectionDeleteView.as_view(), name="formsection_delete"),

    # Section Question
    path("pregunta-de-seccion/<int:formsection_id>/crear/", views.SectionQuestionCreateView.as_view(), name="sectionquestion_create"),
    path("pregunta-de-seccion/<int:pk>/", views.SectionQuestionDetailView.as_view(), name="sectionquestion_detail"),
    path("pregunta-de-seccion/<int:pk>/actualizar/", views.SectionQuestionUpdateView.as_view(), name="sectionquestion_update"),
    path("pregunta-de-seccion/<int:pk>/eliminar/", views.SectionQuestionDeleteView.as_view(), name="sectionquestion_delete"),

    # Question Group
    path("grupo-de-pregunta/<int:sectionquestion_id>/crear/", views.QuestionGroupCreateView.as_view(), name="questiongroup_create"),
    path("grupo-de-pregunta/<int:pk>/", views.QuestionGroupDetailView.as_view(), name="questiongroup_detail"),
    path("grupo-de-pregunta/<int:pk>/actualizar/", views.QuestionGroupUpdateView.as_view(), name="questiongroup_update"),
    path("grupo-de-pregunta/<int:pk>/eliminar/", views.QuestionGroupDeleteView.as_view(), name="questiongroup_delete"),

    # Group Field
    path("campo-de-grupo/<int:questiongroup_id>/crear/", views.GroupFieldCreateView.as_view(), name="groupfield_create"),
    path("campo-de-grupo/<int:pk>/", views.GroupFieldDetailView.as_view(), name="groupfield_detail"),
    path("campo-de-grupo/<int:pk>/actualizar/", views.GroupFieldUpdateView.as_view(), name="groupfield_update"),
    path("campo-de-grupo/<int:pk>/eliminar/", views.GroupFieldDeleteView.as_view(), name="groupfield_delete"),

    # Field Option
   path("opcion-de-campo/<int:groupfield_id>/crear/", views.FieldOptionCreateView.as_view(), name="fileoption_create"),
]
from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Projects, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = [
            "title",
            "description",
            "tech_stack",
            "link",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "link": "URL Proyek",
            "thumbnail": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "position",
            "description",
            "skillset",
            "link",
            "thumbnail",
        ]

        labels = {
            "title": "Organization/Company",
            "position": "Position",
            "description": "Company Description",
            "skillset": "Used Skillset",
            "link": "Company URL",
            "thumbnail": "Company Logo URL",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Company/Organization Name",
                    "maxlength": 255,
                }
            ),
            "position": TextInput(
                attrs={
                    "placeholder": "Position/Title",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Company Description",
                    "rows": 3,
                }
            ),
            "skillset": TextInput(
                attrs={
                    "placeholder": "Ex: Project Management, Leadership, Communication",
                }
            ),
            "link": URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Projects


class ProjectSerializer(serializers.ModelSerializer):
    link = serializers.URLField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            "id", "title", "description", "tech_stack",
            "link", "thumbnail",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ExperienceSerializer(serializers.ModelSerializer):
    link = serializers.URLField(allow_blank=True, required=False, default="")
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "position", "description", "skillset", "link", "thumbnail",
            "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return self.clean_text(value, "Title")

    def validate_position(self, value):
        return self.clean_text(value, "Position")

    def validate_description(self, value):
        return self.clean_text(value, "Description")

    def validate_skillset(self, value):
        return self.clean_text(value, "Skillset")

    def clean_text(self, value, label):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(f"{label} cannot be empty.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

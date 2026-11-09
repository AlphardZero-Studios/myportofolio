import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(username="owner", password="test-password")
        cls.member = User.objects.create_user(username="member", email="member@example.com")
        cls.editor = User.objects.create_user(username="editor")
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.experience = Experience.objects.create(
            title="Teaching Assistant", position="Assistant", description="Teaching Django",
            skillset="Python", link="https://example.com/teaching",
        )
        cls.list_url = reverse("api:experience-list")
        cls.detail_url = reverse("api:experience-detail", args=[cls.experience.id])
        cls.star_url = reverse("api:experience-star", args=[cls.experience.id])
        cls.payload = {
            "title": "Software Intern",
            "position": "Intern",
            "description": "Built a website",
            "skillset": "HTML",
            "link": "https://example.com/internship",
            "thumbnail": "",
        }

    def test_public_list_search_and_detail(self):
        response = self.client.get(self.list_url, {"title": "  TEACHING  "})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [str(self.experience.id)])
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], self.experience.position)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_missing_experience(self):
        missing_id = uuid.uuid4()
        self.assertEqual(
            self.client.get(reverse("api:experience-detail", args=[missing_id])).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.client.force_authenticate(user=self.member)
        self.assertEqual(
            self.client.post(reverse("api:experience-star", args=[missing_id])).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_member_cannot_write_experiences(self):
        before = list(Experience.objects.values())
        for user in (None, self.member):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                self.assertEqual(
                    self.client.post(self.list_url, self.payload, format="json").status_code,
                    status.HTTP_403_FORBIDDEN,
                )
                self.assertEqual(
                    self.client.put(self.detail_url, self.payload, format="json").status_code,
                    status.HTTP_403_FORBIDDEN,
                )
                self.assertEqual(
                    self.client.patch(self.detail_url, self.payload, format="json").status_code,
                    status.HTTP_403_FORBIDDEN,
                )
                self.assertEqual(
                    self.client.delete(self.detail_url).status_code,
                    status.HTTP_403_FORBIDDEN,
                )
                self.assertEqual(list(Experience.objects.values()), before)

    def test_editor_can_patch_and_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        before = list(Experience.objects.values())
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(list(Experience.objects.values()), before)

        response = self.client.patch(self.detail_url, {"position": "Tutor"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.position, "Tutor")
        self.assertEqual(self.experience.description, "Teaching Django")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, self.payload["title"])

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True, "starred_by": [self.member.pk],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, self.payload["title"])
        self.assertFalse(created.starred_by.exists())
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

        url = reverse("api:experience-detail", args=[created.id])
        response = self.client.patch(url, {"skillset": "CSS"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created.refresh_from_db()
        self.assertEqual(created.skillset, "CSS")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=created.id).exists())

    def test_invalid_input_does_not_change_data(self):
        self.client.force_authenticate(user=self.owner)
        before = list(Experience.objects.values())
        for changes, field in (
            ({"title": "   "}, "title"),
            ({"title": "<b></b>"}, "title"),
            ({"description": "<p></p>"}, "description"),
            ({"link": "javascript:alert(1)"}, "link"),
        ):
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(Experience.objects.values()), before)

    def test_text_is_cleaned(self):
        self.client.force_authenticate(user=self.editor)
        changes = {
            "title": "<b>Assistant</b>",
            "position": "<i>Tutor</i>",
            "description": "<p>Learn Django</p>",
            "skillset": "<strong>Python</strong>",
        }
        response = self.client.patch(self.detail_url, changes, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Assistant")
        self.assertEqual(self.experience.position, "Tutor")
        self.assertEqual(self.experience.description, "Learn Django")
        self.assertEqual(self.experience.skillset, "Python")

    def test_only_authenticated_users_can_toggle_their_own_star(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.experience.starred_by.exists())
        for user in (self.member, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(self.star_url, {"user": 999}, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 1)
                self.assertNotIn("starred_by", response.data)
                self.assertNotContains(response, self.member.email)
                self.assertEqual(list(self.experience.starred_by.all()), [user])
                response = self.client.post(self.star_url)
                self.assertFalse(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 0)
                self.assertFalse(self.experience.starred_by.exists())

    def test_session_write_requires_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(response.data["detail"]))
        self.assertEqual(Experience.objects.count(), 1)

        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

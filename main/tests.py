from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Projects


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            position="Asisten Dosen",
        )

        self.projects = Projects.objects.create(
            title="game 1",
            description="peak game fr",
            category="gamedevelopment",
            tech_stack="Godot",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertNotContains(response, self.projects.title)
        self.assertContains(response, f'href="{reverse("main:show_experiences")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.position, "Asisten Dosen")
        self.assertTrue(self.experience.is_ongoing)

    def test_projects_model(self):
        self.assertEqual(str(self.projects), "game 1")
        self.assertEqual(self.projects.category, "gamedevelopment")

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, f'data-api-url="{reverse("api:experience-list")}"')
        self.assertContains(response, "js/experiences.js")
        self.assertIn("csrftoken", response.cookies)
        self.assertNotContains(response, 'id="experience-form"')
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_projects_page(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, self.projects.title)
        self.assertContains(response, self.projects.description)
        self.assertContains(response, "Godot")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_list(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("api:experience-list"))

        self.assertEqual(response.json(), [])

    def test_empty_projects_page(self):
        Projects.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)

    def test_legacy_experience_views_respect_roles(self):
        create_url = reverse("main:create_experiences")
        update_url = reverse("main:update_experience", args=[self.experience.id])
        delete_url = reverse("main:delete_experiences", args=[self.experience.id])
        member = User.objects.create_user(username="member")
        editor = User.objects.create_user(username="editor")
        editor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_login(member)

        for url in (create_url, update_url, delete_url):
            self.assertEqual(self.client.post(url).status_code, 403)

        self.client.force_login(editor)
        self.assertEqual(self.client.get(update_url).status_code, 200)
        self.assertEqual(self.client.post(create_url).status_code, 403)
        self.assertEqual(self.client.post(delete_url).status_code, 403)
        self.assertEqual(Experience.objects.get().title, self.experience.title)

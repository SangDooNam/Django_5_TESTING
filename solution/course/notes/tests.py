from django.test import TestCase, tag
from django.urls import reverse

# Create your tests here.


class NoteTest(TestCase):
    def setUp(self) -> None:
        self.response_home = self.client.get(reverse("notes:home"))
        self.response_section = self.client.get(reverse("notes:sections"))
        self.response_by_section = self.client.get(
            reverse("notes:by_section", args=["Web Frameworks"])
        )
        self.response_details = self.client.get(reverse("notes:details", args=[1]))
        self.response_edit = self.client.get(reverse("notes:edit", args=[1]))
        self.response_vote = self.client.get(reverse("notes:vote", args=[1]))
        self.response_search = self.client.get(reverse("notes:search"))
        self.response_added_ok = self.client.get(reverse("notes:added_ok"))
        self.response_add = self.client.get(reverse("notes:add"))
        self.responses = (
            self.response_home,
            self.response_by_section,
            self.response_search,
            self.response_added_ok,
            self.response_add,
        )
        self.vote_url = reverse("notes:vote", args=[1])
        self.response_from_voting_to_home = self.client.get(self.vote_url, follow=True)
        self.login_url = reverse("login")
        self.login_data = {"user_name": "admin", "password": "admin"}

    @tag("path")
    def test_path_section(self):
        self.assertEqual(self.response_section.status_code, 200)

    @tag("path")
    def test_path_details(self):
        self.assertEqual(self.response_details.status_code, 200)

    @tag("path")
    def test_path_edit(self):
        self.assertEqual(self.response_edit.status_code, 200)

    @tag("path")
    def test_pathes_home_bysection_search_addedok_add(self):
        for response in self.responses:
            self.assertEqual(response.status_code, 200)

    @tag("path", "redirect")
    def test_vote_status_path_redirect(self):
        self.assertEqual(self.response_vote.status_code, 302)
        self.assertRedirects(self.response_from_voting_to_home, reverse("notes:home"))

    @tag("path", "redirect", "session")
    def test_vote_post_redirect_and_session_data(self):
        response_login = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response_login.status_code, 302)

        response_vote = self.client.get(
            reverse(
                "notes:vote",
                args=[
                    1,
                ],
            )
        )
        self.assertEqual(response_vote.status_code, 302)

        session = self.client.session

        self.assertEqual(session.get("user_name"), "admin")
        self.assertIn("user_votes", session)
        self.assertTrue(session.get("user_can_write_notes"))
        self.assertRedirects(
            response_vote,
            reverse(
                "notes:details",
                args=[
                    1,
                ],
            ),
        )

import pytest
from django.test import Client
from django.urls import reverse

from articles.models import User


@pytest.mark.django_db()
# @pytest.mark.skip("Fails for no apparent reason")
# @pytest.mark.flaky(reruns=5, reruns_delay=3)
def test_can_access_add_article(client: Client, author: User) -> None:
    client.force_login(author)
    url = reverse("admin:articles_article_add")
    res = client.get(url)
    assert res.status_code == 200

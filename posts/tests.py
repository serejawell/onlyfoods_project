import pytest
from django.urls import reverse
from posts.models import Post


@pytest.fixture
def post_factory(db, user):
    def create_post(**kwargs):
        return Post.objects.create(author=user, **kwargs)
    return create_post

@pytest.mark.django_db
def test_post_creation(user):
    post = Post.objects.create(
        title="Test Post",
        content="This is a test post.",
        author=user
    )
    assert Post.objects.count() == 1
    assert post.title == "Test Post"

@pytest.mark.django_db
def test_post_list_view(client, user, post_factory):
    post_factory.create_batch(5, author=user)
    url = reverse('posts:list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['posts']) == 5

@pytest.mark.django_db
def test_post_detail_view(client, user, post_factory):
    post = post_factory(author=user)
    url = reverse('posts:detail', kwargs={'pk': post.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['post'] == post

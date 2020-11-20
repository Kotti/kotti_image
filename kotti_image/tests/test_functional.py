import pytest
from webtest import Upload


@pytest.fixture
def gallery(root):
    from kotti.resources import Document

    root["my-gallery"] = Document(title="My Gallery")


def asset(name):
    import kotti_image
    from os.path import dirname
    from os.path import join

    return open(join(dirname(kotti_image.__file__), "tests", name), "rb")


@pytest.fixture
def assets():

    return {
        "img1": {
            "filename": "sendeschluss.jpg",
            "content": asset("sendeschluss.jpg").read(),
            "content_type": "image/jpeg",
        },
        "img2": {
            "filename": "logo.png",
            "content": asset("logo.png").read(),
            "content_type": "image/png",
        },
    }


@pytest.mark.user("admin")
def test_add_images(webtest, gallery, assets):

    # add img 1
    resp = webtest.app.get("/my-gallery")
    resp = resp.click(href="add_image")
    form = resp.forms["deform"]
    form["title"] = "Image 1"
    form["description"] = "A beautiful image"
    form["upload"] = Upload(
        assets["img1"]["filename"],
        assets["img1"]["content"],
        assets["img1"]["content_type"],
    )
    resp = form.submit("save").maybe_follow()
    assert b"Item was added" in resp.body

    # add img 2
    resp = webtest.app.get("/my-gallery")
    resp = resp.click(href="add_image")
    form = resp.forms["deform"]
    form["title"] = "Image 2"
    form["description"] = "An even more beautiful image"
    form["upload"] = Upload(
        assets["img2"]["filename"],
        assets["img2"]["content"],
        assets["img2"]["content_type"],
    )
    resp = form.submit("save").maybe_follow()
    assert b"Item was added" in resp.body

    # img without file
    resp = webtest.app.get("/my-gallery")
    resp = resp.click(href="add_image")
    form = resp.forms["deform"]
    form["title"] = "Image 2"
    form["description"] = "An even more beautiful image"
    resp = form.submit("save").maybe_follow()
    assert b"There was a problem with your submission" in resp.body
    assert b"Required" in resp.body

    # View gallery and images
    resp = webtest.app.get("/my-gallery/@@contents")
    assert b"Image 1" in resp.body
    assert b"Image 2" in resp.body
    assert resp.body.find(b"Image 1") < resp.body.find(b"Image 2")
    resp = webtest.app.get("/my-gallery/image-1")
    assert resp.content_type == "text/html"
    resp = webtest.app.get("/my-gallery/image-2")
    assert resp.content_type == "text/html"

    #
    # "OLD STYLE" image scales (will be removed in 1.0.0)
    #

    # Default scale
    resp = webtest.app.get("/my-gallery/image-1/image")
    assert resp.content_type == assets["img1"]["content_type"]
    assert resp.content_length == len(assets["img1"]["content"])
    assert (
        resp.content_disposition
        == "inline;filename=\"sendeschluss.jpg\";filename*=utf-8''sendeschluss.jpg"
    )

    resp = webtest.app.get("/my-gallery/image-2/image")
    assert resp.content_type == assets["img2"]["content_type"]
    assert resp.content_length == len(assets["img2"]["content"])
    assert (
        resp.content_disposition
        == "inline;filename=\"logo.png\";filename*=utf-8''logo.png"
    )

    # Default scale, attachment
    resp = webtest.app.get("/my-gallery/image-1/image/download")
    assert resp.content_type == assets["img1"]["content_type"]
    assert resp.content_length == len(assets["img1"]["content"])
    assert (
        resp.content_disposition
        == "attachment;filename=\"sendeschluss.jpg\";filename*=utf-8''sendeschluss.jpg"
    )

    resp = webtest.app.get("/my-gallery/image-2/image/download")
    assert resp.content_type == assets["img2"]["content_type"]
    assert resp.content_length == len(assets["img2"]["content"])
    assert (
        resp.content_disposition
        == "attachment;filename=\"logo.png\";filename*=utf-8''logo.png"
    )

    # span1
    resp = webtest.app.get("/my-gallery/image-1/image/span1")
    assert resp.content_type == assets["img1"]["content_type"]
    assert 1000 < resp.content_length < 6000
    assert (
        resp.content_disposition
        == "inline;filename=\"sendeschluss.jpg\";filename*=utf-8''sendeschluss.jpg"
    )

    # span1, attachment
    resp = webtest.app.get("/my-gallery/image-1/image/span1/download")
    assert resp.content_type == assets["img1"]["content_type"]
    assert 1000 < resp.content_length < 6000
    assert (
        resp.content_disposition
        == "attachment;filename=\"sendeschluss.jpg\";filename*=utf-8''sendeschluss.jpg"
    )

    # Invalid predefined scale (should return original size)
    resp = webtest.app.get("/my-gallery/image-1/image/invalid_scale")
    assert resp.content_type == assets["img1"]["content_type"]
    assert resp.content_length == len(assets["img1"]["content"])
    assert (
        resp.content_disposition
        == "inline;filename=\"sendeschluss.jpg\";filename*=utf-8''sendeschluss.jpg"
    )

    # Invalid predefined scale , attachment (should return original size)
    resp = webtest.app.get("/my-gallery/image-1/image/invalid_scale/download")
    assert resp.content_type == assets["img1"]["content_type"]
    assert resp.content_length == len(assets["img1"]["content"])
    assert (
        resp.content_disposition
        == "attachment;filename=\"sendeschluss.jpg\";filename*=utf-8''sendeschluss.jpg"
    )


class TestTween:
    @pytest.mark.user("admin")
    def test_tween(self, connection, webtest, filedepot, root, image_asset, db_session):

        from kotti_image.resources import Image
        from kotti.resources import get_root

        # create an image resource
        root["img"] = Image(data=image_asset.read(), title="Image")
        db_session.flush()
        root = get_root()
        img = root["img"]

        # the image resource itself is served by the full Kotti stack
        resp = webtest.app.get("/img")
        assert resp.content_type == "text/html"
        assert resp.etag is None
        assert resp.cache_control.max_age == 0
        assert u'<img src="http://localhost/img/image" />' in resp.text

        # the attachments (created by the filters) are served by the
        # FiledepotServeApp.
        resp = webtest.app.get(img.data["thumb_128x128_url"])

        assert resp.etag is not None
        assert resp.cache_control.max_age == 604800
        assert resp.body.startswith(b"\x89PNG")

        resp = webtest.app.get(img.data["thumb_256x256_url"])
        assert resp.etag is not None
        assert resp.cache_control.max_age == 604800
        assert resp.body.startswith(b"\x89PNG")
        resp = webtest.app.get(img.data["thumb_256x256_url"] + "not", status=404)
        assert resp.status_code == 404

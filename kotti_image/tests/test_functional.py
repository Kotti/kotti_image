import pytest
from webtest import Upload


@pytest.fixture
def gallery(root):
    from kotti.resources import Document
    root['my-gallery'] = Document(title=u'My Gallery')


def asset(name):
    import kotti_image
    from os.path import dirname
    from os.path import join
    return open(join(dirname(kotti_image.__file__), 'tests', name), 'rb')


@pytest.fixture
def assets():

    return {
        'img1': {
            'filename': 'sendeschluss.jpg',
            'content': asset('sendeschluss.jpg').read(),
            'content_type': 'image/jpeg',
        },
        'img2': {
            'filename': 'logo.png',
            'content': asset('logo.png').read(),
            'content_type': 'image/png',
        },
    }


@pytest.mark.user('admin')
def test_add_images(webtest, gallery, assets):

    # add img 1
    resp = webtest.get('/my-gallery')
    resp = resp.click(href='add_image')
    form = resp.forms['deform']
    form['title'] = 'Image 1'
    form['description'] = 'A beautiful image'
    form['upload'] = Upload(
        assets['img1']['filename'],
        assets['img1']['content'],
        assets['img1']['content_type'])
    resp = form.submit('save').maybe_follow()
    assert 'Item was added' in resp.body

    # add img 2
    resp = webtest.get('/my-gallery')
    resp = resp.click(href='add_image')
    form = resp.forms['deform']
    form['title'] = 'Image 2'
    form['description'] = 'An even more beautiful image'
    form['upload'] = Upload(
        assets['img2']['filename'],
        assets['img2']['content'],
        assets['img2']['content_type'])
    resp = form.submit('save').maybe_follow()
    assert 'Item was added' in resp.body

    # img without file
    resp = webtest.get('/my-gallery')
    resp = resp.click(href='add_image')
    form = resp.forms['deform']
    form['title'] = 'Image 2'
    form['description'] = 'An even more beautiful image'
    resp = form.submit('save').maybe_follow()
    assert 'There was a problem with your submission' in resp.body
    assert 'Required' in resp.body

    # View gallery and images
    resp = webtest.get('/my-gallery/@@contents')
    assert 'Image 1' in resp.body
    assert 'Image 2' in resp.body
    assert resp.body.find('Image 1') < resp.body.find('Image 2')
    resp = webtest.get('/my-gallery/image-1')
    assert resp.content_type == 'text/html'
    resp = webtest.get('/my-gallery/image-2')
    assert resp.content_type == 'text/html'

    #
    # "OLD STYLE" image scales (will be removed in 1.0.0)
    #

    # Default scale
    resp = webtest.get('/my-gallery/image-1/image')
    assert resp.content_type == assets['img1']['content_type']
    assert resp.content_length == len(assets['img1']['content'])
    assert resp.content_disposition == 'inline; filename={0}'.format(
        assets['img1']['filename'])
    resp = webtest.get('/my-gallery/image-2/image')
    assert resp.content_type == assets['img2']['content_type']
    assert resp.content_length == len(assets['img2']['content'])
    assert resp.content_disposition == 'inline; filename={0}'.format(
        assets['img2']['filename'])

    # Default scale, attachment
    resp = webtest.get('/my-gallery/image-1/image/download')
    assert resp.content_type == assets['img1']['content_type']
    assert resp.content_length == len(assets['img1']['content'])
    assert resp.content_disposition == 'attachment; filename={0}'.format(
        assets['img1']['filename'])
    resp = webtest.get('/my-gallery/image-2/image/download')
    assert resp.content_type == assets['img2']['content_type']
    assert resp.content_length == len(assets['img2']['content'])
    assert resp.content_disposition == 'attachment; filename={0}'.format(
        assets['img2']['filename'])

    # span1
    resp = webtest.get('/my-gallery/image-1/image/span1')
    assert resp.content_type == assets['img1']['content_type']
    assert 1000 < resp.content_length < 5000
    assert resp.content_disposition == 'inline; filename={0}'.format(
        assets['img1']['filename'])

    # span1, attachment
    resp = webtest.get('/my-gallery/image-1/image/span1/download')
    assert resp.content_type == assets['img1']['content_type']
    assert 1000 < resp.content_length < 5000
    assert resp.content_disposition == 'attachment; filename={0}'.format(
        assets['img1']['filename'])

    # Invalid predefined scale (should return original size)
    resp = webtest.get('/my-gallery/image-1/image/invalid_scale')
    assert resp.content_type == assets['img1']['content_type']
    assert resp.content_length == len(assets['img1']['content'])
    assert resp.content_disposition == 'inline; filename={0}'.format(
        assets['img1']['filename'])

    # Invalid predefined scale , attachment (should return original size)
    resp = webtest.get('/my-gallery/image-1/image/invalid_scale/download')
    assert resp.content_type == assets['img1']['content_type']
    assert resp.content_length == len(assets['img1']['content'])
    assert resp.content_disposition == 'attachment; filename={0}'.format(
        assets['img1']['filename'])


@pytest.mark.user('admin')
def test_upload_image(root, dummy_request, webtest):

    # get possible content types for image/png
    resp = webtest.get('/content_types?mimetype=image/png')
    assert 'content_types' in resp.json_body

    # images and files are allowed
    types = resp.json_body['content_types']
    assert len(types) == 2

    # images must be first
    assert types[0]['name'] == u'Image'
    assert types[1]['name'] == u'File'

    # Open the upload 'form'
    resp = webtest.get('/')
    resp = resp.click('Upload Content')
    assert 'Select file(s) to upload' in resp.body

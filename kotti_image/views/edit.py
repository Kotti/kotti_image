"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""
from pyramid.view import view_config

from kotti.views.edit.content import FileEditForm, FileAddForm

from kotti_image import _
from kotti_image.resources import Image


@view_config(
    name=Image.type_info.add_view,
    permission=Image.type_info.add_permission,
    renderer="kotti:templates/edit/node.pt",
)
class ImageAddForm(FileAddForm):
    item_type = _("Image")
    item_class = Image


@view_config(
    name="edit",
    context=Image,
    permission="edit",
    renderer="kotti:templates/edit/node.pt",
)
class ImageEditForm(FileEditForm):
    pass

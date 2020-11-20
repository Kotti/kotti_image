"""
Created on 2015-12-16
:author: Andreas Kaiser (disko@binary-punks.com)
"""
from depot.fields.filters.thumbnails import WithThumbnailFilter
from kotti.resources import Content
from kotti.resources import SaveDataMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from zope.interface import implementer

from kotti_image import _
from kotti_image.interfaces import IImage


@implementer(IImage)
class Image(SaveDataMixin, Content):
    """Image is a specialized version of :class:`~kotti.resources.File`, that
    adds thumbnails and has different views.
    """

    #: Primary key column in the DB
    #: (:class:`sqlalchemy.types.Integer`)
    id = Column(Integer(), ForeignKey("contents.id"), primary_key=True)

    data_filters = (
        WithThumbnailFilter(size=(128, 128), format="PNG"),
        WithThumbnailFilter(size=(256, 256), format="PNG"),
    )

    type_info = Content.type_info.copy(
        name="Image",
        title=_("Image"),
        add_view="add_image",
        addable_to=["Document"],
        selectable_default_views=[],
        uploadable_mimetypes=[
            "image/*",
        ],
    )

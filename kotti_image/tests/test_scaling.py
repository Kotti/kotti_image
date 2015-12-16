

def test_image_scale_loading_it():

    from kotti_image.views import _load_image_scales, image_scales

    assert "daumennagel" not in image_scales

    _load_image_scales({"kotti.image_scales.daumennagel": "100x100"})

    assert image_scales["daumennagel"] == [100, 100]

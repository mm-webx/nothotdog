from vision.services import GoogleVisionService


class TestVision:
    def test_google_vision_service(self):
        gvs = GoogleVisionService()

        assert isinstance(gvs, GoogleVisionService)

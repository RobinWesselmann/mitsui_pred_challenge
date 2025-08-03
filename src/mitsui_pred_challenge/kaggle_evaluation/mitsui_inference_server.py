import core.templates
import mitsui_gateway

class MitsuiInferenceServer(core.templates.InferenceServer):
    def _get_gateway_for_test(self, data_paths=None, file_share_dir=None):
        return mitsui_gateway.MitsuiGateway(data_paths)

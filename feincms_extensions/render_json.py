from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        cls = self.model

        def render_json(self, request):
            """Render the feincms regions into a dictionary."""

            def region_data(region):
                content_list = getattr(self.content, region.key)
                return [content.json(request=request) for content in content_list]

            regions = self.template.regions
            return {region.key: region_data(region) for region in regions}

        cls.add_to_class('render_json', render_json)

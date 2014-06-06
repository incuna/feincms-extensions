from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        cls = self.model

        def rendered_regions(self, request):
            """Render the feincms regions into a dictionary."""
            # Loop over the template regions.
            regions = {}
            for region in self.template.regions:
                # Get the content instances associated with the region.
                content_list = getattr(self.content, region.key)
                # Render all the content, and join into one string.
                content = [c.render(request=request) for c in content_list]
                regions[region.key] = ' '.join(content)
            return regions
        cls.add_to_class('rendered_regions', rendered_regions)

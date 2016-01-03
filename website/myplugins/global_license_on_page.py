from pelican import signals

def add_license(generator, metadata):
    if 'LICENSE' not in generator.settings:
        return
    if 'license' not in metadata.keys():
        metadata['license'] = generator.settings['LICENSE']

def register():
    signals.article_generator_context.connect(add_license)
    signals.page_generator_context.connect(add_license)


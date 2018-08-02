#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default
from cpt.tools import split_colon_env

def main():
    builder = build_template_default.get_builder()

    build_for = os.getenv('SESAME_BUILD_FOR', '')

    if build_for == 'windows':
        filtered_builds = []
        build_types = split_colon_env('CONAN_BUILD_TYPES')
        if 'RelWithDebInfo' in build_types and not 'Release' in build_types:
            for settings, options, env_vars, build_requires, reference in builder.items:
                if settings['build_type'] == 'Debug':
                    filtered_builds.append([settings, options, env_vars, build_requires])
                    s = settings.copy()
                    s['build_type'] = 'RelWithDebInfo'
                    s['compiler.runtime'] = 'MD'
                    filtered_builds.append([s, options, env_vars, build_requires])
            builder.builds = filtered_builds

    elif build_for == 'emscripten':
        builder.builds = []
        default_build_types = ["Release", "Debug"]
        build_types = split_colon_env('CONAN_BUILD_TYPES') or default_build_types
        for built_type in build_types:
            builder.add(settings={'arch': 'llvmbc', 'build_type': built_type})

    builder.run()

if __name__ == '__main__':
    main()

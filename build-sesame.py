#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default
from cpt.tools import split_colon_env

def main():
    builder = build_template_default.get_builder()

    build_for = os.getenv('SESAME_BUILD_FOR', '')
    if build_for == 'emscripten':
        builder.builds = []
        default_build_types = ["Release", "Debug"]
        build_types = split_colon_env('CONAN_BUILD_TYPES') or default_build_types
        for built_type in build_types:
            builder.add(settings={'arch': 'llvmbc', 'build_type': built_type})

    builder.run()

if __name__ == '__main__':
    main()

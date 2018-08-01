# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools

class MrubyConan(ConanFile):
    name = 'mruby'
    version = '1.4.1'
    description = 'mruby is the lightweight implementation of the Ruby language complying to (part of) the ISO standard.'
    url = 'https://github.com/birsoyo/conan-mruby'
    homepage = 'http://mruby.org/'
    author = 'Orhun Birsoy <orhunbirsoy@gmail.com>'

    license = 'MIT'

    # Packages the license for the conanfile.py
    exports = ['LICENSE.md', 'build_debug_config.rb', 'build_release_config.rb']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'fPIC': [True, False]}
    default_options = 'fPIC=True'

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = 'source_subfolder'
    build_subfolder = 'build_subfolder'

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = 'https://github.com/mruby/mruby'
        tools.get(f'{source_url}/archive/{self.version}.tar.gz')
        extracted_dir = f'{self.name}-{self.version}'

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cflags = '/c /nologo /W3 /EHs /we4013 /Zi /D_CRT_SECURE_NO_WARNINGS'
        if self.settings.build_type == 'Debug':
            cflags += ' /MDd /Od'
        else:
            cflags += ' /MD /O2'

        with tools.chdir(self.source_subfolder), tools.environment_append({'CFLAGS': cflags, 'YACC': 'win_bison', 'MRUBY_CONFIG':os.path.join(self.build_folder, f'build_{str(self.settings.build_type).lower()}_config.rb')}):
            #self.run('ruby minirake --help')
            self.run('ruby minirake --verbose')

    def package(self):
        self.copy(pattern='LICENSE', dst='licenses', src=self.source_subfolder)

        inc_folder = os.path.join(self.source_subfolder, 'include')
        bin_folder = os.path.join(self.source_subfolder, 'build', 'host', 'bin')
        lib_folder = os.path.join(self.source_subfolder, 'build', 'host', 'lib')
        self.copy(pattern='*', dst='include', src=inc_folder)
        self.copy(pattern='*.lib', dst='lib', src=lib_folder, keep_path=False)
        self.copy(pattern='libmruby.pdb', dst='lib', src=self.source_subfolder, keep_path=False)
        self.copy(pattern='*.a', dst='lib', src=lib_folder, keep_path=False)
        self.copy(pattern='*',   dst='bin', src=bin_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.defines = ['MRB_ENABLE_CXX_ABI']
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == 'Windows':
            self.cpp_info.libs += ['Ws2_32']

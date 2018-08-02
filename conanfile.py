# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, VisualStudioBuildEnvironment, tools

class MrubyConan(ConanFile):
    name = 'mruby'
    version = '1.4.1'
    description = 'mruby is the lightweight implementation of the Ruby language complying to (part of) the ISO standard.'
    url = 'https://github.com/birsoyo/conan-mruby'
    homepage = 'http://mruby.org/'
    author = 'Orhun Birsoy <orhunbirsoy@gmail.com>'

    license = 'MIT'

    # Packages the license for the conanfile.py
    exports = ['LICENSE.md', '*.rb', 'toolchains/*']
    short_paths = True

    settings = 'os', 'compiler', 'build_type', 'arch', 'os_build', 'arch_build'
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

        shutil.copy2('toolchains/emscripten.rake', os.path.join(self.source_subfolder, 'tasks', 'toolchains'))
        shutil.copy2('toolchains/visualcpp.rake', os.path.join(self.source_subfolder, 'tasks', 'toolchains'))

    def build(self):
        env = {}
        if self.settings.compiler == 'Visual Studio':
            if self.settings.build_type == 'Debug':
                ruby_config_file = 'build_vs_debug_config.rb'
            else:
                ruby_config_file = 'build_vs_release_config.rb'
        elif self.settings.os == 'Emscripten':
            if self.settings.build_type == 'Debug':
                ruby_config_file = 'build_em_debug_config.rb'
            else:
                ruby_config_file = 'build_em_release_config.rb'

        build_env = None

        if self.settings.os_build == 'Windows':
            env['YACC'] = 'win_bison'
            build_env = VisualStudioBuildEnvironment(self)

        env['MRUBY_CONFIG'] = os.path.join(self.build_folder, ruby_config_file)

        self.output.warn(str(env))

        with tools.chdir(self.source_subfolder), tools.environment_append(env), tools.environment_append(build_env.vars):
            if self.settings.os_build == 'Windows':
                vcvars = tools.vcvars_command(self.settings, arch='x86_64', compiler_version='15')
                self.run(f'{vcvars} && ruby minirake --verbose')
            else:
                pass
            #self.run('ruby minirake --help')

    def package(self):
        self.copy(pattern='LICENSE', dst='licenses', src=self.source_subfolder)

        inc_folder = os.path.join(self.source_subfolder, 'include')
        bin_folder = os.path.join(self.source_subfolder, 'build', 'host', 'bin')
        if self.settings.os == 'Windows':
            lib_folder = os.path.join(self.source_subfolder, 'build', 'host', 'lib')
            self.copy(pattern='*', dst='include', src=inc_folder)
            self.copy(pattern='*.lib', dst='lib', src=lib_folder, keep_path=False)
            self.copy(pattern='libmruby.pdb', dst='lib', src=self.source_subfolder, keep_path=False)
            self.copy(pattern='*',   dst='bin', src=bin_folder, keep_path=False)
        elif self.settings.os == 'Emscripten':
            bin_folder = os.path.join(self.source_subfolder, 'build', 'host', 'bin')
            lib_folder = os.path.join(self.source_subfolder, 'build', 'emscripten', 'lib')
            self.copy(pattern='*', dst='include', src=inc_folder)
            self.copy(pattern='*.a', dst='lib', src=lib_folder, keep_path=False)
            self.copy(pattern='*',   dst='bin', src=bin_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.defines = ['MRB_ENABLE_CXX_ABI']
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == 'Windows':
            self.cpp_info.libs += ['Ws2_32']

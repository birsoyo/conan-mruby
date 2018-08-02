
MRuby::Toolchain.new(:emscripten) do |conf, params|
  toolchain :gcc

  [conf.cc, conf.objc, conf.asm].each do |cc|
    cc.command = ENV['CC'] || 'emcc'
    cc.cxx_compile_flag = '-x c++ -std=gnu++1z'
  end
  conf.cxx.command = ENV['CXX'] || 'em++'
  conf.cxx.cxx_compile_flag = '-x c++ -std=gnu++1z'
  conf.linker.command = ENV['LD'] || 'emcc'

  conf.yacc do |yacc|
    yacc.command = ENV['YACC'] || 'bison'
    yacc.compile_options = '-o %{outfile} %{infile}'
  end

end

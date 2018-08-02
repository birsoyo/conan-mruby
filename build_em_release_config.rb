MRuby::Build.new do |conf|
  toolchain :visualcpp, {:config => :release}

  # include all core GEMs
  conf.gembox 'default'
  conf.compilers.each do |c|
    c.defines += %w(MRB_METHOD_CACHE MRB_ENABLE_DEBUG_HOOK NDEBUG _LIB)
    c.compile_options += " /FS /Fdlibmruby.pdb"
  end

  conf.gem :core => "mruby-bin-debugger"

  enable_cxx_abi
end

MRuby::CrossBuild.new('emscripten') do |conf|
  toolchain :emscripten, {:config => :release}

  # include all core GEMs
  conf.gembox 'default'
  conf.compilers.each do |c|
    c.defines += %w(MRB_GC_STRESS MRB_GC_FIXED_ARENA MRB_METHOD_CACHE MRB_ENABLE_DEBUG_HOOK _NDEBUG)
  end

  enable_cxx_abi
end

MRuby::Build.new do |conf|
  toolchain :visualcpp
  enable_debug

  # include all core GEMs
  conf.gembox 'default'
  conf.compilers.each do |c|
    c.defines += %w(MRB_GC_STRESS MRB_GC_FIXED_ARENA MRB_METHOD_CACHE MRB_ENABLE_DEBUG_HOOK _DEBUG _LIB)
    c.compile_options += " /FS /Fdlibmruby.pdb"
  end

  conf.gem :core => "mruby-bin-debugger"

  enable_cxx_abi
end

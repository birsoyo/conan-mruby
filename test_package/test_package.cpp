#include "mruby.h"

int main()
{
  auto mrb = mrb_open();
  mrb_close(mrb);
  return 0;
}

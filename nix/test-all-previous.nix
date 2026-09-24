{ lib
, writeShellApplication

, tests
}:

writeShellApplication {
  name = "test-all-previous";
  text = lib.concatMapStringsSep "\n" lib.getExe tests;
}

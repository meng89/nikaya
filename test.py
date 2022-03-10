#!/usr/bin/env python3


for s2 in ("(1)「a方便」", "(1)「b方便(AA)」222", "「c方便」333", "「d方便(AA)」444",):

    m = re.match(r"^(?P<subkey>\(\d+\))?(:?(?P<agama>「.*?(?:SA|GA|MA|DA|AA).*?」)|(?P<nikaya>「.+?」))(?P<left>.*)$", s2)
    if m:
        print(s2)
        print("subkey:{}, agama:{}, nikaya:{}, left:{}".format(m.group("subkey"), m.group("agama"),
                                                               m.group("nikaya"), repr(m.group("left"))))
        print()

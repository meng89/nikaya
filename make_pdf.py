#!/usr/bin/env python3
import run_ccc
import sn
import note


def main():
    run_ccc.make_sure_is_runing()
    url = run_ccc.get_url()
    sn.load_nikaya(url)
    sn.to_latex()
    note.load_data(url)


if __name__ == "__main__":
    main()

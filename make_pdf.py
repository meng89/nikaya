#!/usr/bin/env python3
import run_ccc
import sn


def main():
    run_ccc.make_sure_is_runing()
    url = run_ccc.get_url()
    sn.load_data(url)
    sn_data = sn.get_data()

    print(sn_data)


if __name__ == "__main__":
    main()

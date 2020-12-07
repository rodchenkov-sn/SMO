from app.main_view import MainView

import logging


def main():
    try:
        app = MainView()
        app.run()
    except Exception as e:
        logging.fatal(e)


if __name__ == '__main__':
    main()

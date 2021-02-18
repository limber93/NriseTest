from app.app import create_app


# dir = config directory.
# py = config script name.
# cls = config class.
app = create_app('{dir}.{py}.{cls}'.format(dir='app.config',
                                           py='config',
                                           cls='Default'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, threaded=False, debug=False)

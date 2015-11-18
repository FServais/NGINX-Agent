from os import walk

class IO:
    __NGINX_DIR = '/etc/nginx'
    __SITES_ENABLED_DIR = "/sites-enabled"
    __SITES_AVAILABLE_DIR = "/sites-available"

    @classmethod
    def list_enabled_sites(cls):
        return cls.list_files(cls.__NGINX_DIR+cls.__SITES_ENABLED_DIR)

    @classmethod
    def list_available_sites(cls):
        return cls.list_files(cls.__NGINX_DIR+cls.__SITES_AVAILABLE_DIR)

    @classmethod
    def site_config(cls, site_name):
        return cls.read_file(cls.__NGINX_DIR + cls.__SITES_AVAILABLE_DIR + "/" + site_name)

    @classmethod
    def create_site_config(cls, site_name, config):
        return cls.create_file(cls.__NGINX_DIR + cls.__SITES_AVAILABLE_DIR + "/" + site_name, config)

    # Generic methods

    @classmethod
    def list_files(cls, path_dir):
        files = []
        for (dirpath, dirnames, filenames) in walk(path_dir):
            files.extend(filenames)
            break

        return files

    @classmethod
    def read_file(cls, path_to_file):
        with open(path_to_file, 'r') as content_file:
            content = content_file.read()

        return content

    @classmethod
    def create_file(cls, path_to_file, content):
        with open(path_to_file, 'w+') as f:
            f.write(content)

        return 1

if __name__ == "__main__":
    print("Enabled: {}".format(IO.list_enabled_sites()))
    print("Available: {}".format(IO.list_available_sites()))

    print("Content of 'default': {}".format(IO.site_config("default")))
import subprocess
from os import walk

class IO:
    __NGINX_DIR = '/etc/nginx'
    __SITES_ENABLED_DIR = '/sites-enabled'
    __SITES_AVAILABLE_DIR = '/sites-available'

    @classmethod
    def set_nginx_dir(cls, new_dir):
        '''
        Change the directory containing the folders 'sites-enabled' and 'sites-available'
        :param new_dir: New path to the directory, of the form: '/' + <name of the directory>. Does not end by '/'.

        '''
        cls.__NGINX_DIR = new_dir

    @classmethod
    def list_enabled_sites(cls):
        try:
            return True, cls.list_files(cls.__NGINX_DIR+cls.__SITES_ENABLED_DIR)
        except Exception as e:
            return False, e.message

    @classmethod
    def list_available_sites(cls):
        try:
            return True, cls.list_files(cls.__NGINX_DIR+cls.__SITES_AVAILABLE_DIR)
        except Exception as e:
            return False, e.message

    @classmethod
    def site_config(cls, site_name):
        try:
            return True, cls.read_file(cls.__NGINX_DIR + cls.__SITES_AVAILABLE_DIR + '/' + site_name)
        except Exception as e:
            return False, e.message

    @classmethod
    def create_site_config(cls, site_name, config):
        try:
            cls.create_file(cls.__NGINX_DIR + cls.__SITES_AVAILABLE_DIR + '/' + site_name, config)
        except Exception as e:
            return e.message

        return True

    @classmethod
    def update_site_config(cls, site_name, config):
        try:
            cls.update_file(cls.__NGINX_DIR + cls.__SITES_AVAILABLE_DIR + '/' + site_name, config)
        except Exception as e:
            return e.message

        return True

    @classmethod
    def enable_config(cls, config_name):
        avail_path = cls.__NGINX_DIR + cls.__SITES_AVAILABLE_DIR + '/' + config_name
        enable_path = cls.__NGINX_DIR + cls.__SITES_ENABLED_DIR + '/' + config_name
        p = subprocess.Popen(["ln -s " + avail_path + " " + enable_path], stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()

    @classmethod
    def disable_config(cls, config_name):
        enable_path = cls.__NGINX_DIR + cls.__SITES_ENABLED_DIR + '/' + config_name
        p = subprocess.Popen(["rm " + enable_path], stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()

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

    @classmethod
    def update_file(cls, path_to_file, content):
        with open(path_to_file, 'w') as f:
            f.write(content)

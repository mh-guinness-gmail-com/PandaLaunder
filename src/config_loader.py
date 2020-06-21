from omegaconf import OmegaConf
from os import listdir, getcwd
from os.path import exists
import pathlib

def _get_dot_file_config(path):
    if not exists(path):
        return OmegaConf.create()
    dot_file_lines = []
    with open(path, 'r') as fp:
        dot_file_lines = fp.readlines()
    return OmegaConf.from_dotlist(dot_file_lines)

def _get_file_config(path):
    if not exists(path):
        return OmegaConf.create()
    config_from_file = OmegaConf.load(path)
    return config_from_file

def _get_cli_config():
    return OmegaConf.from_cli()

def load_config() -> OmegaConf:
    cwd = getcwd()
    config_from_file = _get_file_config('{0}/configs/config.yml'.format(cwd))
    dot_file_config = _get_dot_file_config('{0}/.env'.format(cwd))
    args_config = _get_cli_config()
    final_conf = OmegaConf.merge(config_from_file, dot_file_config, args_config)
    return final_conf
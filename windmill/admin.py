from abc import ABCMeta, abstractmethod, abstractproperty
from copy import deepcopy
import os

import tornado.web
from tornado import template


class RequestHandler(tornado.web.RequestHandler):
    def initialize(self, manager):
        self.manager = manager
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.loader = template.Loader(os.path.join(base_dir, 'templates'))

    def get(self, obj_id=None):
        if obj_id is not None:
            obj = self.manager.get_obj(obj_id)

            fields = deepcopy(self.manager.fields)
            for ((name, _), field) in fields:
                if isinstance(obj, dict):
                    field.value = obj.get(name, '')
                else:
                    field.value = obj.__getattribute__(name, '')

            self.write(self.loader.load('edit.html').generate(fields=fields))
        else:
            obj_list = self.manager.get_list(0, 10)
            self.write(self.loader.load('list.html').generate(
                fields=self.manager.list_display,
                obj_list=obj_list
            ))


class Manager(metaclass=ABCMeta):
    @staticmethod
    @abstractproperty
    def fields():
        raise NotImplementedError()

    @staticmethod
    @abstractproperty
    def list_display():
        raise NotImplementedError()

    @abstractmethod
    def get_obj(self, obj_id):
        raise NotImplementedError()

    @abstractmethod
    def save_obj(self, data, is_new):
        raise NotImplementedError()

    @abstractmethod
    def get_list(self, skip, take, query=None, ordering=list, filtering=dict):
        raise NotImplementedError()


class AdminGenerator:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.handlers = list()

    def add_handler(self, path, handler: type):
        self.handlers.append((path, handler))

    def get_routes(self):
        routes = list()
        for path, handler in self.handlers:
            routes.append((r'/{}/{}/(\d+)?'.format(self.prefix, path),
                           RequestHandler,
                           dict(manager=handler())))
            routes.append((r'/{}/{}'.format(self.prefix, path),
                           RequestHandler,
                           dict(manager=handler())))

        return routes

#!/usr/bin/env python
# !-*- coding:utf-8 -*-
import json
from bin import until


class Bean(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.key = None
        self.value = None
        self.relation = None
        self.xx = None

    @property
    def json(self):
        """JSON format data."""
        json = {
            self.relation: {self.key: self.value}
        }

        if hasattr(self, 'key'):
            json['key'] = self.key
        if hasattr(self, 'key'):
            json['key'] = self.key
        json.update(self.kwargs)
        return json

#
# Copyright (c) 2014 Christopher Bura
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from pythoncad.db.alchemy import DocumentDb
from pythoncad.db import schema


class Drawing(object):
    def __init__(self, db_path):
        self.layers = []
        self.active_layer = None

        # Database Connection
        self.connection = DocumentDb(db_path)
        self.db = self.connection.session
        self.db_path = self.connection.db_path

    def get_property(self, property_name):
        property_value = self.db.query(schema.Setting).filter_by(name=property_name).first()

        if not property_value:
            property_value = schema.Setting(name='drawing_title', value='Untitled')
            self.db.add(property_value)
            self.db.commit()

        return property_value

    def set_property(self, property_name, property_value):
        property_obj = self.get_property(property_name)
        property_obj.value = property_value
        self.db.commit()
        # TODO: Error checking


#!/usr/bin/env python3
"""The initialization module"""

import models.engine.file_storage as s
storage = s.FileStorage()
storage.reload()

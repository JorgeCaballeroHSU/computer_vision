"""
Path module

This module provides a class to manage filesystem paths for images and TFRecords
based on project data stored in a database.

Key features:
- Builds paths from project + material
- Automatically creates directories if they do not exist
- Separates paths by file type (image / tfrecord)
- Ensures safe and valid folder names
"""

import os
from Database.Tables.Tables import DatasetTable


class Path:
    """
    Handles generation, storage, and retrieval of filesystem paths
    for project-related files (images and TFRecords).
    """

    # Valid file types
    VALID_TYPES = {"image", "tfrecord"}

    def __init__(self, dbFile: str) -> None:
        """
        Initialize Path manager.

        Parameters:
            dbFile (str): Path to the SQLite database file
        """
        self.dbFile = dbFile

        # Store paths per type to avoid overwriting
        self._paths = {
            "image": "",
            "tfrecord": ""
        }

        # Default base directories (can be overridden)
        self.windowsAddressPictures = os.getenv(
            "CV_PICTURES_PATH",
            r"D:\Computer Vision Project\01 Pictures"
        )

        self.windowsAddressTFRecords = os.getenv(
            "CV_TFRECORDS_PATH",
            r"D:\Computer Vision Project\02. TCRecords"
        )

        # Project metadata (lazy-loaded)
        self.projectName = None
        self.materialType = None

    # =========================
    # Internal utilities
    # =========================

    def _sanitize(self, text: str) -> str:
        """
        Sanitizes a string to be filesystem-safe.

        Parameters:
            text (str): input string

        Returns:
            str: sanitized string
        """
        return str(text).strip().replace(" ", "_").replace("/", "-")

    def _fetchProjectMaterial(self) -> bool:
        """
        Fetch project name and material type from database.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            dataset = DatasetTable(dbFile=self.dbFile)
            dataset.openConnection()

            data = dataset.fetchDataset()

            if not data:
                raise ValueError("Dataset table is empty")

            last_row = data[-1]

            self.projectName = last_row.get("ProjectName")
            self.materialType = last_row.get("MaterialType")

            dataset.closeConnection()

            return True

        except Exception as e:
            print(f"Error fetching project/material: {e}")
            return False

    def _getBasePath(self, fileType: str) -> str:
        """
        Returns base directory depending on file type.
        """
        if fileType == "image":
            return self.windowsAddressPictures
        elif fileType == "tfrecord":
            return self.windowsAddressTFRecords

        raise ValueError(f"Invalid fileType: {fileType}")

    # =========================
    # Public API
    # =========================

    def loadPath(self, fileType: str) -> str | None:
        """
        Builds and ensures a valid directory path for the given file type.

        Parameters:
            fileType (str): "image" or "tfrecord"

        Returns:
            str | None: Full path if successful, otherwise None
        """
        try:
            if fileType not in self.VALID_TYPES:
                raise ValueError(f"Invalid fileType: {fileType}")

            # Load project info if missing
            if not self.projectName or not self.materialType:
                if not self._fetchProjectMaterial():
                    return None

            basePath = self._getBasePath(fileType)

            # Build safe path
            fullPath = os.path.join(
                basePath,
                self._sanitize(self.projectName),
                self._sanitize(self.materialType)
            )

            # Create directory if needed
            os.makedirs(fullPath, exist_ok=True)

            # Store path
            self._paths[fileType] = fullPath

            return fullPath
        
        except Exception as e:

            # informs about errors if they happen
            print('An error has occured: {}'.format(e))




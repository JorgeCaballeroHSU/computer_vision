"""
Label module

Handles generation of labels for:
- raw samples (images)
- preprocessing outputs
- TFRecord files
"""

from app.Database.Database import DatasetTable


# =========================
# SAMPLE LABELING
# =========================

class LabelSample(DatasetTable):
    """
    Generates labels for raw samples based on:
    - Project Name
    - Material Type
    - Incremental Sample Number
    """

    def __init__(self, dbFile: str) -> None:
        super().__init__(dbFile=dbFile)

        self._projectName = ""
        self._materialType = ""
        self._datasetID = 0
        self._sampleNumber = 0

    # =========================
    # Internal utilities
    # =========================

    def _sanitize(self, text: str) -> str:
        """Make label safe and consistent."""
        return str(text).strip().replace(" ", "-").replace("/", "-")

    def _loadDataset(self) -> bool:
        """Loads latest dataset from DB safely."""
        try:
            # OPEN connection
            self.openConnection()

            data = self.fetchDataset()

            if not data:
                raise ValueError("Dataset is empty")

            last = data[-1]

            self._projectName = self._sanitize(last.get("ProjectName", ""))
            self._materialType = self._sanitize(last.get("MaterialType", ""))
            self._datasetID = last.get("DatasetID", 0)

            return True

        except Exception as e:
            print(f"[LabelSample] Error loading dataset: {e}")
            return False

        finally:
            # ALWAYS close connection
            try:
                self.closeConnection()
            except:
                pass

    def _getSampleCount(self) -> int:
        try:
            self.openConnection()

            statement = f"""
                SELECT COUNT(*) as count
                FROM Sample 
                WHERE DatasetID = {self._datasetID}
            """

            result = self.fetchInfo(statement)

            return result[0]["count"] if result else 0

        except Exception as e:
            print(f"[LabelSample] Error counting samples: {e}")
            return 0

        finally:
            self.closeConnection()


    # =========================
    # Public API
    # =========================

    def generateSampleLabel(self) -> str | None:
        """
        Generates a new sample label.

        Returns:
            str: formatted label or None if failed
        """
        try:
            # Load project info
            if not self._loadDataset():
                return None

            # Get next sample number
            self._sampleNumber = self._getSampleCount() + 1

            label = "_".join([
                self._projectName,
                self._materialType,
                str(self._sampleNumber).zfill(3)
            ])

            return label

        except Exception as e:
            print(f"[LabelSample] Error generating label: {e}")
            return None


# =========================
# PREPROCESSING LABELING
# =========================

class LabelPreprocessing:
    """
    Generates labels for preprocessing outputs.

    Example:
    HSU-HH_K_001_F_01
    """

    def __init__(self, sampleLabel: str, preprocessingType: str = "RAW") -> None:
        self._sampleLabel = sampleLabel
        self._preprocessingType = preprocessingType

    def setProperties(self, sampleLabel: str, preprocessingType: str = None) -> None:
        """Update internal properties."""
        self._sampleLabel = sampleLabel
        if preprocessingType is not None:
            self._preprocessingType = preprocessingType

    def generatePreprocessingLabel(self, number: int) -> str:
        """
        Generates preprocessing label.

        Example:
            HSU-HH_K_001_F_01
        """
        return "_".join([
            self._sampleLabel,
            self._preprocessingType,
            str(number).zfill(2)
        ])


# =========================
# TF RECORD LABELING
# =========================

class LabelTFRecording:
    """
    Generates labels for TFRecord files.

    Example:
    HSU-HH_K_001_F_01_ROT
    """

    def __init__(self, preprocessingLabel: str, augmentationType: str) -> None:
        self._preprocessingLabel = preprocessingLabel
        self._augmentationType = augmentationType

    def setProperties(self, preprocessingLabel: str, augmentationType: str) -> None:
        """Update internal properties."""
        self._preprocessingLabel = preprocessingLabel
        self._augmentationType = augmentationType

    def generateTensorFlowRecordLabel(self) -> str:
        """Generate TFRecord label."""
        return "_".join([
            self._preprocessingLabel,
            self._augmentationType
        ])

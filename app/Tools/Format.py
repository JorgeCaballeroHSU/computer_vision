# it contains a function that adds the data-tpye to the name of the file
import os

def addDataType(fileName: str, dataType: str) -> str:
    """
    Adds/overwrites file extension safely.
    """

    if not dataType:
        raise ValueError("Data type must be provided")

    dataType = dataType.lstrip(".")  # remove leading dots

    name, _ = os.path.splitext(fileName)  # remove old extension

    return f"{name}.{dataType}"


import io

import intake
import intake.source


class ExcelSource(intake.source.base.DataSource):
    """Intake source for reading Excel files from URLs.

    Supports simplecache:: prefix for caching.
    """

    container = "dataframe"
    name = "excel_url"
    version = "0.0.1"

    def __init__(
        self,
        urlpath,
        sheet_name="Global Carbon Budget",
        header=21,
        index_col="Year",
        skipfooter=4,
        metadata=None,
    ):
        """Initialize Excel source.

        Args:
            urlpath: URL or simplecache path to Excel file
            sheet_name: Name of sheet to read
            header: Row number to use as header (0-indexed)
            index_col: Column to use as index
            skipfooter: Number of rows to skip at end
            metadata: Additional metadata
        """
        super().__init__(metadata=metadata)
        self.urlpath = urlpath
        self.sheet_name = sheet_name
        self.header = header
        self.index_col = index_col
        self.skipfooter = skipfooter

    def _get_schema(self):
        return intake.source.base.Schema(
            datatypes={"_": "python"},
            shape=(None, None),
            npartitions=1,
            metadata=self.metadata,
        )

    def _load(self):
        import fsspec
        import pandas as pd

        fs, _token, paths = fsspec.get_fs_token_paths(self.urlpath)
        path = paths[0]
        with fs.open(path, "rb") as f:
            return pd.read_excel(
                io.BytesIO(f.read()),
                sheet_name=self.sheet_name,
                header=self.header,
                index_col=self.index_col,
                skipfooter=self.skipfooter,
            )

    def read(self):
        return self._load()

    def _close(self):
        pass


intake.source.register_driver("excel_url", ExcelSource)

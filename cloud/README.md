# Optional cloud layer

The original proof of concept used Azure Blob Storage for CSV logs and images, Azure Data Factory to move event records into Azure SQL, and Streamlit for remote visualisation.

The archived project did not preserve an exportable Azure Data Factory pipeline definition or the original SQL DDL. This repository therefore does not claim full infrastructure-as-code reproducibility for the cloud layer.

`schema.sql` is a small reference schema reconstructed from the four-column event CSV used by the hub and from the query used by `streamlit_dashboard.py`. It is compatible with the curated code but is not presented as the exact historical SQL schema.

Runtime credentials must be supplied through environment variables documented in `docs/deployment.md`. Do not commit Azure connection strings or SQL credentials.

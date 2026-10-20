-- Reference schema compatible with the curated CSV event format and Streamlit dashboard.
-- This is not a recovered copy of the original Azure SQL DDL.

CREATE TABLE dbo.events_log (
    [timestamp] datetime2 NULL,
    [location] nvarchar(255) NULL,
    [event] nvarchar(255) NULL,
    [details] nvarchar(max) NULL
);

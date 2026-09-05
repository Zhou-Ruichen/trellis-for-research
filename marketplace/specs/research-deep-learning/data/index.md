# Data Guidelines

Keep shared data roots read-only by default. Write temporary or rebuildable
products to the project's existing interim or output location; the evidence
a durable product keeps is defined in
[reproducibility.md](../shared/reproducibility.md). Do not rename an
existing layout to match the raw, interim, processed, and output concepts.

For data too large to version, record a reproducible pointer: configured
root or protocol, dataset version or retrieval date, resolution rule, and
the variables or extent consumed. Use a checksum only when exact byte
identity affects transfer integrity, deduplication, or reproduction. Record
split and sampling rules for a durable product in its existing processing
log or data note.

## Checks at the data boundary

Check once, where data enters the pipeline, only conditions whose failure
could silently change the scientific result:

- units, coordinate or key conventions, shapes, dimensions, and dtypes;
- missing values, NaN, fill values, and sentinel conversion;
- label meanings and leakage across samples, subjects, groups, locations,
  or time;
- filtering, interpolation, resampling, masking, and augmentation
  parameters.

Let the data library report missing files, unsupported formats, malformed
syntax, and ordinary I/O errors; no generic validator or preflight
checklist.

## Format details

For netCDF or Zarr, preserve consumed variable names, units, CF metadata,
fill-value handling, and encoding or chunking when they affect model inputs
or reconstruction. For geospatial data, record CRS, longitude convention,
grid definition, and reprojection or resampling parameters when used. For
time series, record time encoding, timezone, aggregation, and join
tolerance when relevant. For other formats, retain the fields and metadata
needed to interpret the model input and rebuild the product.

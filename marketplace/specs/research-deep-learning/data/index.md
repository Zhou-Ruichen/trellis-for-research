# Data Guidelines

Apply these rules when reading, writing, validating, or transforming data.
Keep shared data roots read-only by default. Write temporary or rebuildable
products to the project's existing interim or output location, and retain
durable products with the source and processing information needed to rebuild
or interpret them.

## Layout and provenance

Map the existing project layout to these concepts where useful:

- raw or external: immutable local inputs and read-only upstream sources;
- interim: temporary, rebuildable products;
- processed: model-ready or otherwise durable products;
- outputs: run-specific predictions, checkpoints, and evidence.

Do not rename directories just to match this list. For data too large to
version, record a reproducible pointer: configured root or protocol, dataset
version or retrieval date, resolution rule, and variables or extent consumed.
Use a checksum only when exact byte identity affects transfer integrity,
deduplication, or reproduction.

Record the processing command or notebook, source version, split and sampling
rules, relevant parameters, and output location for a durable product. An
existing processing log or data note is sufficient; no fixed manifest file or
field list is required.

## Checks at the data boundary

Check only conditions whose failure could silently change the scientific result:

- units, coordinate or key conventions, shapes, dimensions, and dtypes;
- missing values, NaN, fill values, and sentinel conversion;
- label meanings and leakage across samples, subjects, groups, locations, or time;
- filtering, interpolation, resampling, masking, and augmentation parameters.

Let the data library report missing files, unsupported formats, malformed syntax,
and ordinary I/O errors. Do not add a generic validator or preflight checklist
for these failures.

## Applicable format details

For netCDF or Zarr, preserve consumed variable names, units, CF metadata,
fill-value handling, and encoding or chunking when they affect model inputs or
reconstruction. For geospatial data, record CRS, longitude convention, grid
definition, and reprojection or resampling parameters when used. For time
series, record time encoding, timezone, aggregation, and join tolerance when
relevant. For other formats, retain the fields and metadata needed to interpret
the model input and rebuild the product.

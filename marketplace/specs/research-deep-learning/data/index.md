# Data Guidelines

Use these rules whenever reading, writing, validating, or transforming data.

The project may keep data under `data/`. The rule is not "no data in repo"; the
rule is "data must have lifecycle, provenance, and rebuild instructions."

## Documentation Files

| File | Read when |
| --- | --- |
| [../shared/project-layout.md](../shared/project-layout.md) | Naming data paths |
| [../shared/reproducibility.md](../shared/reproducibility.md) | Writing manifests and run records |
| [../shared/anti-bloat.md](../shared/anti-bloat.md) | Adding processing scripts or variants |

## General Data Rules

### Data Layout

```text
data/
  raw/
  external/
  interim/
  processed/
  manifests/
```

Use `data/raw/` for immutable local raw inputs or symlinks. Use `data/external/`
for read-only external data roots or symlink targets. Use `data/interim/` for
temporary but rebuildable products. Use `data/processed/` for model-ready
datasets.

### Data Lake Rule

If a project reads from a shared data root such as `<shared-data-root>`, treat
that location as read-only by default.

Project code should write to local `data/interim/`, `data/processed/`, or
`outputs/<run_id>/`. Writing back into a shared data lake requires an explicit
data-processing task and a manifest.

### Manifest Rule

Every durable data product needs a manifest in `data/manifests/`.

Required fields:

```json
{
  "name": "training_data_v1",
  "created_at": "2026-06-10T14:22:33Z",
  "created_by": "python scripts/build_dataset.py --config configs/data/baseline.yaml",
  "source_paths": [],
  "source_versions": {},
  "processing_config": "configs/data/baseline.yaml",
  "output_paths": [],
  "checksums": {},
  "scope": null,
  "split_policy": "recorded in data/manifests/splits_v1.json",
  "assumptions": []
}
```

Do not invent unavailable fields. Use `null`, an empty list, or a clear
assumption only when the value is truly unknown.

### Boundary Validation

Validate at the point where data enters the project:

- file exists and format is expected;
- array shapes match config;
- dtype is expected;
- NaN and fill-value handling is explicit;
- labels, units, coordinate fields, or other model inputs have defined meanings;
- train/validation/test splits do not share samples, subjects, groups, locations,
  or time ranges when that would leak information.

## Format-Specific Rules

Apply only the subsections that match the data in the project. Record each
relevant item in the data manifest or check it once at the data boundary.

### Array Formats (netCDF / Zarr)

For `.nc` (netCDF / CF) and `.zarr` stores used as inputs or durable products:

- Record the format, the library and version that read or wrote it (for example
  `xarray` + `h5netcdf`, or `zarr` + storage backend), and the encoding options
  (compression, filters, shuffling).
- Record every variable name consumed and the `units` attribute for each
  physical variable. Do not strip CF attributes when writing processed products.
- Handle `_FillValue` / `missing_value`, `scale_factor`, and `add_offset`
  explicitly: apply or preserve them at the boundary and record the convention
  used. Never silently let fill values enter model inputs.
- For Zarr, record the chunk shape and storage layout (for example dimension
  order and chunks) so a re-opened store matches the access pattern the pipeline
  expects.

### Geospatial Data

- Record the CRS for every geospatial product: an EPSG code, a PROJ string, or a
  CF `grid_mapping` variable. "Assumed lat/lon" is not a CRS record.
- Record the longitude convention (`[-180, 180]` or `[0, 360]`) and latitude
  bounds at the boundary, and any reprojection or resampling step with its
  parameters.
- Record the affine transform or grid spacing (for rasters) and the pixel
  interpretation (pixel-center vs pixel-corner).

### Time-Series Data

- Record the time coordinate encoding: CF `units` and `calendar`, or an
  ISO-8601 column, plus the timezone if any.
- Record any time aggregation, resampling, or subsetting (for example monthly
  mean, rolling window) and the boundary handling.
- When matching observations across products, record the join tolerance in time
  and the reference time scale.

### Chunking And Access Pattern

- Match array chunking to the dominant access pattern (time-series reads vs
  spatial tiles) and record the chosen chunk shape in the manifest.
- Record whether reads are dask-backed and the task chunk size when that affects
  determinism or memory.

### External Data Pointers

For data too large to version in the repository:

- Store a pointer, not the bytes: an absolute or configured root path, a
  protocol (file, S3, HTTPS, OpenDAP), and the dataset version or collection.
- Record the resolution rule in the manifest (environment variable or config
  key that expands to the real path) so the pointer is reproducible on another
  machine.
- Record a checksum of the resolved source only when exact byte identity
  matters. Otherwise record the upstream version identifier, retrieval date,
  expected size or record count, and consumed variables.

### Data Identity

- Use a checksum only for a concrete byte-identity need such as transfer
  integrity or distinguishing otherwise identical versions. Do not build chunk
  manifests or hashing machinery only to make a record look complete.
- For versioned upstream data, prefer the source version, retrieval date,
  variables, spatial/temporal extent, and processing configuration.

### Domain-Specific Data

When a domain format or scientific quantity carries metadata needed to interpret
the model input or result:

- Record the variables or fields consumed from the source format.
- Record resampling, gridding, interpolation, detrending, filtering, and masking parameters.
- Keep coordinate transforms explicit when coordinates are present.
- Preserve enough metadata to rebuild the processed dataset from source data.
- When matching multiple sources, record the join key and tolerance.

## Data Processing Entrypoints

Use one stable entrypoint per durable processing stage:

```text
scripts/build_dataset.py
scripts/validate_dataset.py
scripts/export_product.py
```

Do not create:

```text
scripts/build_dataset_v2.py
scripts/build_dataset_final.py
scripts/1_make_data.py
scripts/2_fix_data.py
```

If the stage changes, update config and manifest, not the script name.

## Quality Check

- [ ] Durable data output has a manifest.
- [ ] Splits are recorded and leakage-checked for the relevant scientific question.
- [ ] Data paths are config-driven, not hardcoded workstation paths.
- [ ] NaN/fill values and the meaning of model inputs are explicit.
- [ ] For netCDF/Zarr, when used: variable names, units, fill-value handling, and chunk
      layout are recorded.
- [ ] For geospatial data, when used: CRS, coordinate conventions, and grid
      definition are recorded.
- [ ] For time-series data, when used: time encoding, aggregation, and join
      tolerance are recorded.
- [ ] External data is a reproducible pointer (root, protocol, version) with
      the metadata needed to identify the consumed data; checksums are used
      only when exact byte identity matters.
- [ ] Large generated data is ignored by git unless the user explicitly chooses to version a small fixture.

# Guide: Debug NaN, Inf, Divergence, Or OOM

Use for an observed training failure. Start from its traceback and the
affected batch or operation; inspect the smallest amount of data that explains it.

## NaN Or Inf

Locate the first operation producing unexpected non-finite values. Inspect its
inputs, masks, normalization, and precision as relevant. Anomaly detection or a
smaller batch can help locate the failure.

Add `nan_to_num` or loss skipping when the data policy calls for it, and
record the behavior with the run.

## OOM

Locate the allocation or tensors involved. Inspect batch dimensions,
precision, activations, or evaluation accumulation as the failure indicates.
Use a smaller case for diagnosis. The comparison keeps its training
settings, and a rerun is recorded as a rerun.

Print the values needed to locate the failure, and remove temporary
diagnostics afterward.

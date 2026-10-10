# Guide: Debug NaN, Inf, Divergence, Or OOM

Use for an observed training failure. Start from its traceback and the
affected batch or operation; inspect the smallest amount of data that explains it.

## NaN Or Inf

Locate the first operation producing unexpected non-finite values. Inspect its
inputs, masks, normalization, and precision as relevant. Anomaly detection or a
smaller batch can help locate the failure.

Non-finite values are diagnosed at their source. `nan_to_num` or loss
skipping enters the code only where the data policy requires it, and the run
record states that it is active.

## OOM

Locate the allocation or tensors involved. Inspect batch dimensions,
precision, activations, or evaluation accumulation as the failure indicates.
Use a smaller case for diagnosis. The comparison's training settings stay as
they were, and a rerun is a recorded decision rather than an automatic retry.

Print the values needed to locate the failure, and remove temporary
diagnostics afterward.

# Guide: Debug NaN, Inf, Divergence, Or OOM

Use only for an observed training failure. Start from its traceback and the
affected batch or operation; inspect the smallest amount of data that explains it.

## NaN Or Inf

Locate the first operation producing unexpected non-finite values. Inspect its
inputs, masks, normalization, and precision as relevant. Anomaly detection or a
smaller batch can help locate the failure; neither is a required preliminary run.

Do not add broad `nan_to_num` or silent loss skipping unless the data policy
explicitly requires it and the behavior is recorded.

## OOM

Locate the allocation or retained tensors involved. Inspect batch dimensions,
precision, activations, or evaluation accumulation only as the failure indicates.
Use a smaller case if it helps diagnosis; do not silently change the comparison's
training settings or add automatic retry logic.

Print only the values needed to locate the failure, and remove temporary
diagnostics afterward.

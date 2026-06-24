import mlflow

mlflow.set_experiment("Fit_Rep")

def start_run(exercise, up_threshold, down_threshold):
    run = mlflow.start_run()
    mlflow.log_param("exercise", exercise)
    mlflow.log_param("up_threshold", up_threshold)
    mlflow.log_param("down_threshold", down_threshold)
    return run.info.run_id

def log_rep_metrics(rep_count, avg_confidence, min_confidence):
    mlflow.log_metric("rep_count", rep_count)
    mlflow.log_metric("avg_confidence", avg_confidence)
    mlflow.log_metric("min_confidence", min_confidence)

def log_angle_metrics(max_angle, min_angle, average_up_angle, average_down_angle):
    mlflow.log_metric("max_angle", max_angle)
    mlflow.log_metric("min_angle", min_angle)
    mlflow.log_metric("average_up_angle", average_up_angle)
    mlflow.log_metric("average_down_angle", average_down_angle)

def end_run():
    mlflow.end_run()
import unittest

from src.pipeline.prediction_pipeline import PredictionPipeline


class PredictionPipelineTest(unittest.TestCase):
    def test_prediction_pipeline_uses_local_model_fallback(self):
        pipeline = PredictionPipeline()
        model = pipeline.get_trained_model()

        self.assertTrue(hasattr(model, "predict"))

        sample_input = [
            35, 2, 1, 0, 2, 50000.0, 1200.0, 600, 30, 200, 50, 70, 30.0, 20, 10.0, 3, 4, 5, 2, 1, 2
        ]
        prediction = pipeline.run_pipeline(sample_input)
        self.assertTrue(len(prediction) > 0)


if __name__ == "__main__":
    unittest.main()

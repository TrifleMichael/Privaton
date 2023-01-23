class Environment:
    def __init__(self):
        # self.variable_names_map = {}
        # self.condition_evaluation_map = {}
        # self.block_ignore_map = {}
        # self.expressions_value_map = {}
        self.evaluations = []

    def get_environment(self) -> dict:
        environment_dict = {
            # "variables": self.variable_names_map,
            # "if_evaluations": self.condition_evaluation_map,
            # "block_ignore": self.block_ignore_map,
            # "expressions_evaluations": self.expressions_value_map,
            "latest_evaluations": self.evaluations
        }
        return environment_dict

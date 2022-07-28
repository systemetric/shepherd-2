from app.runner import Runner, States

class TestRunner():
    def setup(self):
        self.runner = Runner()

    def test_runner_inital_state(self):
        assert self.runner.state == States.READY
